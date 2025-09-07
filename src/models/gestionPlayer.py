from models.player import PlayerData, save_player, delete_player
from datetime import datetime
from models.tournament import gestion_tournament


def validate_and_format_id(nationalId: str) -> str:
    if len(nationalId) != 7:
        raise ValueError("L'ID doit contenir exactement 7 caractères")

    letters = nationalId[:2].upper()
    digits = nationalId[2:]

    if not letters.isalpha() or not digits.isdigit():
        raise ValueError("Format invalide")

    return letters + digits


def format_birthdate(raw_date: str) -> str:
    try:
        dt = datetime.strptime(raw_date, "%Y%m%d")
        return dt.strftime("%Y/%m/%d")
    except ValueError:
        raise ValueError("Date invalide, utilisez le format YYYYMMDD")


def gestion_player():
    print("=== Gestion des joueurs ===")
    print("1. Créer un joueur")
    print("2. Supprimer un joueur")
    print("3. Commencer le tournoi")
    choix = input("Choisissez une option (1/2/3) : ").strip()

    if choix == "1":
        name_input = input("Prénom : ").strip()
        lastName_input = input("Nom : ").strip()
        birthDate_input = input("Date de naissance (YYYY-MM-DD) : ").strip()
        nationalId_input = input("Identifiant national : ").strip()

        try:
            nationalId = validate_and_format_id(nationalId_input)
            birthDate = format_birthdate(birthDate_input)
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            return

        lastName = lastName_input.capitalize()
        name = name_input.capitalize()

        joueur = PlayerData(name, lastName, birthDate, nationalId)
        ok = save_player(joueur)
        if ok:
            print(f"✅ {joueur.name} {joueur.lastName} ajouté avec succès.")
        else:
            print(f"❌ Joueur avec ID {joueur.nationalId} déjà existant.")

    elif choix == "2":
        nationalId_input = input(
            "Entrez l'identifiant national du joueur à supprimer : "
        ).strip()

        try:
            nationalId = validate_and_format_id(nationalId_input)
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            return

        ok = delete_player(nationalId)
        if ok:
            print(f"✅ Joueur avec ID {nationalId} supprimé avec succès.")
        else:
            print(f"❌ Aucun joueur trouvé avec l'ID {nationalId}.")

    elif choix == "3":
        print("Début du tournoi...")
        gestion_tournament()

    else:
        print("❌ Choix invalide.")
