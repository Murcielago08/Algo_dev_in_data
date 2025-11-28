import numpy as np

def covariance_matrix(data):
    """
    Calcule la matrice de covariance entre les features d'un dataset
    en utilisant uniquement du broadcasting et np.einsum.
    
    data : np.ndarray de shape (n_samples, n_features)
    """
    # Centrage des données (broadcasting)
    mean = data.mean(axis=0, keepdims=True)   # shape (1, n_features)
    centered = data - mean                    # shape (n_samples, n_features)

    # Calcul de la covariance avec einsum
    # Formule : (X^T X) / (n_samples - 1)
    n_samples = data.shape[0]
    cov = np.einsum('ij,ik->jk', centered, centered) / (n_samples - 1)

    return cov


# Exemple d'utilisation
np.random.seed(0)
X = np.random.rand(10, 4)  # 10 échantillons, 4 features
cov_matrix = covariance_matrix(X)

print("Matrice de covariance :\n", cov_matrix)