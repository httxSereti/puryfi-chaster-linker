from models.connection_manager import manager

async def puryfi_lock(userId: str):
    connection = manager.get_by_username(userId)

    if not connection:
        return {"status": "Puryfi is offline/not linked."}

    resPassword = await connection.send_message("setState", {
            "path": "lockConfiguration", 
            "value": {
                "password": {"secret": "test"}
            }
        })
    return resPassword