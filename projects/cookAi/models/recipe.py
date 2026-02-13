from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from uuid import UUID

if TYPE_CHECKING:
    from projects.cookAi.models.cookai_user import CookAiUser

class Recipe(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    font:str
    link:str
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    cookai_user_id: UUID = Field(foreign_key="cookaiuser.id")
    
    cookai_user: Optional["CookAiUser"] = Relationship(back_populates="recipes")