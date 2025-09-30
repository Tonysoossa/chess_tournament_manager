import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from models.player import PlayerData

TOURNAMENTS_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "tournaments.json"
)


@dataclass
class TournamentData:
    name: str
    area: str
    start_date: str
    end_date: str
    rounds: int = 4
    rounds_list: list = field(default_factory=list)
    registered_players: list[PlayerData] = field(default_factory=list)
    description: str = ""
    player_scores: dict = field(default_factory=dict)  # {national_id: score}
    tournament_winner: str = ""  # "name (national_id)"


def save_tournament(data: TournamentData):
    """Sauvegarde le tournoi dans data/tournaments.json."""
    if TOURNAMENTS_PATH.exists():
        try:
            with open(TOURNAMENTS_PATH, "r", encoding="utf-8") as f:
                tournaments = json.load(f)
        except json.JSONDecodeError:
            tournaments = []
    else:
        tournaments = []

    tournaments.append(asdict(data))

    with open(TOURNAMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(tournaments, f, ensure_ascii=False, indent=4)