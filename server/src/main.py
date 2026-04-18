import os
from dotenv import load_dotenv
import asyncio
import msgpack
import requests

load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.chaster_api import addDurationToLock
from models.chaster import PartnerGetSessionAuthRepDto

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manifest = {
    "name": "Puryfi-Chaster-Linker",
    "version": "1.0.0",
    "description": "Link Puryfi with your Chaster lock",
    "author": "Sereti",
    "website": "https://paa.ge/sereti",
}

class Connection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.next_response_id = 0
        self.pending_requests = {}
        self.username = ""
        self.configuration = {
            "logEmptyObjects": {
                "name": "Log Empty Scans",
                "type": "boolean",
                "value": False,
            },
            "chasterToken": {
                "name": "Your Chaster API token",
                "type": "string",
                "value": "",
            },
            "chasterLockId": {
                "name": "Chaster Lock Identifier to interact with",
                "type": "string",
                "value": "",
            },
            "chasterConsequenceDuration": {
                "name": "Duration to add to the lock (in seconds)",
                "type": "number",
                "value": 60,
            },
            "chasterConsequenceTriggerNumber": {
                "name": "Number of times subject is allowed to view a Censored Object",
                "type": "number",
                "value": 100,
            },
        }
        self.store = {
            "censoredPicturesViewed": 0,
        }
        self.intents_granted_event = asyncio.Event()

    async def send_message(self, msg_type: str, payload: dict) -> dict:
        response_id = self.next_response_id
        self.next_response_id += 1
        
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[response_id] = future
        
        message = {
            "type": msg_type,
            "payload": payload,
            "responseId": response_id
        }
        encoded = msgpack.packb(message)
        await self.websocket.send_bytes(encoded)
        
        return await future

    async def send_response(self, response_id: int, payload: dict):
        message = {
            "payload": payload,
            "responseId": response_id
        }
        encoded = msgpack.packb(message)
        await self.websocket.send_bytes(encoded)

    async def handle_message(self, data: bytes):
        message = msgpack.unpackb(data)
        
        if "type" not in message:
            response_id = message.get("responseId")
            if response_id is not None and response_id in self.pending_requests:
                self.pending_requests[response_id].set_result(message.get("payload"))
                del self.pending_requests[response_id]
            return
        
        msg_type = message.get("type")
        payload = message.get("payload", {})
        response_id = message.get("responseId")
        response = None

        if msg_type == "ready":
            response = {"type": "ok"}
            # Start initialization process in background
            asyncio.create_task(self.initialize_plugin())
            
        elif msg_type == "configurationChange":
            self.configuration = payload.get("configuration", self.configuration)
            
        elif msg_type == "intentsGrant":
            granted_intents = payload.get("intents", [])
            required_intents = ["readUserState", "readMediaProcesses"]
            if all(intent in granted_intents for intent in required_intents):
                self.intents_granted_event.set()
                
        elif msg_type == "staticMediaScan":
            objects = payload.get("objects", [])
            is_log_empty = self.configuration.get("logEmptyObjects", {}).get("value", False)
            
            if not is_log_empty and len(objects) == 0:
                pass
            else:
                print(f"Scan event: {len(objects)} object(s) detected")
                for obj in objects:
                    # user had something censored in his view
                    self.store["censoredPicturesViewed"] += 1
                    if self.store["censoredPicturesViewed"] >= self.configuration.get("chasterConsequenceTriggerNumber", {}).get("value", 5):
                        # trigger duration add
                        print("[Puryfi-Linker] Too many censored pictures seen! Adding {} seconds to lock".format(self.configuration.get("chasterConsequenceDuration", {}).get("value", 60)))
                        data = addDurationToLock(
                            lockId=self.configuration.get("chasterLockId", {}).get("value", ""),
                            duration=self.configuration.get("chasterConsequenceDuration", {}).get("value", 60),
                            token=self.configuration.get("chasterToken", {}).get("value", ""),
                        )
                        print(data)
                        self.store["censoredPicturesViewed"] = 0

        if response_id is not None and response is not None:
            await self.send_response(response_id, response)

    async def initialize_plugin(self):
        try:
            # 1. Set Plugin Manifest
            res = await self.send_message("setPluginManifest", {"manifest": manifest})
            if res.get("type", "") == "error":
                print(f"Failed to set plugin manifest: {res.get('message')}")
                return

            # 2. Set Plugin Configuration
            res = await self.send_message("setPluginConfiguration", {"configuration": self.configuration})
            if res.get("type", "") == "error":
                print(f"Failed to set plugin configuration: {res.get('message')}")
                return

            # 3. Request Intents
            intents = ["readUserState","readMediaProcesses"]
            res = await self.send_message("getPluginIntents", {})
            if res.get("type", "") == "error":
                print(f"Failed to get plugin intents: {res.get('message')}")
                return
                
            granted_intents = res.get("intents", [])
            if not all(intent in granted_intents for intent in intents):
                res = await self.send_message("requestPluginIntents", {"intents": intents})
                if res.get("type", "") == "error":
                    print(f"Failed to request plugin intents: {res.get('message')}")
                    return
                # Wait for the client to grant intents through the 'intentsGrant' message
                await self.intents_granted_event.wait()
                
            # 4. Subscribe to Static Media Scans
            res = await self.send_message("subscribeToStaticMediaScans", {})
            if res.get("type", "") == "error":
                print(f"Failed to subscribe to static media scans: {res.get('message')}")
                return

            # 5. Get User State for username
            res = await self.send_message("getState", {"path": "user.username"})
            username = res.get("value")
            self.username = username

        except Exception as e:
            print(f"Initialization error: {e}")

connections: list[Connection] = []

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection = Connection(websocket)
    connections.append(connection)
    print("New client connected to WebSocket connection on port 8090")
    try:
        while True:
            data = await websocket.receive_bytes()
            await connection.handle_message(data)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket connection")

@app.get("/webhook/{username}", tags=["chaster"])
async def read_chaster_webhook(username: str):
    print(username)

    for connection in connections:
        print(connection.username)
        if connection.username.lower() == username.lower():
            # connection.send_message()
            return {"status": "ok"}


    return {"status": "error"}

@app.get("/api/extensions/auth/sessions/{mainToken}", tags=["chaster", "extensions"], response_model=PartnerGetSessionAuthRepDto)
async def exchange_main_token(mainToken: str):
    """
        Exchange the mainToken for the Chaster session object
        using the Developer Token
    """
    developer_token = os.getenv("CHASTER_DEVELOPER_TOKEN", "")
    
    if not developer_token:
        print("[WARNING] CHASTER_DEVELOPER_TOKEN empty!")
        
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {developer_token}"
    }
    
    try:
        response = requests.get(
            f"https://api.chaster.app/api/extensions/auth/sessions/{mainToken}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    print("WebSocket server listening on port 8090")
    uvicorn.run(app, host="127.0.0.1", port=8090)
