import os
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


def create_custom_log(session_id: str, title: str, description: str, icon: str = "link", color: str = "#ffffff") -> bool:
    """
    POST /api/extensions/sessions/{sessionId}/logs/custom
    Create a custom log entry for an extension lock session.
    """
    developer_token = os.getenv("CHASTER_DEVELOPER_TOKEN", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {developer_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "role": "user",
        "icon": icon,
        "color": color,
        "title": title,
        "description": description,
    }

    try:
        response = requests.post(
            url=f"https://api.chaster.app/api/extensions/sessions/{session_id}/logs/custom",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[Chaster] Error creating custom log: {e}")
        return False