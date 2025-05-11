import json
import os

SAVE_FILE = "./save/save.json"

# Création du fichier save.json par défaut si absent
def init_save_file():
    if not os.path.exists(SAVE_FILE):
        data = {
            "Highest_score": 0,
            "money": 0,
            "level": {}
        }
        with open(SAVE_FILE, "w") as save:
            json.dump(data, save, indent=4)
        print("Fichier de sauvegarde créé")

# Fonction pour enregistrer un nouveau score
def new_score(level: str, score: int):
    with open(SAVE_FILE, "r") as save:
        data = json.load(save)

    # Créer la section level si elle n'existe pas
    if "level" not in data:
        data["level"] = {}

    # Créer l'entrée pour ce niveau si elle n'existe pas
    if level not in data["level"]:
        data["level"][level] = {"best_score": 0}

    # Vérifier et mettre à jour le best_score du niveau
    current_best = data["level"][level]["best_score"]
    if score > current_best:
        data["level"][level]["best_score"] = score

    # Mettre à jour le Highest_score global si nécessaire
    if score > data.get("Highest_score", 0):
        data["Highest_score"] = score

    # Sauvegarder les modifications
    with open(SAVE_FILE, "w") as save:
        json.dump(data, save, indent=4)

def get_highest_score():
    try:
        with open(SAVE_FILE, "r") as save:
            data = json.load(save)
        return data.get("Highest_score", 0)
    except FileNotFoundError:
        print("Fichier de sauvegarde introuvable.")
        return 0
    except json.JSONDecodeError:
        print("Erreur de lecture du fichier JSON.")
        return 0

def get_money():
    try:
        with open(SAVE_FILE, "r") as save:
            data = json.load(save)
        return data.get("money", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def set_money(amount):
    try:
        with open(SAVE_FILE, "r") as save:
            data = json.load(save)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["money"] = amount

    with open(SAVE_FILE, "w") as save:
        json.dump(data, save, indent=4)

def reset_progression():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("Fichier de sauvegarde supprimé.")
    else:
        print("Aucun fichier de sauvegarde à supprimer.")
