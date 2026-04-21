import db
from models.sql.queued_message import QueuedMessage

def queue_message(link_token: str, msg_type: str, payload: dict) -> None:
    db._ensure_engine()
    with db.SessionLocal() as db_session:
        msg = QueuedMessage(link_token=link_token, msg_type=msg_type, payload=payload)
        db_session.add(msg)
        db_session.commit()

def fetch_and_delete_queued_messages(link_token: str) -> list[dict]:
    db._ensure_engine()
    with db.SessionLocal() as db_session:
        messages = db_session.query(QueuedMessage).filter_by(link_token=link_token).all()
        result = [{"msg_type": msg.msg_type, "payload": msg.payload} for msg in messages]
        for msg in messages:
            db_session.delete(msg)
        db_session.commit()
        return result
