from models.player import load_players
from models.round import Round
from models.match import MatchData
from models.gestionPlayer import gestion_player
import os
import json
from pathlib import Path


def round_with_matches():
    """Test : créer un round avec des matchs depuis le JSON"""
    players = load_players("data/players.json")

    m1 = MatchData(players[0].name, players[1].name)
    m1.j1_win()

    m2 = MatchData(players[2].name, players[3].name)
    m2.draw()

    m3 = MatchData(players[4].name, players[1].name)
    m3.j2_win()
    m4 = MatchData(players[2].name, players[3].name)
    m4.draw()
    m5 = MatchData(players[2].name, players[4].name)
    m5.j1_win()
    m6 = MatchData(players[3].name, players[0].name)
    m6.j2_win()

    round1 = Round("Round 1")
    round1.add_match(m1.to_tuple())
    round1.add_match(m2.to_tuple())
    round1.matchDone()

    round2 = Round("Round 2")
    round2.add_match(m3.to_tuple())
    round2.add_match(m4.to_tuple())
    round2.add_match(m5.to_tuple())
    round2.add_match(m6.to_tuple())
    round2.matchDone()

    print(round1)
    print(round2)


def main(base_dir="../data"):
    os.makedirs(base_dir, exist_ok=True)

    files = ["players.json", "tournaments.json"]

    for filename in files:
        filepath = Path(base_dir) / filename

        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # round_with_matches()
    main()
    gestion_player()
