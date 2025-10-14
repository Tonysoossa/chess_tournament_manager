from models.player import PlayerData, save_player, delete_player
from views.player_view import PlayerView
from controllers.tournament_controller import TournamentController
from datetime import datetime


class PlayerController:
    def __init__(self):
        self.view = PlayerView()
        self.tournament_controller = TournamentController()


    def validate_and_format_id(self, national_id: str) -> str:
        """Valide et formate l'ID national."""
        if len(national_id) != 7:
            raise ValueError("L'ID doit contenir exactement 7 caractères")

        letters = national_id[:2].upper()
        digits = national_id[2:]

        if not letters.isalpha() or not digits.isdigit():
            raise ValueError("Format invalide : 2 lettres suivies de 5 chiffres")

        return letters + digits


    def format_birth_date(self, raw_date: str) -> str:
        """Formate la date de naissance."""
        try:
            dt = datetime.strptime(raw_date, "%Y%m%d")
            return dt.strftime("%Y/%m/%d")
        except ValueError:
            raise ValueError("Date invalide, utilisez le format YYYYMMDD")


    def create_player(self):
        """Gère la création d'un joueur avec gestion d'erreurs."""
        while True:
            try:
                name, last_name, birth_date, national_id = self.view.get_player_info()

                # Validation
                national_id = self.validate_and_format_id(national_id)
                birth_date = self.format_birth_date(birth_date)

                last_name = last_name.capitalize()
                name = name.capitalize()

                joueur = PlayerData(name, last_name, birth_date, national_id)
                ok = save_player(joueur)

                if ok:
                    self.view.show_success(f"{joueur.name} {joueur.last_name} ajouté avec succès.")
                    return
                else:
                    self.view.show_error(f"Joueur avec ID {joueur.national_id} déjà existant.")

                    retry = self.view.ask_retry()
                    if retry != 'o':
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

    def delete_player_action(self):
        """Gère la suppression d'un joueur avec gestion d'erreurs."""
        while True:
            try:
                national_id = self.view.get_player_id_to_delete()
                national_id = self.validate_and_format_id(national_id)

                ok = delete_player(national_id)

                if ok:
                    self.view.show_success(f"Joueur avec ID {national_id} supprimé avec succès.")
                    return
                else:
                    self.view.show_error(f"Aucun joueur trouvé avec l'ID {national_id}.")

                    retry = self.view.ask_retry()
                    if retry != 'o':
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
                self.view.show_info("\nProgramme interrompu. Au revoir !")
                break
            except Exception as e:
                self.view.show_error(f"Erreur inattendue : {e}")
                retry = self.view.ask_continue()
                if retry != 'o':
                    break
