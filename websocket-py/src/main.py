import asyncio
import msgpack
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class Connection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.next_response_id = 0
        self.pending_requests = {}
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
                    label = obj.get("label", "Unknown")
                    score = obj.get("score", 0.0)
                    rect = obj.get("rect", {})
                    x = rect.get("x", 0.0)
                    y = rect.get("y", 0.0)
                    width = rect.get("width", 0.0)
                    height = rect.get("height", 0.0)
                    print(f"label={label} score={score:.3f} at ({x:.3f}, {y:.3f}) {width:.3f}x{height:.3f}")

        if response_id is not None and response is not None:
            await self.send_response(response_id, response)

    async def initialize_plugin(self):
        try:
            # 1. Set Plugin Manifest
            manifest = {
                "name": "Puryfi-Chaster-Linker",
                "version": "1.0.0",
                "description": "Link Puryfi with your Chaster lock",
                "author": "Sereti <httxsereti@gmail.com>",
                "website": "https://paa.ge/sereti",
            }
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
            intents = ["readUserState", "readMediaProcesses"]
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
                
            # 5. Get User State
            res = await self.send_message("getState", {"path": "user.username"})
            print("received state")
            print(res)

        except Exception as e:
            print(f"Initialization error: {e}")

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection = Connection(websocket)
    print("New client connected to WebSocket connection on port 8093")
    try:
        while True:
            data = await websocket.receive_bytes()
            await connection.handle_message(data)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket connection")

if __name__ == "__main__":
    import uvicorn
    print("WebSocket server listening on port 8093")
    uvicorn.run(app, host="127.0.0.1", port=8090)
