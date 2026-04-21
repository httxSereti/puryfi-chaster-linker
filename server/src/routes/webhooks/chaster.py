from fastapi import APIRouter
from models.connection_manager import manager   
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi import status, Depends, HTTPException, Request
from .actions import handle_lock_frozen, handle_lock_unfrozen, handle_extension_updated
import os
import secrets
from pprint import pprint

router = APIRouter(prefix="/api/webhooks", tags=["webhook"])
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    expected_user = os.getenv("CHASTER_WEBHOOK_USER", "")
    expected_pwd = os.getenv("CHASTER_WEBHOOK_PWD", "")
    
    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), 
        expected_user.encode("utf8")
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), 
        expected_pwd.encode("utf8")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.post("/extensions/chaster")
async def chaster_webhook(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    """
        Chaster webhook endpoint
    """
    print("----- PAYLOAD -----")
    data = await request.json()
    pprint(data)
    
    event: str = data["event"]
    requestId: str = data["requestId"]

    print(f"event '{event}'")
    print(f"requestId '{requestId}'")
    print("-------------")
    
    if event == "action_log.created":
        actionPayload: dict = data["data"]["actionLog"]
        actionType: str = actionPayload["type"]

        print(f"actionType '{actionType}'")
        
        if actionType == "lock_frozen":
            return await handle_lock_frozen(data)

        if actionType == "lock_unfrozen":
            return await handle_lock_unfrozen(data)

        if actionType == "extension_updated":
            return await handle_extension_updated(data)

    return {"status": "ok"}
