import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from itertools import combinations
from random import shuffle
from models.player import load_players, PlayerData
from models.round import Round
from models.match import MatchData

TOURNAMENTS_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "tournaments.json"
)


def format_date(input_date: str) -> str:
    """
    Transforme une date YYYYMMDD en YYYY/MM/DD
    """
    if len(input_date) == 8 and input_date.isdigit():
        return f"{input_date[:4]}/{input_date[4:6]}/{input_date[6:]}"
    return input_date


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


def select_players_for_tournament() -> list[PlayerData]:
    """Permet à l'utilisateur de choisir les joueurs via nationalId."""
    all_players = load_players()
    print("\nListe des joueurs disponibles :")
    for p in all_players:
        print(f"- {p.name} {p.lastName} ({p.nationalId})")

    chosen_ids = input(
        "\nEntrez les ID des joueurs à inscrire, séparés par des virgules : "
    )
    chosen_ids = [x.strip().upper() for x in chosen_ids.split(",")]

    registered = []
    for p in all_players:
        if p.nationalId.upper() in chosen_ids:
            registered.append(p)

    message = [p.name + " " + p.lastName for p in registered]
    print(f"\n✅ Joueurs inscrits : {message}")
    return registered


def players_pairs(players: list):
    """Retourne toutes les paires possibles de joueurs."""
    return list(combinations(players, 2))


def simulate_round_manual(data: TournamentData, round_number: int):
    """
    Crée un round avec tous les joueurs se rencontrant une seule fois.
    Les résultats sont saisis manuellement.
    """
    players = data.registered_players.copy()
    shuffle(players)

    all_pairs = players_pairs(players)
    round_obj = Round(f"Round {round_number}")
    used_pairs = set()

    for p1, p2 in all_pairs:
        pair_key = tuple(sorted([p1.nationalId, p2.nationalId]))
        if pair_key not in used_pairs:
            used_pairs.add(pair_key)

            match = MatchData(p1.name, p2.name)

            print(f"\nMatch : {p1.name} vs {p2.name}")
            print(
                "Entrez le résultat :\n"
                f"1 = {p1.name} gagne\n"
                f"2 = {p2.name} gagne\n"
                "3 = nul"
            )

            choix = input("Résultat : ").strip()
            if choix == "1":
                match.j1_win()
            elif choix == "2":
                match.j2_win()
            elif choix == "3":
                match.draw()
            else:
                print("❌ Résultat invalide, match annulé")
                continue

            round_obj.add_match(match.to_tuple())

    round_obj.matchDone()
    data.rounds_list.append(round_obj)

    print(f"\n=== {round_obj.name} terminé ===")
    for m in round_obj.matchs:
        print(f"- {m[0][0]} ({m[0][1]}) vs {m[1][0]} ({m[1][1]})")


def simulate_tournament_manual(data: TournamentData):
    """Simule tous les rounds du tournoi avec résultats manuels."""
    for r in range(1, data.rounds + 1):
        simulate_round_manual(data, r)


def save_tournament(data: TournamentData):
    """Sauvegarde le tournoi dans data/tournaments.json sans rounds_index."""
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


def gestion_tournament():
    """Fonction principale pour créer et simuler un tournoi."""
    print("=== Création d'un nouveau tournoi ===")
    name = input("Nom du tournoi : ").strip()
    area = input("Lieu / Zone : ").strip()
    start_date = format_date(input("Date de début (YYYYMMDD) : ").strip())
    end_date = format_date(input("Date de fin (YYYYMMDD) : ").strip())
    rounds_str = input("Nombre de rounds (par défaut 4) : ").strip()
    description = input("Description (optionnelle) : ").strip()
    rounds = int(rounds_str) if rounds_str.isdigit() else 4

    tournament = TournamentData(
        name=name,
        area=area,
        start_date=start_date,
        end_date=end_date,
        rounds=rounds,
        description=description,
        registered_players=select_players_for_tournament(),
    )

    simulate_tournament_manual(tournament)
    save_tournament(tournament)
    print(f"\n✅ Tournoi '{tournament.name}' sauvegardé avec succès !")
