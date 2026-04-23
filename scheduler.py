"""Game Night Scheduler — plan and manage your group's weekly game rotation."""

from datetime import date, timedelta


class GameNightScheduler:
    def __init__(self, host: str):
        self.host = host
        self.games: list[str] = []
        self.schedule: list[dict] = []

    def add_game(self, game: str) -> None:
        """Add a game to the rotation."""
        self.games.append(game)

    def get_games(self) -> list[str]:
        """Return the current game list."""
        return self.games.copy()

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
