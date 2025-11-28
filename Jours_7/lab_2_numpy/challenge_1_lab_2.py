import numpy as np
from datetime import datetime

# Définition du type structuré
dtype_inventaire = [
    ('nom', 'U20'),
    ('categorie', 'U20'),
    ('prix', 'f8'),
    ('quantite', 'i4'),
    ('date_ajout', 'datetime64[D]')
]

# Création d'un inventaire initial
inventaire = np.array([
    ('Laptop', 'Electronique', 1200.0, 15, np.datetime64('2025-11-01')),
    ('Smartphone', 'Electronique', 800.0, 8, np.datetime64('2025-11-05')),
    ('Chaise', 'Mobilier', 150.0, 25, np.datetime64('2025-11-10')),
    ('Table', 'Mobilier', 300.0, 5, np.datetime64('2025-11-15')),
], dtype=dtype_inventaire)

# ➡️ Ajouter un produit
def ajouter_produit(inventaire, produit):
    return np.append(inventaire, np.array([produit], dtype=dtype_inventaire))

# ➡️ Supprimer un produit par nom
def supprimer_produit(inventaire, nom):
    return inventaire[inventaire['nom'] != nom]

# ➡️ Filtrer produits low-stock (< 10 unités)
def produits_low_stock(inventaire):
    return inventaire[inventaire['quantite'] < 10]

# ➡️ Trouver le produit le plus cher par catégorie
def produit_plus_cher_par_categorie(inventaire):
    categories = np.unique(inventaire['categorie'])
    resultats = {}
    for cat in categories:
        produits_cat = inventaire[inventaire['categorie'] == cat]
        produit_max = produits_cat[np.argmax(produits_cat['prix'])]
        resultats[cat] = produit_max
    return resultats

# Exemple d'utilisation
inventaire = ajouter_produit(inventaire, ('Casque', 'Electronique', 200.0, 12, np.datetime64('2025-11-20')))
inventaire = supprimer_produit(inventaire, 'Table')

print("Produits low-stock:\n", produits_low_stock(inventaire))
print("\nProduits les plus chers par catégorie:")
for cat, prod in produit_plus_cher_par_categorie(inventaire).items():
    print(cat, ":", prod)