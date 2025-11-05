import csv
import os

def lire_csv_en_dict(chemin_fichier: str):
    """
    Lit un fichier CSV et retourne une liste de dictionnaires.
    Chaque ligne est convertie en dict selon les en-têtes du CSV.
    """
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")

    with open(chemin_fichier, mode="r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
