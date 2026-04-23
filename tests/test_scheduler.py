"""Tests for GameNightScheduler.

These tests serve as the spec for the demo's conflict resolution.
After resolving the conflict in scheduler.py, all 6 tests should pass.
"""

import pytest
from datetime import date
from scheduler import GameNightScheduler


# ── Basic functionality (pass on main) ──────────────────────────────────────

def test_add_game():
    s = GameNightScheduler("Jordan")
    s.add_game("Catan")
    assert "Catan" in s.get_games()


def test_build_schedule_cycles_through_games():
    s = GameNightScheduler("Jordan")
    s.add_game("Catan")
    s.add_game("Ticket to Ride")
    schedule = s.build_schedule(4, start_date=date(2025, 9, 5))

    assert schedule[0]["game"] == "Catan"
    assert schedule[1]["game"] == "Ticket to Ride"
    assert schedule[2]["game"] == "Catan"
    assert schedule[3]["game"] == "Ticket to Ride"


def test_build_schedule_raises_with_no_games():
    s = GameNightScheduler("Jordan")
    with pytest.raises(ValueError, match="No games in rotation"):
        s.build_schedule(3)


# ── feature/dedup-games (passes after conflict resolution) ──────────────────

def test_add_game_skips_duplicates():
    s = GameNightScheduler("Jordan")
    s.add_game("Catan")
    s.add_game("Catan")
    s.add_game("Codenames")
    assert s.get_games() == ["Catan", "Codenames"]
    assert s.get_games().count("Catan") == 1


# ── feature/random-picker (passes after conflict resolution) ────────────────

def test_pick_random_returns_a_game_from_rotation():
    s = GameNightScheduler("Jordan")
    s.add_game("Catan")
    s.add_game("Codenames")
    s.add_game("Pandemic")
    result = s.pick_random()
    assert result in ["Catan", "Codenames", "Pandemic"]


def test_pick_random_returns_none_when_rotation_is_empty():
    s = GameNightScheduler("Jordan")
    assert s.pick_random() is None
