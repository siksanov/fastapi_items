import uuid
from sqlmodel import SQLModel, Field, Relationship

from models.user import User


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255,)
    description: str | None = Field(default=None, max_length=255,)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255,)


class Item(ItemBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    owner_id: str = Field(
        foreign_key='user.id', nullable=False, ondelete='CASCADE')
    owner: User | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: str
    owner_id: str


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int
