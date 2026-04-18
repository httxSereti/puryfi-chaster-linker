import os
import requests
from fastapi import APIRouter, HTTPException
from models.chaster import PartnerGetSessionAuthRepDto

router = APIRouter(tags=["chaster", "extensions"])

@router.get("/api/extensions/auth/sessions/{mainToken}", response_model=PartnerGetSessionAuthRepDto)
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
