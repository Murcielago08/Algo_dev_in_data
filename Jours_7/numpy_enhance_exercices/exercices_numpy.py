"""
Exercices NumPy et Matplotlib - Analyse des joueurs MMORPG
Auteur: Étudiant
Date: 2025-11-28
"""

import numpy as np
import matplotlib.pyplot as plt

# Chargement du dataset
print("=" * 60)
print("CHARGEMENT DU DATASET")
print("=" * 60)

# Charger le fichier CSV avec genfromtxt
data = np.genfromtxt('dataset_joueurs.csv', delimiter=',', names=True, dtype=None, encoding='utf-8')

# Afficher les premières lignes
print("\nPremiers éléments du dataset:")
print(data[:5])

# Afficher les dernières lignes
print("\nDerniers éléments du dataset:")
print(data[-5:])

# Afficher les noms des colonnes
print("\nNoms des colonnes:")
print(data.dtype.names)

# Informations sur le dataset
print("\n" + "=" * 60)
print("INFORMATIONS SUR LE DATASET")
print("=" * 60)
print(f"Taille du dataset: {data.size}")
print(f"Forme du dataset: {data.shape}")
print(f"Type de données: {data.dtype}")

# ============================================================================
# QUESTION 1: Meilleur joueur dans la classe Guerrier
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 1: Meilleur joueur dans la classe Guerrier")
print("=" * 60)

# Filtrer les joueurs de la classe Guerrier
guerriers = data[data['class'] == 'Guerrier']
print(f"Nombre de Guerriers: {len(guerriers)}")

# Trouver l'indice du joueur avec le maximum de victoires
if len(guerriers) > 0:
    idx_meilleur_guerrier = np.argmax(guerriers['nb_victoires'])
    meilleur_guerrier = guerriers[idx_meilleur_guerrier]
    print(f"Meilleur Guerrier: {meilleur_guerrier['pseudo']}")
    print(f"  - Parties jouées: {meilleur_guerrier['nb_parties']}")
    print(f"  - Victoires: {meilleur_guerrier['nb_victoires']}")
    print(f"  - Équipe: {meilleur_guerrier['team']}")

# ============================================================================
# QUESTION 2: Meilleur joueur dans la classe Archer
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 2: Meilleur joueur dans la classe Archer")
print("=" * 60)

# Filtrer les joueurs de la classe Archer
archers = data[data['class'] == 'Archer']
print(f"Nombre d'Archers: {len(archers)}")

# Trouver l'indice du joueur avec le maximum de victoires
if len(archers) > 0:
    idx_meilleur_archer = np.argmax(archers['nb_victoires'])
    meilleur_archer = archers[idx_meilleur_archer]
    print(f"Meilleur Archer: {meilleur_archer['pseudo']}")
    print(f"  - Parties jouées: {meilleur_archer['nb_parties']}")
    print(f"  - Victoires: {meilleur_archer['nb_victoires']}")
    print(f"  - Équipe: {meilleur_archer['team']}")

# ============================================================================
# QUESTION 3: Afficher toutes les équipes disponibles
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 3: Toutes les équipes disponibles")
print("=" * 60)

equipes_uniques = np.unique(data['team'])
print(f"Nombre d'équipes: {len(equipes_uniques)}")
print("Équipes:", equipes_uniques)

# ============================================================================
# QUESTION 4: Meilleure équipe (victoires cumulées)
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 4: Meilleure équipe (victoires cumulées)")
print("=" * 60)

# Calculer les victoires par équipe
victoires_par_equipe = {}
for equipe in equipes_uniques:
    joueurs_equipe = data[data['team'] == equipe]
    total_victoires = np.sum(joueurs_equipe['nb_victoires'])
    victoires_par_equipe[equipe] = total_victoires
    print(f"Équipe {equipe}: {total_victoires} victoires")

# Trouver la meilleure équipe
meilleure_equipe = max(victoires_par_equipe, key=victoires_par_equipe.get)
print(f"\nMeilleure équipe: {meilleure_equipe} avec {victoires_par_equipe[meilleure_equipe]} victoires")

# ============================================================================
# QUESTION 5: Meilleur joueur global
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 5: Meilleur joueur global")
print("=" * 60)

idx_meilleur_joueur = np.argmax(data['nb_victoires'])
meilleur_joueur = data[idx_meilleur_joueur]
print(f"Meilleur joueur: {meilleur_joueur['pseudo']}")
print(f"  - Parties jouées: {meilleur_joueur['nb_parties']}")
print(f"  - Victoires: {meilleur_joueur['nb_victoires']}")
print(f"  - Équipe: {meilleur_joueur['team']}")
print(f"  - Classe: {meilleur_joueur['class']}")

# ============================================================================
# QUESTION 6: Afficher toutes les classes disponibles
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 6: Toutes les classes disponibles")
print("=" * 60)

classes_uniques = np.unique(data['class'])
print(f"Nombre de classes: {len(classes_uniques)}")
print("Classes:", classes_uniques)

# ============================================================================
# QUESTION 7: Corrélation entre parties jouées et victoires
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 7: Corrélation parties jouées vs victoires")
print("=" * 60)

# Calculer la corrélation
correlation_matrix = np.corrcoef(data['nb_parties'], data['nb_victoires'])
correlation = correlation_matrix[0, 1]
print(f"Coefficient de corrélation: {correlation:.4f}")

if correlation > 0.7:
    print("Interprétation: Forte corrélation positive")
    print("Plus un joueur joue de parties, plus il a tendance à gagner.")
elif correlation > 0.3:
    print("Interprétation: Corrélation positive modérée")
    print("Il y a une relation entre le nombre de parties et les victoires.")
elif correlation > -0.3:
    print("Interprétation: Faible corrélation")
    print("Pas de relation claire entre le nombre de parties et les victoires.")
else:
    print("Interprétation: Corrélation négative")

# ============================================================================
# QUESTION 8: Corrélation entre classe et victoires
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 8: Corrélation classe vs victoires")
print("=" * 60)

print("Moyenne des victoires par classe:")
for classe in classes_uniques:
    joueurs_classe = data[data['class'] == classe]
    moyenne_victoires = np.mean(joueurs_classe['nb_victoires'])
    ecart_type = np.std(joueurs_classe['nb_victoires'])
    print(f"  {classe}: {moyenne_victoires:.2f} victoires (±{ecart_type:.2f})")

# Analyse qualitative
moyennes_classes = []
for classe in classes_uniques:
    joueurs_classe = data[data['class'] == classe]
    moyenne_victoires = np.mean(joueurs_classe['nb_victoires'])
    moyennes_classes.append(moyenne_victoires)

variance_moyennes = np.var(moyennes_classes)
print(f"\nVariance des moyennes entre classes: {variance_moyennes:.2f}")

if variance_moyennes > 10:
    print("Interprétation: Les classes ont des performances significativement différentes.")
else:
    print("Interprétation: Les classes ont des performances similaires.")

# ============================================================================
# QUESTION 9: Graphique parties jouées vs victoires
# ============================================================================
print("\n" + "=" * 60)
print("QUESTION 9: Graphique scatter plot")
print("=" * 60)

# Créer le graphique de dispersion
plt.figure(figsize=(10, 6))
plt.scatter(data['nb_parties'], data['nb_victoires'], alpha=0.6, color='blue', edgecolors='black')

# Configuration des axes et du titre
plt.xlabel('Nombre de parties jouées', fontsize=12)
plt.ylabel('Nombre de victoires', fontsize=12)
plt.title('Relation entre le nombre de parties jouées et le nombre de victoires', fontsize=14, fontweight='bold')

# Ajouter une grille pour faciliter la lecture
plt.grid(True, alpha=0.3)

# Ajouter la ligne de corrélation (régression linéaire simple)
z = np.polyfit(data['nb_parties'], data['nb_victoires'], 1)
p = np.poly1d(z)
plt.plot(data['nb_parties'], p(data['nb_parties']), "r--", alpha=0.8, label=f'Tendance (r={correlation:.3f})')

plt.legend()

# Sauvegarder le graphique
plt.savefig('graphique_parties_vs_victoires.png', dpi=300, bbox_inches='tight')
print("Graphique sauvegardé: graphique_parties_vs_victoires.png")

# Afficher le graphique (commenté pour éviter le blocage)
# plt.show()

print("\n" + "=" * 60)
print("ANALYSE TERMINÉE")
print("=" * 60)
