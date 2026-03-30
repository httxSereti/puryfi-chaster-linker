import requests

def addDurationToLock(lockId: str, duration: int, token: str) -> bool:
    """
        Add duration to a Chaster Lock
    """
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    try:
        data = requests.post(
            url=f"https://api.chaster.app/locks/{lockId}/update-time",
            headers=headers,
            json={"duration": duration},
        )
        data.raise_for_status()
        
        if data.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error adding duration: {e}")
        return False
    