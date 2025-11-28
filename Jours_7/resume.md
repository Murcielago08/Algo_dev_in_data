# Broadcasting Avancé & Einstein Summation en NumPy

## Table des Matières
- [Introduction](#introduction)
- [Broadcasting Avancé](#broadcasting-avancé)
- [Einstein Summation](#einstein-summation)
- [Combinaison des Techniques](#combinaison-des-techniques)
- [Challenge Pratique](#challenge-pratique)
- [Conclusion](#conclusion)

## Introduction

### Qu'est-ce que le Broadcasting?
Le **broadcasting** est un mécanisme de NumPy permettant d'effectuer des opérations arithmétiques sur des tableaux de formes différentes en étendant automatiquement les dimensions.

### Qu'est-ce que l'Einstein Summation?
La **notation d'Einstein** simplifie l'écriture des expressions avec des sommes sur des indices répétés, implémentée via `np.einsum`.

## Broadcasting Avancé

### Règles Fondamentales

1. **Alignement à droite** : Les dimensions sont alignées depuis la droite
2. **Dimensions unités** : Les dimensions de taille 1 sont étendues

### Exemple Détaillé : Broadcasting Simple

```python
import numpy as np

# Création des tableaux
A = np.array([1, 2, 3])        # Shape: (3,)
B = np.array([[1], [2], [3]])  # Shape: (3, 1)

print("Tableau A:")
print(f"Shape: {A.shape}")
print(f"Valeurs: {A}")
print("\nTableau B:")
print(f"Shape: {B.shape}")
print(f"Valeurs:\n{B}")

# Opération avec broadcasting
result = A + B
print("\nRésultat A + B:")
print(f"Shape: {result.shape}")
print(f"Valeurs:\n{result}")
```

**Déroulement détaillé :**

1. **Alignement des shapes** :
   - A: (3,) → (1, 3)
   - B: (3, 1) → (3, 1)

2. **Extension des dimensions** :
   - A est étendu de (1, 3) à (3, 3) :
     ```
     [[1, 2, 3],
      [1, 2, 3],
      [1, 2, 3]]
     ```
   - B est étendu de (3, 1) à (3, 3) :
     ```
     [[1, 1, 1],
      [2, 2, 2],
      [3, 3, 3]]
     ```

3. **Addition élément par élément** :
   ```
   [[1+1, 2+1, 3+1],
    [1+2, 2+2, 3+2],
    [1+3, 2+3, 3+3]]
   ```

### Application Avancée : Calcul de Distances

```python
def distance_matrix_broadcasting(points1, points2):
    """
    Calcule la matrice des distances euclidiennes entre deux ensembles de points
    """
    # points1 shape: (m, d), points2 shape: (n, d)
    
    # Broadcasting: (m, 1, d) - (1, n, d) → (m, n, d)
    diff = points1[:, np.newaxis, :] - points2[np.newaxis, :, :]
    
    # Carré des différences et somme sur la dernière dimension
    squared_diff = np.sum(diff ** 2, axis=2)  # Shape: (m, n)
    
    return np.sqrt(squared_diff)

# Test avec des points simples
points_A = np.array([[0, 0], [1, 1], [2, 2]])
points_B = np.array([[1, 0], [0, 1]])

print("Points A:")
print(points_A)
print("\nPoints B:")
print(points_B)

distances = distance_matrix_broadcasting(points_A, points_B)
print("\nMatrice des distances:")
print(distances)
```

**Valeur ajoutée :**
- Évite les boucles Python coûteuses
- Code plus lisible et concis
- Meilleures performances sur de grands datasets

## Einstein Summation

### Syntaxe de Base

La syntaxe `np.einsum` suit le format :
```python
np.einsum('indices_input -> indices_output', array1, array2, ...)
```

### Opérations Élémentaires Détaillées

```python
# Création d'une matrice simple
A = np.array([[1, 2], 
              [3, 4]])

print("Matrice originale A:")
print(A)
print(f"Shape: {A.shape}")

# Transposition avec einsum
transposed = np.einsum('ij->ji', A)
print("\nTransposition 'ij->ji':")
print(transposed)

# Somme sur les lignes
sum_rows = np.einsum('ij->j', A)  # Somme sur l'axe 0 (lignes)
print("\nSomme sur les lignes 'ij->j':")
print(sum_rows)

# Somme sur les colonnes  
sum_cols = np.einsum('ij->i', A)  # Somme sur l'axe 1 (colonnes)
print("\nSomme sur les colonnes 'ij->i':")
print(sum_cols)
```

**Explication des indices :**
- `i` : indice des lignes
- `j` : indice des colonnes
- `ij->ji` : échange les dimensions
- `ij->j` : somme sur la dimension `i` (lignes)

### Application Avancée : Produit Matriciel

```python
def compare_matrix_multiplication():
    # Matrices de test
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])  # Shape: (2, 3)
    
    B = np.array([[7, 8],
                  [9, 10],
                  [11, 12]])   # Shape: (3, 2)
    
    print("Matrice A (2x3):")
    print(A)
    print("\nMatrice B (3x2):")
    print(B)
    
    # Méthode classique
    classic = np.dot(A, B)
    print("\nProduit classique (np.dot):")
    print(classic)
    print(f"Shape: {classic.shape}")
    
    # Avec einsum
    einsum_result = np.einsum('ik,kj->ij', A, B)
    print("\nProduit avec einsum 'ik,kj->ij':")
    print(einsum_result)
    
    # Vérification
    print(f"\nLes résultats sont identiques: {np.allclose(classic, einsum_result)}")
    
    return classic, einsum_result

classic, einsum = compare_matrix_multiplication()
```

**Déroulement du produit matriciel avec einsum :**

Pour `'ik,kj->ij'` :
- `i` : lignes de A (2)
- `k` : colonnes de A / lignes de B (3)  
- `j` : colonnes de B (2)

L'opération effectue : `result[i,j] = sum_k(A[i,k] * B[k,j])`

### Application Complexe : Similarité Cosinus

```python
def cosine_similarity_einsum(vectors):
    """
    Calcule la matrice de similarité cosinus entre des vecteurs
    """
    # Calcul des normes au carré
    norms_squared = np.einsum('ij,ij->i', vectors, vectors)
    
    print("Normes au carré de chaque vecteur:")
    print(norms_squared)
    
    # Normalisation des vecteurs
    normalized = vectors / np.sqrt(norms_squared[:, np.newaxis])
    
    print("\nVecteurs normalisés:")
    print(normalized)
    
    # Calcul de la similarité cosinus
    similarity = np.einsum('ik,jk->ij', normalized, normalized)
    
    return similarity

# Test avec des vecteurs simples
vectors = np.array([[1, 0, 0],    # Vecteur unité selon x
                    [0, 1, 0],    # Vecteur unité selon y  
                    [1, 1, 0]])   # Vecteur à 45°

print("Vecteurs originaux:")
print(vectors)

similarity_matrix = cosine_similarity_einsum(vectors)
print("\nMatrice de similarité cosinus:")
print(similarity_matrix)
```

## Combinaison des Techniques

### Exemple Intégré Détaillé

```python
def traitement_donnees_capteurs():
    """
    Exemple combinant broadcasting et einsum pour traiter des données de capteurs
    """
    # Simuler des données: 3 capteurs, 5 mesures, 2 features
    sensor_data = np.random.rand(3, 5, 2) * 100
    weights = np.random.rand(3, 2)
    
    print("Données des capteurs (3 capteurs × 5 mesures × 2 features):")
    print(f"Shape: {sensor_data.shape}")
    print(sensor_data)
    
    print("\nPoids par capteur et feature (3 capteurs × 2 features):")
    print(f"Shape: {weights.shape}")
    print(weights)
    
    # Méthode 1: Avec broadcasting manuel
    print("\n--- Méthode avec broadcasting manuel ---")
    # Étendre weights pour correspondre aux dimensions
    weights_expanded = weights[:, np.newaxis, :]  # Shape: (3, 1, 2)
    weighted_data = sensor_data * weights_expanded  # Broadcasting: (3, 5, 2)
    result_broadcast = np.sum(weighted_data, axis=2)  # Shape: (3, 5)
    
    print("Résultat avec broadcasting:")
    print(result_broadcast)
    
    # Méthode 2: Avec einsum (plus élégant)
    print("\n--- Méthode avec einsum ---")
    result_einsum = np.einsum('ijk,ik->ij', sensor_data, weights)
    
    print("Résultat avec einsum:")
    print(result_einsum)
    
    # Vérification
    print(f"\nLes résultats sont identiques: {np.allclose(result_broadcast, result_einsum)}")
    
    return result_broadcast, result_einsum

result1, result2 = traitement_donnees_capteurs()
```

**Valeur ajoutée de la combinaison :**
- **Performance** : Élimination des boucles Python
- **Lisibilité** : Code plus expressif et concis
- **Mémoire** : Opérations effectuées sans copies inutiles
- **Flexibilité** : Facile à adapter à différentes dimensions

## Challenge Pratique

### Implémentation de la Matrice de Covariance

```python
def covariance_matrix_custom(data):
    """
    Calcule la matrice de covariance sans utiliser np.cov
    en utilisant broadcasting et einsum
    """
    # data shape: (n_samples, n_features)
    
    # Centrer les données (soustraire la moyenne)
    means = np.mean(data, axis=0)  # Moyenne par feature
    centered = data - means  # Broadcasting: (n, m) - (m,) → (n, m)
    
    print("Données centrées:")
    print(centered)
    
    # Calcul de la covariance avec einsum
    # Formule: cov = (X.T @ X) / (n-1)
    n = data.shape[0]
    covariance = np.einsum('ki,kj->ij', centered, centered) / (n - 1)
    
    return covariance

def compare_with_numpy_cov(data):
    """Compare notre implémentation avec np.cov"""
    custom_cov = covariance_matrix_custom(data)
    numpy_cov = np.cov(data, rowvar=False)
    
    print("\nNotre implémentation:")
    print(custom_cov)
    print("\nNumPy np.cov:")
    print(numpy_cov)
    print(f"\nIdentique: {np.allclose(custom_cov, numpy_cov)}")
    
    return custom_cov, numpy_cov

# Test avec des données simples
test_data = np.array([[1, 2], 
                      [3, 4], 
                      [5, 6]])

print("Données de test:")
print(test_data)

custom, numpy = compare_with_numpy_cov(test_data)
```

## Conclusion

### Points Clés à Retenir

1. **Broadcasting** :
   - Extension automatique des dimensions
   - Alignement à partir de la droite
   - Dimensions de taille 1 étendues

2. **Einstein Summation** :
   - Notation concise pour les opérations tensorielles
   - Contrôle précis des dimensions de sortie
   - Évite les opérations intermédiaires coûteuses

3. **Combinaison** :
   - Meilleure performance que les boucles Python
   - Code plus lisible et maintenable
   - Réduction de l'utilisation mémoire

### Avantages Concrets

- **Productivité** : Code plus rapide à écrire et debugger
- **Performance** : Exécution optimisée par NumPy
- **Expressivité** : Intention du code plus claire
- **Évolutivité** : Facile à adapter à des dimensions différentes

### Prochaines Étapes

1. Pratiquer avec des datasets réels
2. Explorer d'autres fonctions NumPy avancées
3. Apprendre à profiler le code pour identifier les goulots d'étranglement
4. Étudier l'intégration avec d'autres bibliothèques (Dask, JAX)

**La maîtrise de ces techniques transforme la façon d'écrire du code scientifique, passant de boucles explicites à des opérations vectorielles élégantes et performantes.**