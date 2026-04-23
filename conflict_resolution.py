"""
INSTRUCTOR REFERENCE — DO NOT COMMIT TO ANY BRANCH
===================================================
This file shows the correct resolved version of scheduler.py after the demo conflict.

The conflict is in add_game(). Here is what each branch was trying to do:

  feature/dedup-games:   added a duplicate check before appending
  feature/random-picker: added random.shuffle() after appending, plus a pick_random() method

The resolution: keep the dedup check, keep pick_random(), DROP the shuffle.

Why drop the shuffle?
  Shuffling on every add_game() call changes the rotation order unpredictably —
  that's a side effect no caller would expect from a method named "add_game".
  Randomness belongs in pick_random(), where the caller is explicitly asking for it.
  This preserves both intents without the unexpected side effect.

After resolving, all 6 tests in tests/test_scheduler.py should pass.
"""

import random
from datetime import date, timedelta


class GameNightScheduler:
    def __init__(self, host: str):
        self.host = host
        self.games: list[str] = []
        self.schedule: list[dict] = []

    def add_game(self, game: str) -> None:
        """Add a game to the rotation. Skips duplicates."""
        # ✓ from feature/dedup-games: prevents duplicates cluttering the rotation
        if game not in self.games:
            self.games.append(game)
        # ✗ NOT included: random.shuffle(self.games) from feature/random-picker
        #   Shuffling on add is a side effect the caller doesn't expect.
        #   Randomness is handled by pick_random() below.

    def get_games(self) -> list[str]:
        """Return the current game list."""
        return self.games.copy()

    def pick_random(self) -> str | None:
        """Pick a random game from the rotation.

        ✓ from feature/random-picker: lets the group pick spontaneously
        without committing to the full rotation order.
        """
        return random.choice(self.games) if self.games else None

    def build_schedule(self, weeks: int, start_date: date = None) -> list[dict]:
        """Build a weekly schedule cycling through the game rotation."""
        if not self.games:
            raise ValueError("No games in rotation. Add at least one game before building a schedule.")
        if start_date is None:
            start_date = date.today()

        self.schedule = []
        for i in range(weeks):
            week_date = start_date + timedelta(weeks=i)
            self.schedule.append({
                "week": i + 1,
                "date": week_date.isoformat(),
                "game": self.games[i % len(self.games)],
                "host": self.host,
            })
        return self.schedule

    def get_schedule(self) -> list[dict]:
        """Return the current schedule."""
        return self.schedule.copy()

    def summary(self) -> str:
        """Return a readable summary of the current rotation and schedule."""
        if not self.games:
            return f"Host: {self.host} | No games in rotation yet."
        game_list = ", ".join(self.games)
        weeks_planned = len(self.schedule)
        return (
            f"Host: {self.host}\n"
            f"Games in rotation ({len(self.games)}): {game_list}\n"
            f"Weeks scheduled: {weeks_planned}"
        )
