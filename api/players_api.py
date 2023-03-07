from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from sqlmodel import Session, select

from db.database import engine, DbConnection
from models.player import Player, PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/", response_model=Player)
def create_player(player: PlayerCreate):
    with Session(engine) as session:
        db_player = Player.from_orm(player)
        session.add(db_player)
        session.commit()
        session.refresh(db_player)
        return db_player


@router.get("/players/", response_model=List[PlayerRead])
def read_players(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(Player).offset(offset).limit(limit)).all()


@router.get("/players/{player_id}", response_model=PlayerRead)
def read_player(player_id: int):
    session = DbConnection().get_db()
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.patch("/players/{player_id}", response_model=PlayerUpdate)
def update_player(player_id: int, player: Player):
    session = DbConnection().get_db()
    db_player = session.get(Player, player_id)
    player_data = player.dict(exclude_unset=True)
    for key, value in player_data.items():
        setattr(db_player, key, value)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


@router.delete("/players/{player_id}")
def delete_player(player_id: int):
    session = DbConnection().get_db()
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    session.delete(player)
    session.commit()
    return {"ok": True}


@router.get("/players/")
def read_players_by_team(team_id: int):
    session = DbConnection().get_db()
    return session.exec(select(Player).where(text(f"team_id={team_id}"))).all()
