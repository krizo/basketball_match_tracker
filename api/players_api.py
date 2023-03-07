from typing import List

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from sqlmodel import Session, select

from db.database import engine
from models.player import Player, PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(prefix="/players",
                   tags=["players"],
                   responses={404: {"description": "Not found"}})


@router.post("/", response_model=Player)
def create_player(player: PlayerCreate):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player


@router.get("/", response_model=List[PlayerRead])
def read_players(offset: int = 0, limit: int = 100):
    with Session(engine) as session:
        return session.exec(select(Player).offset(offset).limit(limit)).all()


@router.get("{player_id}", response_model=PlayerRead)
def read_player(player_id: int):
    with Session(engine) as session:
        player = session.get(Player, player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player


@router.patch("{player_id}", response_model=PlayerRead)
def update_player(player_id: int, player: PlayerUpdate):
    with Session(engine) as session:
        db_player = read_player(player_id)
        player_data = player.dict(exclude_unset=True)
        for key, value in player_data.items():
            setattr(db_player, key, value)
        session.add(db_player)
        session.commit()
        session.refresh(db_player)
        return db_player


@router.delete("{player_id}")
def delete_player(player_id: int):
    with Session(engine) as session:
        player = session.get(Player, player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        session.delete(player)
        session.commit()
        return {"ok": True}


@router.get("")
def read_players_by_team(team_id: int):
    with Session(engine) as session:
        return session.exec(select(Player).where(text(f"team_id={team_id}"))).all()
