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


    def validate_and_format_id(self, national_id: str) -> str:
        """Valide et formate l'ID national."""
        national_id = national_id.strip()

        if len(national_id) != 7:
            raise ValueError(f"ID invalide '{national_id}' : doit contenir exactement 7 caractères")

        letters = national_id[:2].upper()
        digits = national_id[2:]

        if not letters.isalpha() or not digits.isdigit():
            raise ValueError(f"Format invalide '{national_id}' : 2 lettres suivies de 5 chiffres")

        return letters + digits


    def format_date(self, input_date: str) -> str:
        """Transforme une date YYYYMMDD en YYYY/MM/DD"""
        if len(input_date) == 8 and input_date.isdigit():
            return f"{input_date[:4]}/{input_date[4:6]}/{input_date[6:]}"
        raise ValueError("Date invalide, utilisez le format YYYYMMDD")


    def initialize_scores(self, tournament: TournamentData):
        """Initialise les scores de tous les joueurs à 0."""
        for player in tournament.registered_players:
            tournament.player_scores[player.national_id] = 0.0


    def update_scores(self, tournament: TournamentData, match_tuple):
        """Met à jour les scores après un match."""
        j1_name = match_tuple[0][0]
        j1_score = match_tuple[0][1]
        j2_name = match_tuple[1][0]
        j2_score = match_tuple[1][1]

        # Trouver les national_id correspondants
        for player in tournament.registered_players:
            if player.name == j1_name:
                tournament.player_scores[player.national_id] += j1_score
            elif player.name == j2_name:
                tournament.player_scores[player.national_id] += j2_score


    def get_tournament_winners(self, tournament: TournamentData) -> list[tuple[str, str, float]]:
        """Retourne la liste des gagnants (gère les ex aequo)."""
        if not tournament.player_scores:
            return []

        # Trouver le score maximum
        max_score = max(tournament.player_scores.values())

        # Trouver tous les joueurs avec ce score
        winners = []
        for player in tournament.registered_players:
            if tournament.player_scores.get(player.national_id) == max_score:
                winners.append((
                    f"{player.name} {player.last_name}",
                    player.national_id,
                    max_score
                ))

        return winners


    def select_players_for_tournament(self) -> list[PlayerData] | None:
        """Permet à l'utilisateur de choisir les joueurs via national_id avec gestion d'erreurs."""
        while True:
            try:
                all_players = load_players()

                if not all_players:
                    self.view.show_error("Aucun joueur disponible. Veuillez d'abord créer des joueurs.")
                    return []

                self.view.show_available_players(all_players)
                chosen_ids_input = self.view.get_player_ids()
                chosen_ids_raw = [x.strip() for x in chosen_ids_input.split(",")]

                # Valider tous les IDs avant de continuer
                validated_ids = []
                for id_raw in chosen_ids_raw:
                    try:
                        validated_id = self.validate_and_format_id(id_raw)
                        validated_ids.append(validated_id)
                    except ValueError as e:
                        self.view.show_error(str(e))
                        raise ValueError("Un ou plusieurs IDs sont invalides")

                # Récupérer les joueurs correspondants
                registered = []
                for p in all_players:
                    if p.national_id.upper() in [vid.upper() for vid in validated_ids]:
                        registered.append(p)

                if len(registered) < 2:
                    self.view.show_error("Il faut au moins 2 joueurs pour un tournoi.")
                    retry = self.view.ask_retry()
                    if retry != 'o':
                        return []
                    continue

                self.view.show_registered_players(registered)
                return registered

            except ValueError as e:
                self.view.show_error(str(e))
                retry = self.view.ask_retry()
                if retry != 'o':
                    return []
            except Exception as e:
                self.view.show_error(f"Erreur lors de la sélection : {e}")
                retry = self.view.ask_retry()
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
            pair_key = tuple(sorted([p1.national_id, p2.national_id]))
            if pair_key not in used_pairs:
                used_pairs.add(pair_key)

                while True:
                    try:
                        match = MatchData(p1.name, p2.name)
                        self.view.show_match(p1.name, p2.name)

                        choix = self.view.get_match_result()

                        if choix == "1":
                            match.j1_win()
                            match_tuple = match.to_tuple()
                            round_obj.add_match(match_tuple)
                            self.update_scores(data, match_tuple)
                            break
                        elif choix == "2":
                            match.j2_win()
                            match_tuple = match.to_tuple()
                            round_obj.add_match(match_tuple)
                            self.update_scores(data, match_tuple)
                            break
                        elif choix == "3":
                            match.draw()
                            match_tuple = match.to_tuple()
                            round_obj.add_match(match_tuple)
                            self.update_scores(data, match_tuple)
                            break
                        else:
                            self.view.show_error("Résultat invalide. Choisissez 1, 2 ou 3.")

                    except Exception as e:
                        self.view.show_error(f"Erreur lors de la saisie : {e}")
                        retry = self.view.ask_retry_match()
                        if retry != 'o':
                            break

        round_obj.matchDone()
        data.rounds_list.append(round_obj)

        # Afficher le résumé du round
        self.view.show_round_summary(round_obj.name, round_obj.matchs)
        self.view.show_scores(data.player_scores, data.registered_players)


    def simulate_tournament_manual(self, data: TournamentData):
        """Simule tous les rounds du tournoi avec résultats manuels."""
        # Initialiser les scores
        self.initialize_scores(data)

        for r in range(1, data.rounds + 1):
            self.view.show_round_header(r, data.rounds)
            self.simulate_round_manual(data, r)

            if r < data.rounds:
                continuer = self.view.ask_continue_next_round()
                if continuer != 'o':
                    self.view.show_info("Tournoi interrompu.")
                    return False

        # Déterminer le(s) gagnant(s) du tournoi
        winners = self.get_tournament_winners(data)

        # Construire la chaîne pour tournament_winner
        if len(winners) == 1:
            winner_name, winner_id, _ = winners[0]
            data.tournament_winner = f"{winner_name} ({winner_id})"
        else:
            # Format pour ex aequo : "Name1 (ID1), Name2 (ID2)"
            winner_strings = [f"{name} ({wid})" for name, wid, _ in winners]
            data.tournament_winner = ", ".join(winner_strings)

        # Afficher le(s) gagnant(s) du tournoi
        self.view.show_tournament_winners(winners)

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
                retry = self.view.ask_retry()
                if retry != 'o':
                    return
            except Exception as e:
                self.view.show_error(f"Erreur inattendue : {e}")
                retry = self.view.ask_retry()
                if retry != 'o':
                    return