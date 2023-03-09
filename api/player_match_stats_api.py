from fastapi import APIRouter
from sqlalchemy import text
from sqlmodel import select
from api.base_api import create_record, read_record, update_record
from db.database import DbConnection
from models.player_match_stats import PlayerMatchStats
from utils.numbers_utils import get_percentage

router = APIRouter(responses={404: {"description": "Not found"}})


@router.post("/match_stats/", response_model=PlayerMatchStats)
def create_match_stats(match_stats: PlayerMatchStats):
    return create_record(model_class=PlayerMatchStats, data=match_stats)


@router.patch("/match_stats/", response_model=PlayerMatchStats)
def update_match_stats(match_stats_id: int, match_stats: PlayerMatchStats):
    return update_record(model_class=PlayerMatchStats, update_data=match_stats, record_id=match_stats_id)


@router.get("/match_stats/{team_id}", response_model=PlayerMatchStats)
def read_match_stats(match_stats_id: int):
    return read_record(model_class=PlayerMatchStats, record_id=match_stats_id)


def select_stats_for_player_in_match(match_id: int, player_id: int):
    session = DbConnection().get_db()
    return session.exec(
        select(PlayerMatchStats).where(text(f"player_id={player_id} and match_id={match_id}"))).one()


def get_metric(metric: str, match_id: int, player_id: int):
    stats = select_stats_for_player_in_match(match_id=match_id, player_id=player_id).dict()
    return stats.get(metric)


def get_scores_2pts_percentage(match_id: int, player_id: int):
    attempts_2pts = get_metric(metric=PlayerMatchStats.attempts_2pts.key, match_id=match_id, player_id=player_id)
    scored_2pts = get_metric(metric=PlayerMatchStats.scored_2pts.key, match_id=match_id, player_id=player_id)
    return get_percentage(scored_2pts, attempts_2pts)
