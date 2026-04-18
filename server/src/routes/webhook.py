from fastapi import APIRouter
from models.connection_manager import manager

router = APIRouter(tags=["chaster"])

@router.get("/webhook/{username}")
async def read_chaster_webhook(username: str):
    print(username)

    connection = manager.get_by_username(username)
    if connection:
        # connection.send_message()
        return {"status": "ok"}

    return {"status": "error"}
