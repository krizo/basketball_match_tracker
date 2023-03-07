import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.players_api import create_player, read_players, read_player, update_player, delete_player
from main import engine, recreate_db
from models.player import Player
from sqlmodel import Session


@pytest.fixture
def player():
    return Player(first_name='Emi', last_name='Name', number=0, id=1)


@pytest.fixture
def player_updated():
    return Player(first_name='Emilia', last_name='Bober', number=5, id=1)


@pytest.fixture
def player_no_last_name():
    return Player(first_name='Emilia', last_name=None, number=5, id=1)


@pytest.fixture
def player_no_first_name():
    return Player(first_name=None, last_name='Bober', number=5, id=1)


@pytest.fixture
def player_no_number():
    return Player(first_name=None, last_name='Bober', number=None, id=1)


def setup_function():
    recreate_db()


def assert_player(actual: Player, expected: Player):
    assert actual.id == expected.id, 'Player Id'
    assert actual.last_name == expected.last_name, 'Player last_name'
    assert actual.first_name == expected.first_name, 'Player first name'
    assert actual.number == expected.number, 'Player number'


def test_player_direct_create(player):
    with Session(engine) as db:
        db.add(player)
        db.commit()
        actual_players = read_players()
        assert actual_players, "No players have been persisted"
        assert_player(actual_players[0], player)


def test_player_create_api_no_last_name(player_no_last_name):
    with pytest.raises(ValidationError):
        create_player(player_no_last_name)


def test_player_create_api_no_first_name(player_no_first_name):
    create_player(player_no_first_name)


def test_player_create_api_no_number(player_no_number):
    create_player(player_no_number)


def test_player_create_api(player):
    created_player = create_player(player)
    players_by_id = read_player(created_player.id)
    assert_player(players_by_id, created_player)


def test_player_update_api(player, player_updated):
    create_player(player)
    updated_player = update_player(player_id=player.id, player=player_updated)
    actual_player = read_player(player.id)
    assert_player(actual_player, updated_player)


def test_player_not_existing():
    with pytest.raises(HTTPException):
        read_player(666)


def test_player_delete_api(player):
    player = create_player(player)
    response = delete_player(player.id)
    assert response.get('ok')
    with pytest.raises(HTTPException):
        read_player(player.id)

