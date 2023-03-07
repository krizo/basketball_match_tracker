import pytest

from api.players_api import create_player, read_players_by_team
from api.teams_api import create_team
from main import recreate_db
from models.player import Player
from models.team import Team


@pytest.fixture
def team():
    return Team(name='Wisła Canpack U-12', id=1)


@pytest.fixture
def player(team):
    return Player(first_name='Emilia', last_name='Bober', number=5, id=1, team_id=team.id)


@pytest.fixture
def second_player(team):
    return Player(first_name='Martyna', last_name='Koszykarska', number=6, id=2, team_id=team.id)


def setup_function():
    recreate_db()


def test_create_team(team):
    create_team(team)


def test_create_player_with_team(team, player):
    create_team(team)
    create_player(player)


def test_get_players_in_team(team, player, second_player):
    create_team(team)
    create_player(player)
    create_player(second_player)
    players_in_team = read_players_by_team(team.id)
    assert len(players_in_team) == 2
    assert player in players_in_team
    assert second_player in players_in_team
