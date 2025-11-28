import numpy as np
from numpy.lib.stride_tricks import as_strided

def fenetrage_signal(signal, taille_fenetre):
    """
    Crée des fenêtres glissantes sur un signal sans duplication mémoire.
    """
    n = signal.shape[0]
    # Nombre de fenêtres possibles
    nb_fenetres = n - taille_fenetre + 1
    
    # Strides : avancer d'un élément à chaque fenêtre
    fenetres = as_strided(signal,
                          shape=(nb_fenetres, taille_fenetre),
                          strides=(signal.strides[0], signal.strides[0]))
    return fenetres

# Exemple : signal simulé
signal = np.arange(20, dtype=np.float64)
fenetres = fenetrage_signal(signal, taille_fenetre=5)

print("Signal original :", signal)
print("\nFenêtres générées :")
print(fenetres)

# Exemple d'analyse : moyenne par fenêtre
moyennes = fenetres.mean(axis=1)
print("\nMoyenne par fenêtre :", moyennes)