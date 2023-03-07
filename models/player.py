from typing import Optional

from sqlmodel import SQLModel, Field


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = Field(index=True)
    last_name: str
    number: Optional[int]
    # team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class PlayerCreate(SQLModel):
    first_name: Optional[str] = Field(index=True)
    last_name: str
    number: Optional[int]


class PlayerRead(SQLModel):
    id: int
    first_name: Optional[str] = Field(index=True)
    last_name: str
    number: Optional[int]


class PlayerUpdate(SQLModel):
    first_name: Optional[str] = Field(index=True)
    last_name: str
    number: Optional[int]
