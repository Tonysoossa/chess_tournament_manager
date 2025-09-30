class PlayerView:
    @staticmethod
    def show_menu():
        print("\n=== Gestion des joueurs ===")
        print("1. Créer un joueur")
        print("2. Supprimer un joueur")
        print("3. Commencer le tournoi")
        print("0. Quitter")

    @staticmethod
    def get_menu_choice():
        return input("Choisissez une option (1/2/3/0) : ").strip()

    @staticmethod
    def get_player_info():
        """Demande les informations du joueur."""
        name = input("Prénom : ").strip()
        lastName = input("Nom : ").strip()
        birthDate = input("Date de naissance (YYYYMMDD) : ").strip()
        nationalId = input("Identifiant national (2 lettres + 5 chiffres) : ").strip()
        return name, lastName, birthDate, nationalId

    @staticmethod
    def get_player_id_to_delete():
        """Demande l'ID du joueur à supprimer."""
        return input("Entrez l'identifiant national du joueur à supprimer : ").strip()

    @staticmethod
    def show_success(message: str):
        print(f"✅ {message}")

    @staticmethod
    def show_error(message: str):
        print(f"❌ {message}")

    @staticmethod
    def show_info(message: str):
        print(f"ℹ️  {message}")