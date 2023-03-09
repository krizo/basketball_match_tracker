from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from sqlmodel import Session, select

from api.base_api import create_record, read_record, update_record, delete_record
from db.database import engine, DbConnection
from models.player import Player, PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/players/", response_model=Player)
def create_player(player: PlayerCreate):
    return create_record(Player, player)


@router.get("/players/", response_model=List[PlayerRead])
def read_players(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(Player).offset(offset).limit(limit)).all()


@router.get("/players/{player_id}", response_model=PlayerRead)
def read_player(player_id: int):
    return read_record(Player, player_id)


@router.patch("/players/{player_id}", response_model=PlayerUpdate)
def update_player(player_id: int, player: Player):
    return update_record(model_class=Player, update_data=player, record_id=player.id)


@router.delete("/players/{player_id}")
def delete_player(player_id: int):
    return delete_record(model_class=Player, record_id=player_id)


@router.get("/players/")
def read_players_by_team(team_id: int):
    session = DbConnection().get_db()
    return session.exec(select(Player).where(text(f"team_id={team_id}"))).all()
