from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class CookAiUserUpdate(BaseModel):
    bios: Optional[str] = None

class CookAiUserResponse(BaseModel):
    id: UUID
    user_id: UUID
    bios: Optional[str] = None
    premium_member: bool

    model_config = ConfigDict(from_attributes=True)