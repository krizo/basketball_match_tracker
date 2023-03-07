from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    players: List["Player"] = Relationship(back_populates="team")
