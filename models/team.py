from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class TeamBase(SQLModel):
    name: str = Field(index=True)


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    players: List["Player"] = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": 'subquery'})


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int
