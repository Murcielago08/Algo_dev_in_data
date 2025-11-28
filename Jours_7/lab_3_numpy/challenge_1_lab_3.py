import numpy as np

# Fonction Python standard
def rendement_compose(capital_initial, taux, duree):
    """
    Calcule le rendement composé :
    capital_final = capital_initial * (1 + taux) ** duree
    """
    return capital_initial * (1 + taux) ** duree

# Conversion en UFunc
ufunc_rendement = np.frompyfunc(rendement_compose, 3, 1)

# Exemple : calcul sur plusieurs investissements
capitaux = np.array([1000, 2000, 5000], dtype=np.float64)
taux = np.array([0.05, 0.03, 0.07], dtype=np.float64)
durees = np.array([10, 5, 20], dtype=np.int64)

resultats = ufunc_rendement(capitaux, taux, durees)

print("Capitaux initiaux :", capitaux)
print("Taux :", taux)
print("Durées :", durees)
print("Capitaux finaux :", resultats)