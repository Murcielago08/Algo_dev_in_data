import numpy as np
import pandas as pd
import time

print("="*80)
print("TP : Comparaison entre np.sum et np.einsum sur un dataset NBA")
print("="*80)

# ============================================================================
# 1. PRÉPARATION DU DATASET
# ============================================================================
print("\n1. Préparation du dataset...")

# Nombre d'échantillons
n_samples = 1000000

# Liste de joueurs NBA fictifs
player_names = ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo", 
                "Luka Doncic", "Nikola Jokic", "Joel Embiid", "Damian Lillard"]
teams = ["LAL", "GSW", "BKN", "MIL", "DAL", "DEN", "PHI", "POR"]
positions = ["SF", "PG", "SF", "PF", "PG", "C", "C", "PG"]

# Génération du dataset complet
data = {
    "player": np.random.choice(player_names, n_samples),
    "team": np.random.choice(teams, n_samples),
    "POS": np.random.choice(positions, n_samples),
    "GP": np.random.randint(50, 82, n_samples),  # Games Played (50-82)
    "MIN": np.random.rand(n_samples) * 48,  # Minutes (0-48)
    "PTS": np.random.rand(n_samples) * 30,  # Points (0-30)
    "REB": np.random.rand(n_samples) * 15,  # Rebounds (0-15)
    "AST": np.random.rand(n_samples) * 12,  # Assists (0-12)
    "STL": np.random.rand(n_samples) * 5,   # Steals (0-5)
    "BLK": np.random.rand(n_samples) * 5,   # Blocks (0-5)
    "TO": np.random.rand(n_samples) * 6,    # Turnovers (0-6)
    "salary": np.random.randint(500000, 45000000, n_samples)  # Salary (500k-45M)
}

df = pd.DataFrame(data)

# Affichage des premières lignes
print(f"Dataset créé : {df.shape[0]} échantillons, {df.shape[1]} colonnes")
print(f"\nPremières lignes du dataset :")
print(df.head(10))
print(f"\nTypes de données :")
print(df.dtypes)

# Conversion des colonnes numériques en array NumPy pour accélérer les calculs
# On extrait uniquement les colonnes numériques (PTS, REB, AST)
numeric_cols = ["PTS", "REB", "AST"]
arr = df[numeric_cols].to_numpy()
print(f"\nArray NumPy créé pour les calculs : {arr.shape[0]} lignes x {arr.shape[1]} colonnes")
print(f"Colonnes numériques utilisées : {numeric_cols}")

# ============================================================================
# 2. SOMME AVEC NP.SUM
# ============================================================================
print("\n" + "="*80)
print("2. Somme avec np.sum")
print("="*80)

start = time.time()
# Somme des points, rebonds et passes
total_sum = np.sum(arr, axis=0)
end = time.time()

print("Résultat np.sum:", total_sum)
print("Temps d'exécution np.sum:", end - start, "secondes")

# ============================================================================
# 3. SOMME AVEC NP.EINSUM
# ============================================================================
print("\n" + "="*80)
print("3. Somme avec np.einsum")
print("="*80)

start = time.time()
# np.einsum permet de sommer les colonnes facilement
total_einsum = np.einsum('ij->j', arr)
end = time.time()

print("Résultat np.einsum:", total_einsum)
print("Temps d'exécution np.einsum:", end - start, "secondes")

# ============================================================================
# 4. ANALYSE DES RÉSULTATS
# ============================================================================
print("\n" + "="*80)
print("4. Analyse des résultats")
print("="*80)

# Vérification que les résultats sont identiques
if np.allclose(total_sum, total_einsum):
    print("✓ Les résultats de np.sum et np.einsum sont identiques!")
else:
    print("✗ ATTENTION : Les résultats diffèrent!")

print(f"\nDifférence absolue : {np.abs(total_sum - total_einsum)}")

# ============================================================================
# 5. EXERCICE AVANCÉ : SOMME PONDÉRÉE
# ============================================================================
print("\n" + "="*80)
print("5. Exercice avancé : somme pondérée")
print("="*80)

weights = np.array([0.5, 1.5, 2.0])  # pondérations pour PTS, REB, AST
print(f"Poids utilisés : PTS={weights[0]}, REB={weights[1]}, AST={weights[2]}")

# Méthode 1 : avec np.sum
print("\nMéthode 1 : np.sum")
start = time.time()
weighted_sum1 = np.sum(arr * weights, axis=1)
end = time.time()
time_sum = end - start

print("Résultat np.sum pondéré (5 premiers):", weighted_sum1[:5])
print(f"Temps d'exécution : {time_sum} secondes")

# Méthode 2 : avec np.einsum
print("\nMéthode 2 : np.einsum")
start = time.time()
weighted_sum2 = np.einsum('ij,j->i', arr, weights)
end = time.time()
time_einsum = end - start

print("Résultat np.einsum pondéré (5 premiers):", weighted_sum2[:5])
print(f"Temps d'exécution : {time_einsum} secondes")

# Vérification
print("\nVérification :")
if np.allclose(weighted_sum1, weighted_sum2):
    print("✓ Les deux méthodes donnent des résultats identiques!")
else:
    print("✗ ATTENTION : Les résultats diffèrent!")

# Comparaison des performances
print("\n" + "="*80)
print("6. Comparaison des performances")
print("="*80)

speedup = time_sum / time_einsum
if speedup > 1:
    print(f"np.einsum est {speedup:.2f}x plus rapide que np.sum pour la somme pondérée")
elif speedup < 1:
    print(f"np.sum est {1/speedup:.2f}x plus rapide que np.einsum pour la somme pondérée")
else:
    print("Les deux méthodes ont des performances similaires")

print("\n" + "="*80)
print("Conclusion :")
print("- np.einsum est plus flexible pour les calculs complexes")
print("- Pour des opérations simples, np.sum peut être plus lisible")
print("- Les performances peuvent varier selon la taille du dataset et l'opération")
print("="*80)
