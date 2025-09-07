from models.player import PlayerData, save_player, delete_player


def gestion_player():
    print("=== Gestion des joueurs ===")
    print("1. Créer un joueur")
    print("2. Supprimer un joueur")
    choix = input("Choisissez une option (1/2) : ").strip()

    if choix == "1":
        name = input("Prénom : ").strip()
        lastName = input("Nom : ").strip()
        birthDate = input("Date de naissance (YYYY-MM-DD) : ").strip()
        nationalId = input("Identifiant national : ").strip()

        joueur = PlayerData(name, lastName, birthDate, nationalId)
        ok = save_player(joueur)
        if ok:
            print(f"✅ {joueur.name} {joueur.lastName} ajouté avec succès.")
        else:
            print(f"❌ Joueur avec ID {joueur.nationalId} déjà existant.")

    elif choix == "2":
        nationalId = input(
            "Entrez l'identifiant national du joueur à supprimer : "
        ).strip()
        ok = delete_player(nationalId)
        if ok:
            print(f"✅ Joueur avec ID {nationalId} supprimé avec succès.")
        else:
            print(f"❌ Aucun joueur trouvé avec l'ID {nationalId}.")

    else:
        print("❌ Choix invalide.")
