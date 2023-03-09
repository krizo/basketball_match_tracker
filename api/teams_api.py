from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from api.base_api import create_record, read_record
from db.database import engine
from models.team import Team, TeamRead, TeamCreate

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/teams/", response_model=TeamCreate)
def create_team(team: TeamCreate):
    return create_record(Team, team)


@router.get("/teams/{team_id}", response_model=TeamRead)
def read_team(team_id: int):
    return read_record(Team, team_id)


@router.get("/teams/", response_model=List[Team])
def read_teams(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(Team).offset(offset).limit(limit)).all()
