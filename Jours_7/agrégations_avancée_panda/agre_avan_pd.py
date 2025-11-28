import os
import pandas as pd

# ---------------------------------------------------
# Étape 1 : Charger le dataset
# ---------------------------------------------------

# Définir le chemin du dossier où se trouve ton fichier
base_dir = r"C:\Users\darkj\Desktop\Doc_Ynov\DATA\Algo_dev_in_data\Jours_7\agrégations_avancée_panda"
file_path = os.path.join(base_dir, "basketball_stats.csv")

# Charger le dataset
df = pd.read_csv(file_path)
print("Aperçu du dataset :")
print(df.head())

# ---------------------------------------------------
# Étape 2 : Agrégation simple par année
# ---------------------------------------------------

# Moyenne des points et des rebonds par année
result_simple = df.groupby('year')[['PTS', 'REB']].mean()
print("\nMoyenne des points et rebonds par année :")
print(result_simple)

# ---------------------------------------------------
# Étape 3 : Agrégation avancée avec plusieurs fonctions
# ---------------------------------------------------

aggregations = {
    'PTS': ['sum', 'mean', 'max'],          # total, moyenne, maximum
    'REB': ['sum', 'mean', 'std'],          # total, moyenne, écart-type
    'salary': ['sum', lambda x: x.quantile(0.9)]  # somme et 90e percentile
}

result_adv = df.groupby('year').agg(aggregations)
print("\nAgrégations avancées par année :")
print(result_adv)

# ---------------------------------------------------
# Étape 4 : Agrégation par équipe et par position
# ---------------------------------------------------

team_pos_agg = df.groupby(['team', 'POS']).agg({
    'PTS': ['mean', 'max'],
    'AST': 'mean',
    'REB': 'mean'
})
print("\nAgrégations par équipe et position :")
print(team_pos_agg)

# ---------------------------------------------------
# Étape 5 : Exploration des résultats
# ---------------------------------------------------

# Identifier l'année où les joueurs ont marqué le plus de points
year_max_points = result_adv['PTS']['sum'].idxmax()
print(f"\nAnnée avec le plus de points marqués : {year_max_points}")

# Identifier l'équipe et la position ayant la meilleure moyenne de passes (AST)
best_ast = team_pos_agg['AST']['mean'].idxmax()
print(f"Équipe et position avec la meilleure moyenne de passes : {best_ast}")
