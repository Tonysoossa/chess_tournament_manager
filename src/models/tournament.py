from dataclasses import dataclass


@dataclass
class TournamentData:
    nam: str
    area: str
    start_date: str
    end_date: str
    rounds: int = 4
    rounds_index: int
    rounds_list: list
    registered_players: list
    description: str
