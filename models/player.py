from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from models.team import Team


class PlayerBase(SQLModel):
    first_name: Optional[str] = Field(index=True)
    last_name: str = Field(default=None, index=True)
    number: Optional[int]
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Player(PlayerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    team: Optional[Team] = Relationship(back_populates="players", sa_relationship_kwargs={"lazy": 'subquery'})


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(Player):
    pass


class PlayerUpdate(Player):
    pass
