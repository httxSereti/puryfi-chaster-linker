async def handle_lock_unfrozen(payload: dict) -> dict:
    """
    Handle the 'lock_unfrozen' event action from Chaster.
    """
    print("lock unfrozen action triggered")
    # TODO: Implement lock_unfrozen logic
    return {"status": "ok", "action": "lock_unfrozen_processed"}
