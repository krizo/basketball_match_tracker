from typing import Optional

from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime


class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    home_team_id: Optional[int] = Field(default=None, foreign_key="team.id", index=True)
    away_team_id: Optional[int] = Field(default=None, foreign_key="team.id", index=True)
    home_score: Optional[int]
    away_score: Optional[int]
    created_at: datetime = Field(default=datetime.now())
