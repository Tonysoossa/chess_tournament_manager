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
            print(f"- {p.name} {p.lastName} ({p.nationalId})")

    @staticmethod
    def get_player_ids():
        """Demande les IDs des joueurs à inscrire."""
        return input("\nEntrez les ID des joueurs à inscrire, séparés par des virgules : ").strip()

    @staticmethod
    def show_registered_players(players: list[PlayerData]):
        """Affiche les joueurs inscrits."""
        names = [f"{p.name} {p.lastName}" for p in players]
        print(f"\n✅ Joueurs inscrits : {', '.join(names)}")

    @staticmethod
    def show_match(p1_name: str, p2_name: str):
        """Affiche les informations d'un match."""
        print(f"\nMatch : {p1_name} vs {p2_name}")
        print(f"Entrez le résultat :")
        print(f"1 = {p1_name} gagne")
        print(f"2 = {p2_name} gagne")
        print(f"3 = nul")

    @staticmethod
    def get_match_result():
        """Demande le résultat du match."""
        return input("Résultat (1/2/3) : ").strip()

    @staticmethod
    def show_round_summary(round_name: str, matches: list):
        """Affiche le résumé d'un round."""
        print(f"\n=== {round_name} terminé ===")
        for m in matches:
            print(f"- {m[0][0]} ({m[0][1]}) vs {m[1][0]} ({m[1][1]})")

    @staticmethod
    def show_tournament_saved(tournament_name: str):
        print(f"\n✅ Tournoi '{tournament_name}' sauvegardé avec succès !")

    @staticmethod
    def show_error(message: str):
        print(f"❌ {message}")

    @staticmethod
    def show_info(message: str):
        print(f"ℹ️  {message}")