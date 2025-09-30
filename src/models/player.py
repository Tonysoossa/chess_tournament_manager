from dataclasses import dataclass, asdict
from pathlib import Path
import json

short_cut = Path(__file__).resolve().parent.parent.parent
DATA_PATH = short_cut / "data" / "players.json"


@dataclass
class PlayerData:
    name: str
    last_name: str
    birth_date: str
    national_id: str


def load_players() -> list[PlayerData]:
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

    return [PlayerData(**p) for p in data]


def save_player(player: PlayerData) -> bool:
    players = load_players()

    for p in players:
        if p.national_id == player.national_id:
            return False

    players.append(player)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        player_array = [asdict(p) for p in players]
        json.dump(player_array, f, ensure_ascii=False, indent=4)

    return True


def delete_player(national_id: str) -> bool:
    players = load_players()

    new_players = [p for p in players if p.national_id != national_id]

    if len(new_players) == len(players):
        return False

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        new_players_array = [asdict(p) for p in new_players]
        json.dump(new_players_array, f, ensure_ascii=False, indent=4)

    return True