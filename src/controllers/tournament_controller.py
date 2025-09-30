from itertools import combinations
from random import shuffle
from models.player import load_players, PlayerData
from models.tournament import TournamentData, save_tournament
from models.round import Round
from models.match import MatchData
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self):
        self.view = TournamentView()

    def format_date(self, input_date: str) -> str:
        """Transforme une date YYYYMMDD en YYYY/MM/DD"""
        if len(input_date) == 8 and input_date.isdigit():
            return f"{input_date[:4]}/{input_date[4:6]}/{input_date[6:]}"
        raise ValueError("Date invalide, utilisez le format YYYYMMDD")

    def select_players_for_tournament(self) -> list[PlayerData]:
        """Permet à l'utilisateur de choisir les joueurs via nationalId avec gestion d'erreurs."""
        while True:
            try:
                all_players = load_players()

                if not all_players:
                    self.view.show_error("Aucun joueur disponible. Veuillez d'abord créer des joueurs.")
                    return []

                self.view.show_available_players(all_players)
                chosen_ids = self.view.get_player_ids()
                chosen_ids = [x.strip().upper() for x in chosen_ids.split(",")]

                registered = []
                for p in all_players:
                    if p.nationalId.upper() in chosen_ids:
                        registered.append(p)

                if len(registered) < 2:
                    self.view.show_error("Il faut au moins 2 joueurs pour un tournoi.")
                    retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                    if retry != 'o':
                        return []
                    continue

                self.view.show_registered_players(registered)
                return registered

            except Exception as e:
                self.view.show_error(f"Erreur lors de la sélection : {e}")
                retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                if retry != 'o':
                    return []

    def players_pairs(self, players: list):
        """Retourne toutes les paires possibles de joueurs."""
        return list(combinations(players, 2))

    def simulate_round_manual(self, data: TournamentData, round_number: int):
        """Crée un round avec tous les joueurs se rencontrant une seule fois."""
        players = data.registered_players.copy()
        shuffle(players)

        all_pairs = self.players_pairs(players)
        round_obj = Round(f"Round {round_number}")
        used_pairs = set()

        for p1, p2 in all_pairs:
            pair_key = tuple(sorted([p1.nationalId, p2.nationalId]))
            if pair_key not in used_pairs:
                used_pairs.add(pair_key)

                while True:
                    try:
                        match = MatchData(p1.name, p2.name)
                        self.view.show_match(p1.name, p2.name)

                        choix = self.view.get_match_result()

                        if choix == "1":
                            match.j1_win()
                            round_obj.add_match(match.to_tuple())
                            break
                        elif choix == "2":
                            match.j2_win()
                            round_obj.add_match(match.to_tuple())
                            break
                        elif choix == "3":
                            match.draw()
                            round_obj.add_match(match.to_tuple())
                            break
                        else:
                            self.view.show_error("Résultat invalide. Choisissez 1, 2 ou 3.")

                    except Exception as e:
                        self.view.show_error(f"Erreur lors de la saisie : {e}")
                        retry = input("Voulez-vous réessayer ce match ? (o/n) : ").strip().lower()
                        if retry != 'o':
                            break

        round_obj.matchDone()
        data.rounds_list.append(round_obj)
        self.view.show_round_summary(round_obj.name, round_obj.matchs)

    def simulate_tournament_manual(self, data: TournamentData):
        """Simule tous les rounds du tournoi avec résultats manuels."""
        for r in range(1, data.rounds + 1):
            print(f"\n{'=' * 50}")
            print(f"Round {r}/{data.rounds}")
            print(f"{'=' * 50}")
            self.simulate_round_manual(data, r)

            if r < data.rounds:
                continuer = input("\nContinuer au round suivant ? (o/n) : ").strip().lower()
                if continuer != 'o':
                    self.view.show_info("Tournoi interrompu.")
                    return False
        return True

    def create_tournament(self):
        """Fonction principale pour créer et simuler un tournoi avec gestion d'erreurs."""
        while True:
            try:
                self.view.show_tournament_creation_header()

                name, area, start_date, end_date, rounds_str, description = self.view.get_tournament_info()

                # Validation des dates
                start_date = self.format_date(start_date)
                end_date = self.format_date(end_date)

                # Validation du nombre de rounds
                rounds = int(rounds_str) if rounds_str.isdigit() and int(rounds_str) > 0 else 4

                # Sélection des joueurs
                registered_players = self.select_players_for_tournament()

                if not registered_players:
                    self.view.show_info("Retour au menu principal.")
                    return

                tournament = TournamentData(
                    name=name,
                    area=area,
                    start_date=start_date,
                    end_date=end_date,
                    rounds=rounds,
                    description=description,
                    registered_players=registered_players,
                )

                # Simulation du tournoi
                completed = self.simulate_tournament_manual(tournament)

                if completed:
                    save_tournament(tournament)
                    self.view.show_tournament_saved(tournament.name)

                return

            except ValueError as e:
                self.view.show_error(str(e))
                retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                if retry != 'o':
                    return
            except Exception as e:
                self.view.show_error(f"Erreur inattendue : {e}")
                retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                if retry != 'o':
                    return