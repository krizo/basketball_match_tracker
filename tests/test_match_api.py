import datetime
import pytest
from fastapi import HTTPException

from api.matches_api import create_match, read_match, update_match, delete_match, read_latest_matches_by_home_team_id, \
    read_matches
from main import recreate_db
from models.match import Match
from models.team import Team


@pytest.fixture
def home_team():
    return Team(name='Wisła Canpack U-12', id=1)


@pytest.fixture
def away_team():
    return Team(name='Ślęza Wrocław', id=2)


@pytest.fixture
def match(home_team, away_team):
    return Match(home_team_id=home_team.id, away_team_id=away_team.id, timestamp=datetime.datetime.now(),
                 home_score=100, away_score=0, id=1)


@pytest.fixture
def match_2(home_team, away_team):
    return Match(home_team_id=home_team.id, away_team_id=away_team.id, timestamp=datetime.datetime.now(),
                 home_score=0, away_score=0, id=2)


@pytest.fixture
def match_updated():
    return Match(home_team_id=5, away_team_id=6, timestamp=datetime.datetime.now(), home_score=99, away_score=3, id=1)


def setup_function():
    recreate_db()


def test_create_read_match(match):
    match_create = create_match(match)
    assert match_create, match
    match_read = read_match(match_id=match_create.id)
    assert match_read, match


def test_create_update_match(match, match_updated):
    match_create = create_match(match)
    update_match(match_id=match_create.id, match=match_updated)
    match_read = read_match(match_id=match_updated.id)
    assert match_read == match_updated


def test_create_delete_match(match):
    match_create = create_match(match)
    delete_match(match_id=match_create.id)
    with pytest.raises(HTTPException):
        read_match(match_id=match_create.id)


def test_create_read_match_by_home_team(match, home_team):
    create_match(match)
    match_by_home_team = read_latest_matches_by_home_team_id(home_team_id=match.home_team_id)
    assert match_by_home_team == match


def test_create_read_matches(match, match_2):
    create_match(match)
    create_match(match_2)
    matches = read_matches()
    assert len(matches) == 2
    assert match in matches
    assert match_2 in matches
