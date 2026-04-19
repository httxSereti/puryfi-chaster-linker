from db import SessionLocal
from models.sql.user_lock_configuration import UserLockConfiguration
from utils.chaster_api import create_custom_log


async def link_with_token(link_token: str, username: str = "user") -> bool:
    """
    Look up the UserLockConfiguration matching link_token and mark it as linked.
    Returns True if the link was successful, False otherwise.
    """
    try:
        db = SessionLocal()
        lock_config = (
            db.query(UserLockConfiguration)
            .filter_by(link_token=link_token)
            .first()
        )

        if lock_config is None:
            print(f"[Link] No UserLockConfiguration found for token {link_token!r}")
            db.close()
            return False

        lock_config.is_linked = True
        db.commit()

        session_id = lock_config.session_id
        db.close()

        print(f"[Link] Session {lock_config.id!r} is now linked ✓")

        # Post a custom log entry to the Chaster lock session
        if session_id:
            create_custom_log(
                session_id=session_id,
                title="%USER% linked Puryfi",
                description=f"Puryfi linked as '{username}' — monitoring is now active.",
                icon="link",
                color="#ffffff",
            )

        return True

    except Exception as e:
        print(f"[Link] Error during linking: {e}")
        return False
