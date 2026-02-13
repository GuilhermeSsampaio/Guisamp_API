from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class RecipeRegister(BaseModel):
    title: str
    content: str
    font: Optional[str] = None
    link: Optional[str] = None


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class RecipeResponse(BaseModel):
    id: int
    title: str
    content: str
    font: str
    link: str
    created_at: datetime
    cookai_user_id: UUID

    # IMPORTANTE: Permite converter objeto do banco direto pra JSON
    model_config = ConfigDict(from_attributes=True)


class ScrappingResponse(BaseModel):
    title: str
    font: str
    link: str
    content: str
