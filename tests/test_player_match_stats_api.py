import datetime

import pytest

from api.matches_api import create_match
from api.player_match_stats_api import create_match_stats, read_match_stats, update_match_stats, \
    get_scores_2pts_percentage, select_stats_for_player_in_match, get_scores_3pts_percentage, get_metric
from main import recreate_db
from models.match import Match
from models.player import Player
from models.player_match_stats import PlayerMatchStats, PlayerMatchStatsMetrics
from models.team import Team
from utils.numbers_utils import get_percentage


@pytest.fixture
def team():
    return Team(name='Wisła Canpack U-12', id=1)


@pytest.fixture
def player_1(team):
    return Player(first_name='Emilia', last_name='Bober', number=5, id=1, team_id=team.id)


@pytest.fixture
def player_2(team):
    return Player(first_name='Martyna', last_name='Koszykarska', number=7, id=2, team_id=team.id)


@pytest.fixture
def away_team():
    return Team(name='Ślęza Wrocław', id=2)


@pytest.fixture
def match(team, away_team):
    return create_match(Match(home_team_id=team.id, away_team_id=away_team.id, timestamp=datetime.datetime.now()))


@pytest.fixture
def player_match_stats(player_1, team, match):
    return PlayerMatchStats(id=1, player_id=player_1.id, match_id=match.id)


@pytest.fixture
def player_1_match_stats_metrics(player_1, team, match):
    return PlayerMatchStats(id=1, player_id=player_1.id, match_id=match.id, attempts_2pts=7, attempts_3pts=7,
                            attempts_1pts=1, scored_1pts=1, scored_2pts=5, scored_3pts=1, rebounds_defensive=10,
                            rebounds_offensive=3, assists=14, steals=3, blocks=2, turnovers=2, fouls=6,
                            changed_in=[0, 600, 1200], changed_out=[300, 900, 1800])


@pytest.fixture
def player_2_match_stats_metrics(player_2, match):
    return PlayerMatchStats(id=2, player_id=player_2.id, match_id=match.id, attempts_1pts=6, scored_1pts=6,
                            attempts_2pts=6, attempts_3pts=0, scored_2pts=4, scored_3pts=0, rebounds_defensive=3,
                            rebounds_offensive=1, assists=2, steals=1, blocks=0, turnovers=6, fouls=2,
                            changed_in=[0, 200, 400], changed_out=[100, 17000, 1800])


@pytest.fixture
def match_stats_metrics_attempts_greater_than_scores(player_2, match):
    return PlayerMatchStats(id=2, player_id=player_2.id, match_id=match.id, attempts_1pts=1, scored_1pts=2,
                            scored_2pts=-1, attempts_2pts=0, attempts_3pts=0, scored_3pts=0, )


def setup_function():
    recreate_db()


def test_player_match_stats_create_read_api(player_match_stats):
    create_match_stats(match_stats=player_match_stats)
    stats_db = read_match_stats(match_stats_id=player_match_stats.id)
    assert stats_db == player_match_stats


def test_player_match_stats_update_read_api(player_match_stats, player_1_match_stats_metrics):
    create_match_stats(match_stats=player_match_stats)
    updated_stats = update_match_stats(match_stats=player_1_match_stats_metrics, match_stats_id=player_match_stats.id)
    stats_db = read_match_stats(match_stats_id=updated_stats.id)
    assert stats_db == player_1_match_stats_metrics


def test_player_1_match_stats_create_api(player_1_match_stats_metrics):
    create_match_stats(match_stats=player_1_match_stats_metrics)
    stats_db = read_match_stats(match_stats_id=player_1_match_stats_metrics.id)
    assert stats_db == player_1_match_stats_metrics


def test_player_2_match_stats_create_api(player_2_match_stats_metrics):
    create_match_stats(match_stats=player_2_match_stats_metrics)
    stats_db = read_match_stats(match_stats_id=player_2_match_stats_metrics.id)
    assert stats_db == player_2_match_stats_metrics


def test_select_stats_for_player_in_match(match, player_1, player_1_match_stats_metrics):
    stats = create_match_stats(match_stats=player_1_match_stats_metrics)
    player_stats = select_stats_for_player_in_match(match_id=match.id, player_id=player_1.id)
    assert stats == player_stats


def test_player_match_stats_get_metric(match, player_1, player_1_match_stats_metrics):
    create_match_stats(match_stats=player_1_match_stats_metrics)
    player_stats = select_stats_for_player_in_match(match_id=match.id, player_id=player_1.id)
    metrics = list(PlayerMatchStatsMetrics.dict(player_stats).keys())
    for metric in metrics:
        metric_stats = get_metric(match_id=match.id, player_id=player_1.id, metric=metric)
        assert metric_stats is not None, f"No value for metric {metric}"
        assert metric_stats == player_stats.dict().get(metric)


def test_match_stats_2_pts_percentage(player_1_match_stats_metrics):
    create_match_stats(match_stats=player_1_match_stats_metrics)
    scores_perc = get_scores_2pts_percentage(match_id=player_1_match_stats_metrics.match_id,
                                             player_id=player_1_match_stats_metrics.player_id)
    expected_perc = get_percentage(player_1_match_stats_metrics.scored_2pts, player_1_match_stats_metrics.attempts_2pts)
    assert scores_perc == expected_perc


def test_match_stats_3_pts_percentage(player_1_match_stats_metrics):
    create_match_stats(match_stats=player_1_match_stats_metrics)
    scores_perc = get_scores_3pts_percentage(match_id=player_1_match_stats_metrics.match_id,
                                             player_id=player_1_match_stats_metrics.player_id)
    expected_perc = get_percentage(player_1_match_stats_metrics.scored_3pts, player_1_match_stats_metrics.attempts_3pts)
    assert scores_perc == expected_perc
