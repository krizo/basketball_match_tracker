from typing import List

from fastapi import APIRouter
from sqlalchemy import text
from sqlmodel import Session, select

from api.base_api import create_record, read_record, update_record, delete_record
from db.database import engine, DbConnection
from models.match import Match

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/", response_model=Match)
def create_match(match: Match):
    return create_record(Match, match)


@router.get("/match/", response_model=List[Match])
def read_matches(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(Match).offset(offset).limit(limit)).all()


@router.get("/match/{match_id}", response_model=Match)
def read_match(match_id: int):
    return read_record(Match, match_id)


@router.patch("/match/{match_id}", response_model=Match)
def update_match(match_id: int, match: Match):
    return update_record(model_class=Match, update_data=match, record_id=match_id)


@router.delete("/match/{match_id}")
def delete_match(match_id: int):
    return delete_record(model_class=Match, record_id=match_id)


@router.get("/match/")
def read_latest_matches_by_home_team_id(home_team_id: int, limit: int = 10):
    session = DbConnection().get_db()
    return session.exec(
        select(Match).where(text(f"home_team_id={home_team_id}")).limit(limit).order_by(Match.id.desc())).one()
