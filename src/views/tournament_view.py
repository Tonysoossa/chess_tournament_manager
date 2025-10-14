from models.player import PlayerData


class TournamentView:
    @staticmethod
    def show_tournament_creation_header():
        print("\n=== Création d'un nouveau tournoi ===")

    @staticmethod
    def get_tournament_info():
        """Demande les informations du tournoi."""
        name = input("Nom du tournoi : ").strip()
        area = input("Lieu / Zone : ").strip()
        start_date = input("Date de début (YYYYMMDD) : ").strip()
        end_date = input("Date de fin (YYYYMMDD) : ").strip()
        rounds_str = input("Nombre de rounds (par défaut 4) : ").strip()
        description = input("Description (optionnelle) : ").strip()
        return name, area, start_date, end_date, rounds_str, description

    @staticmethod
    def show_available_players(players: list[PlayerData]):
        """Affiche la liste des joueurs disponibles."""
        print("\nListe des joueurs disponibles :")
        for p in players:
            print(f"- {p.name} {p.last_name} ({p.national_id})")

    @staticmethod
    def get_player_ids():
        """Demande les IDs des joueurs à inscrire."""
        return input(
            "\nEntrez les ID des joueurs à inscrire, séparés par des virgules : "
        ).strip()

    @staticmethod
    def show_registered_players(players: list[PlayerData]):
        """Affiche les joueurs inscrits."""
        names = [f"{p.name} {p.last_name}" for p in players]
        print(f"\n✅ Joueurs inscrits : {', '.join(names)}")

    @staticmethod
    def show_match(p1_name: str, p2_name: str, p1_id: str = "", p2_id: str = ""):
        """Affiche les informations d'un match."""
        p1_display = f"{p1_name} ({p1_id})" if p1_id else p1_name
        p2_display = f"{p2_name} ({p2_id})" if p2_id else p2_name
        print(f"\nMatch : {p1_display} vs {p2_display}")
        print("Entrez le résultat :")
        print(f"1 = {p1_display} gagne")
        print(f"2 = {p2_display} gagne")
        print("3 = nul")

    @staticmethod
    def get_match_result():
        """Demande le résultat du match."""
        return input("Résultat (1/2/3) : ").strip()

    @staticmethod
    def show_round_header(round_number: int, total_rounds: int):
        """Affiche l'en-tête du round."""
        print(f"\n{'=' * 50}")
        print(f"Round {round_number}/{total_rounds}")
        print(f"{'=' * 50}")

    @staticmethod
    def show_round_summary(round_name: str, matches: list):
        """Affiche le résumé d'un round."""
        print(f"\n=== {round_name} terminé ===")
        for m in matches:
            # Format: ([j1_id, j1_name, j1_score], [j2_id, j2_name, j2_score])
            j1_id, j1_name, j1_score = m[0][0], m[0][1], m[0][2]
            j2_id, j2_name, j2_score = m[1][0], m[1][1], m[1][2]
            print(
                f"- {j1_name} ({j1_id}) [{j1_score}] vs {j2_name} ({j2_id}) [{j2_score}]"
            )

    @staticmethod
    def show_scores(scores: dict, players: list[PlayerData]):
        """Affiche les scores de tous les joueurs."""
        print("\n📊 Scores actuels :")
        player_map = {p.national_id: p for p in players}

        # Trier par score décroissant
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for idx, (national_id, score) in enumerate(sorted_scores, 1):
            player = player_map.get(national_id)
            if player:
                print(
                    f"{idx}. {player.name} {player.last_name} ({national_id}) - {score} points"
                )

    @staticmethod
    def show_tournament_winners(winners: list[tuple[str, str, float]]):
        """Affiche le(s) gagnant(s) du tournoi."""
        print(f"\n{'=' * 60}")
        if len(winners) == 1:
            print("🏆🏆🏆 GAGNANT DU TOURNOI 🏆🏆🏆")
            winner_name, winner_id, final_score = winners[0]
            print(f"{winner_name} ({winner_id})")
            print(f"Score final : {final_score} points")
        else:
            print("🏆🏆🏆 GAGNANTS DU TOURNOI (EX AEQUO) 🏆🏆🏆")
            for winner_name, winner_id, final_score in winners:
                print(f"- {winner_name} ({winner_id}) - {final_score} points")
        print(f"{'=' * 60}")

    @staticmethod
    def ask_continue_next_round():
        """Demande si l'utilisateur veut continuer au round suivant."""
        return input("\nContinuer au round suivant ? (o/n) : ").strip().lower()

    @staticmethod
    def ask_retry():
        """Demande si l'utilisateur veut réessayer."""
        return input("Voulez-vous réessayer ? (o/n) : ").strip().lower()

    @staticmethod
    def ask_retry_match():
        """Demande si l'utilisateur veut réessayer un match."""
        return input("Voulez-vous réessayer ce match ? (o/n) : ").strip().lower()

    @staticmethod
    def show_tournament_saved(tournament_name: str):
        print(f"\n✅ Tournoi '{tournament_name}' sauvegardé avec succès !")

    @staticmethod
    def show_error(message: str):
        print(f"❌ {message}")

    @staticmethod
    def show_info(message: str):
        print(f"ℹ️  {message}")
