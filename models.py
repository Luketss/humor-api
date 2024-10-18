# models.py
from typing import Optional
from sqlmodel import SQLModel, Field


class UserSchema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field()


class HumorSchema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    humor_range: int = Field()
