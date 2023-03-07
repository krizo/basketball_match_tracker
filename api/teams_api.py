from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from db.database import engine
from models.team import Team, TeamRead, TeamCreate

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/teams/", response_model=TeamRead)
def create_team(team: TeamCreate):
    with Session(engine) as session:
        db_team = Team.from_orm(team)
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        return db_team


@router.get("/teams/", response_model=List[Team])
def read_teams(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        players = session.exec(select(Team).offset(offset).limit(limit)).all()
        return players
