from models.player import PlayerData, save_player, delete_player
from views.player_view import PlayerView
from controllers.tournament_controller import TournamentController
from datetime import datetime


class PlayerController:
    def __init__(self):
        self.view = PlayerView()
        self.tournament_controller = TournamentController()

    def validate_and_format_id(self, nationalId: str) -> str:
        """Valide et formate l'ID national."""
        if len(nationalId) != 7:
            raise ValueError("L'ID doit contenir exactement 7 caractères")

        letters = nationalId[:2].upper()
        digits = nationalId[2:]

        if not letters.isalpha() or not digits.isdigit():
            raise ValueError("Format invalide : 2 lettres suivies de 5 chiffres")

        return letters + digits

    def format_birthdate(self, raw_date: str) -> str:
        """Formate la date de naissance."""
        try:
            dt = datetime.strptime(raw_date, "%Y%m%d")
            return dt.strftime("%Y/%m/%d")
        except ValueError:
            raise ValueError("Date invalide, utilisez le format YYYYMMDD (sans separateur)")

    def create_player(self):
        """Gère la création d'un joueur avec gestion d'erreurs."""
        while True:
            try:
                name, lastName, birthDate, nationalId = self.view.get_player_info()

                # Validation
                nationalId = self.validate_and_format_id(nationalId)
                birthDate = self.format_birthdate(birthDate)

                lastName = lastName.capitalize()
                name = name.capitalize()

                joueur = PlayerData(name, lastName, birthDate, nationalId)
                ok = save_player(joueur)

                if ok:
                    self.view.show_success(f"{joueur.name} {joueur.lastName} ajouté avec succès.")
                    return
                else:
                    self.view.show_error(f"Joueur avec ID {joueur.nationalId} déjà existant.")

                    retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                    if retry != 'o':
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

    def delete_player_action(self):
        """Gère la suppression d'un joueur avec gestion d'erreurs."""
        while True:
            try:
                nationalId = self.view.get_player_id_to_delete()
                nationalId = self.validate_and_format_id(nationalId)

                ok = delete_player(nationalId)

                if ok:
                    self.view.show_success(f"Joueur avec ID {nationalId} supprimé avec succès.")
                    return
                else:
                    self.view.show_error(f"Aucun joueur trouvé avec l'ID {nationalId}.")

                    retry = input("Voulez-vous réessayer ? (o/n) : ").strip().lower()
                    if retry != 'o':
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

    def run(self):
        """Boucle principale du programme."""
        while True:
            try:
                self.view.show_menu()
                choix = self.view.get_menu_choice()

                if choix == "1":
                    self.create_player()
                elif choix == "2":
                    self.delete_player_action()
                elif choix == "3":
                    self.view.show_info("Début du tournoi...")
                    self.tournament_controller.create_tournament()
                elif choix == "0":
                    self.view.show_info("Au revoir !")
                    break
                else:
                    self.view.show_error("Choix invalide. Veuillez choisir 1, 2, 3 ou 0.")

            except KeyboardInterrupt:
                print("\n")
                self.view.show_info("Programme interrompu. Au revoir !")
                break
            except Exception as e:
                self.view.show_error(f"Erreur inattendue : {e}")
                retry = input("Voulez-vous continuer ? (o/n) : ").strip().lower()
                if retry != 'o':
                    break