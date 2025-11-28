import numpy as np
import time
import math
import matplotlib.pyplot as plt
from numba import vectorize, float64

# ============================================================
# Question 1 : Analyse de Performance
# ============================================================

def calcul_numpy_standard(arr):
    terme1 = np.sin(arr ** 2)
    terme2 = np.cos(2 * arr)
    terme3 = np.exp(-arr / 10)
    terme4 = np.log(np.abs(arr) + 1)
    terme5 = arr ** 2 + 1
    return terme1 + terme2 * terme3 + terme4 / terme5

@vectorize([float64(float64)], nopython=True, target='parallel')
def ufunc_optimisee(x):
    x_carre = x * x
    sin_term = math.sin(x_carre)
    cos_term = math.cos(2 * x)
    exp_term = math.exp(-x / 10)
    log_term = math.log(abs(x) + 1)
    denom = x_carre + 1
    return sin_term + cos_term * exp_term + log_term / denom

def question1_benchmark():
    sizes = [10**5, 10**6, 10**7]
    temps_numpy, temps_ufunc, speedups = [], [], []

    print("\n=== Question 1 : Benchmark Performance ===")
    print(f"{'Taille':<12}{'NumPy (s)':<12}{'uFunc (s)':<12}{'Speedup':<10}")
    print("-"*50)

    for size in sizes:
        arr = np.random.randn(size)

        # NumPy
        start = time.time()
        result_std = calcul_numpy_standard(arr)
        time_std = time.time() - start

        # uFunc
        start = time.time()
        result_ufunc = ufunc_optimisee(arr)
        time_ufunc = time.time() - start

        # Vérification exactitude
        diff_max = np.max(np.abs(result_std - result_ufunc))
        speedup = time_std / time_ufunc

        temps_numpy.append(time_std)
        temps_ufunc.append(time_ufunc)
        speedups.append(speedup)

        print(f"{size:<12}{time_std:<12.4f}{time_ufunc:<12.4f}{speedup:<10.2f}x")
        print(f"Erreur max: {diff_max:.2e}")

    # Graphique comparatif
    plt.figure(figsize=(8,5))
    plt.plot(sizes, temps_numpy, 'o-r', label="NumPy standard")
    plt.plot(sizes, temps_ufunc, 'o-b', label="uFunc optimisée")
    plt.xlabel("Taille du tableau")
    plt.ylabel("Temps d'exécution (s)")
    plt.title("Comparaison des performances NumPy vs uFunc")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Graphique speedup
    plt.figure(figsize=(8,5))
    plt.plot(sizes, speedups, 'o-g')
    plt.xlabel("Taille du tableau")
    plt.ylabel("Speedup (x)")
    plt.title("Speedup uFunc vs NumPy")
    plt.grid(True)
    plt.show()


# ============================================================
# Question 2 : Analyse Mémoire (explication)
# ============================================================

def question2_memory():
    print("\n=== Question 2 : Analyse Mémoire ===")
    print("Version NumPy standard : crée 5 tableaux temporaires (terme1 à terme5).")
    print("Version uFunc optimisée : calcule directement chaque élément sans tableaux intermédiaires.")
    print("➡ Les uFuncs réduisent l’empreinte mémoire car elles évitent les copies inutiles.")


# ============================================================
# Question 3 : uFunc Avancée (Gradient numérique)
# ============================================================

@vectorize([float64(float64, float64, float64)], nopython=True)
def gradient_numerique(f_x_plus, f_x_minus, h):
    return (f_x_plus - f_x_minus) / (2 * h)

def question3_gradient():
    print("\n=== Question 3 : Gradient Numérique ===")
    x = np.linspace(-5, 5, 10)
    h = 1e-7
    f_x_plus = np.sin((x+h)**2)
    f_x_minus = np.sin((x-h)**2)
    grad = gradient_numerique(f_x_plus, f_x_minus, h)
    print("Gradient approx:", grad)


# ============================================================
# Question 4 : Application Réelle (Machine Learning)
# ============================================================

@vectorize([float64(float64, float64)], nopython=True)
def mse_loss(y_true, y_pred):
    return (y_true - y_pred) ** 2

@vectorize([float64(float64)], nopython=True)
def sigmoid_derivative(x):
    sig = 1.0 / (1.0 + math.exp(-x))
    return sig * (1 - sig)

def question4_ml():
    print("\n=== Question 4 : Application ML ===")
    y_true = np.array([1, 0, 1, 1])
    y_pred = np.array([0.9, 0.2, 0.8, 0.7])
    mse = mse_loss(y_true, y_pred)
    print("MSE Loss:", mse)

    x = np.linspace(-5, 5, 5)
    sig_der = sigmoid_derivative(x)
    print("Sigmoid derivative:", sig_der)


# ============================================================
# Benchmark Complet (Résumé final)
# ============================================================

def benchmark_complet():
    sizes = [10**5, 10**6, 10**7]
    print("=== BENCHMARK NumPy vs uFuncs ===")
    print(f"{'Taille':<10} {'NumPy (s)':<12} {'uFunc (s)':<12} {'Speedup':<10}")
    print("-" * 50)
    for size in sizes:
        arr = np.random.randn(size)
        
        # Version NumPy standard
        start = time.time()
        result_std = calcul_numpy_standard(arr)
        time_std = time.time() - start
        
        # Version uFunc
        start = time.time()
        result_ufunc = ufunc_optimisee(arr)
        time_ufunc = time.time() - start
        
        # V ́erification de l'exactitude
        diff_max = np.max(np.abs(result_std - result_ufunc))
        speedup = time_std / time_ufunc
        
        print(f"{size:<10} {time_std:<12.4f} {time_ufunc:<12.4f} {speedup:<10.2f}x")
        print(f"Erreur max: {diff_max:.2e}")
    return time_std, time_ufunc, speedup


# ============================================================
# MAIN : Exécution de toutes les questions
# ============================================================

if __name__ == "__main__":
    question1_benchmark()
    question2_memory()
    question3_gradient()
    question4_ml()
    benchmark_complet()