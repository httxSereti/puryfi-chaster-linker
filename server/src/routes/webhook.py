from fastapi import APIRouter
from models.connection_manager import manager

router = APIRouter(tags=["chaster"])

@router.get("/webhook/{username}")
async def read_chaster_webhook(username: str):
    print(username)

    connection = manager.get_by_username(username)
    if connection:
        # enable Puryfi
        resEnabled = await connection.send_message("setState", {"path": "enabled", "value": True})
        print(resEnabled)

        print("--------")
        # lock puryfi
        resPassword = await connection.send_message("setState", {
            "path": "lockConfiguration", 
            "value": {
                "password": {"secret": "test"}
            }
        })
        # resToken = await connection.send_message("setState", {"path": "lockConfiguration.emergencyClientToken", "value": 444})
       
        print(resPassword)
        # print(resToken)

        return {"status": "ok"}

    return {"status": "Puryfi is offline/not linked."}
