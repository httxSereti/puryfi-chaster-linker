from pydantic import BaseModel, ConfigDict


class ChasterExtensionSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    is_linked: bool
    link_token: str | None = None
    lock_on_freeze: bool = False
    unlock_on_unfreeze: bool = False
    lock_password: str | None = None