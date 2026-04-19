from fastapi import APIRouter
from models.connection_manager import manager   
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi import status, Depends, HTTPException, Request
import os
import secrets
from pprint import pprint

router = APIRouter(tags=["chaster"])
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


@router.post("/extension/webhooks/chaster")
async def read_chaster_webhook(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    print("----- PAYLOAD -----")
    data = await request.json()
    pprint(data)
    
    # connection = manager.get_by_username(username)
    # if connection:
    #     # enable Puryfi
    #     resEnabled = await connection.send_message("setState", {"path": "enabled", "value": True})
    #     print(resEnabled)

    #     print("--------")
    #     # lock puryfi
    #     resPassword = await connection.send_message("setState", {
    #         "path": "lockConfiguration", 
    #         "value": {
    #             "password": {"secret": "test"}
    #         }
    #     })
    #     # resToken = await connection.send_message("setState", {"path": "lockConfiguration.emergencyClientToken", "value": 444})
       
    #     print(resPassword)
    #     # print(resToken)

    #     return {"status": "ok"}

    return {"status": "ok"}
