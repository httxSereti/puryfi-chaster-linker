import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.chaster import PartnerGetSessionAuthRepDto
from models.sql.user_lock_configuration import UserLockConfiguration
from schemas.chaster_extension_session_schema import ChasterExtensionSessionSchema

router = APIRouter(prefix="/api/extensions", tags=["extensions"])

@router.get("/auth/sessions/{mainToken}", response_model=ChasterExtensionSessionSchema)
async def fetch_session(mainToken: str, db: Session = Depends(get_db)):
    """
        Fetch Chaster session and create a UserLockConfiguration for it
        using the Developer Token and mainToken issued when opening iframe on chaster app
    """
    developer_token = os.getenv("CHASTER_DEVELOPER_TOKEN", "")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {developer_token}"
    }

    data: PartnerGetSessionAuthRepDto | None = None

    try:
        response = requests.get(
            f"https://api.chaster.app/api/extensions/auth/sessions/{mainToken}",
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    # Fetch or create a UserLockConfiguration for this Chaster session
    session_id: str = data.get("session", {}).get("sessionId", "")
    lock_id: str = data.get("session", {}).get("lock", {}).get("_id", "")
    keyholder = data.get("session", {}).get("lock", {}).get("keyholder")
    keyholder_id: str | None = keyholder.get("_id") if isinstance(keyholder, dict) else None
    wearer = data.get("session", {}).get("lock", {}).get("user")
    wearer_id: str | None = wearer.get("_id") if isinstance(wearer, dict) else None

    lock_config = db.query(UserLockConfiguration).filter_by(session_id=session_id).first()

    if lock_config is None:
        lock_config = UserLockConfiguration(
            session_id=session_id,
            lock_id=lock_id or None,
            keyholder_id=keyholder_id,
            wearer_id=wearer_id,
        )
        db.add(lock_config)
        db.commit()
        db.refresh(lock_config)
        print(f"[DB] Created UserLockConfiguration for session {session_id!r}")
    else:
        print(f"[DB] Found existing UserLockConfiguration for session {session_id!r}")

    session_schema = ChasterExtensionSessionSchema(
        id=lock_config.id,
        role=data.get("role", ""),
        is_linked=lock_config.is_linked,
        link_token=lock_config.link_token,
    )
    return session_schema


@router.post("/sessions/{session_id}/link-token", response_model=ChasterExtensionSessionSchema)
async def create_link_token(session_id: str, db: Session = Depends(get_db)):
    """
        Generate a unique link_token for the UserLockConfiguration identified by session_id.
        Idempotent: returns the existing token if one already exists.
    """
    from models.sql.base import cuid

    lock_config = db.query(UserLockConfiguration).filter_by(id=session_id).first()
    if lock_config is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if not lock_config.link_token:
        lock_config.link_token = cuid()
        db.commit()
        db.refresh(lock_config)
        print(f"[DB] Generated link_token for session {session_id!r}")

    return ChasterExtensionSessionSchema(
        id=lock_config.id,
        role="",  # role not stored on the config row
        is_linked=lock_config.is_linked,
        link_token=lock_config.link_token,
    )

@router.get("/configuration/{configurationToken}")
async def configuration(configurationToken: str):
    """
        Get the configuration of the extension
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
            f"https://api.chaster.app/api/extensions/configurations/{configurationToken}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
