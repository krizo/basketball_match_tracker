from typing import Optional, List

from pydantic import root_validator
from sqlmodel import SQLModel, Field, JSON, Column
from datetime import datetime


class PlayerMatchStatsMetrics(SQLModel):
    attempts_1pts: Optional[int] = 0
    attempts_2pts: Optional[int] = 0
    attempts_3pts: Optional[int] = 0
    scored_1pts: Optional[int] = 0
    scored_2pts: Optional[int] = 0
    scored_3pts: Optional[int] = 0
    rebounds_defensive: Optional[int] = 0
    rebounds_offensive: Optional[int] = 0
    assists: Optional[int] = 0
    steals: Optional[int] = 0
    blocks: Optional[int] = 0
    turnovers: Optional[int] = 0
    fouls: Optional[int] = 0

    @root_validator
    def check_attempts_greater_than_scores(cls, metrics):
        for points in [1, 2, 3]:
            attempts, scores = metrics.get(f'attempts_{points}pts'), metrics.get(f'scored_{points}pts')
            assert attempts >= scores, \
                f"'attempts_{points}pts' value {attempts} needs to be greater or equal than 'scored_{points}pts' ({scores})."
        return metrics


class PlayerMatchStats(PlayerMatchStatsMetrics, table=True):
    __tablename__ = "player_match_stats"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    match_id: Optional[int] = Field(nullable=False, foreign_key="match.id", index=True)
    player_id: Optional[int] = Field(nullable=False, foreign_key="player.id", index=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
