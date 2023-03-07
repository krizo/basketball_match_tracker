from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from db.database import engine
from models.team import Team

router = APIRouter(prefix="/teams",
                   tags=["teams"],
                   responses={404: {"description": "Not found"}})


@router.post("/", response_model=Team)
def create_team(team: Team):
    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team


@router.get("/", response_model=List[Team])
def read_teams(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        players = session.exec(select(Team).offset(offset).limit(limit)).all()
        return players
