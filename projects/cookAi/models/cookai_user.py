from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from auth.models.user import User
    from cookAi.models.recipe import Recipe


class CookAiUser(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    bios: Optional[str] | None
    premium_member: Optional[bool] = Field(default=False)
    recipes: list["Recipe"] = Relationship(back_populates="cookai_user")

    user: "User" = Relationship(sa_relationship_kwargs={"uselist": False})
