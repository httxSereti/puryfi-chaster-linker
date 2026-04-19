from pydantic import BaseModel, ConfigDict


class ChasterExtensionSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    is_linked: bool
    link_token: str | None = None