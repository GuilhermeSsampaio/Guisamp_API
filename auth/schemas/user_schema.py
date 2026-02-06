from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from pydantic import EmailStr

class UserResponse(SQLModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime