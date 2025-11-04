# R c u r s i o n simple ( peut causer stack overflow )
def somme_liste_simple(lst):
	if not lst:
		return 0
	return lst[0] + somme_liste_simple(lst[1:])

# R c u r s i o n terminale (optimise)
def somme_liste_terminale(lst, acc=0):
    if not lst:
        return acc
    print(f"Accumulateur: {acc}, Liste restante: {lst}")
    return somme_liste_terminale(lst[1:], acc + lst[0])

# R c u r s i o n avec pattern matching style
def somme_liste_pattern(lst):
    match lst:
        case []:
            return 0
        case [x, *reste]:
            print(f"Valeur courante: {x}, Reste de la liste: {reste}")
            return x + somme_liste_pattern(reste)

# Utilisation
nombres = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Somme simple: {somme_liste_simple(nombres)}")
print(f"Somme terminale: {somme_liste_terminale(nombres)}")
print(f"Somme pattern: {somme_liste_pattern(nombres)}")

# R c u r s i o n pour Fibonacci
def fibonacci(n):
    """
    Calcule Fibonacci(n) avec une fonction auxiliaire tail-recursive.
    Le helper est appelé avec (n, a, b) où:
      - a représente Fib(k-2)
      - b représente Fib(k-1)
    En initialisant a=0 et b=1 on respecte les valeurs de base:
      Fib(0) = 0, Fib(1) = 1
    Ainsi fib_helper(n, 0, 1) démarre la suite correctement.
    """
    def fib_helper(n, a, b):
        print(f"Calculating Fibonacci: n={n}, a={a}, b={b}")
        if n == 0:
            print(f"Fibonacci({n}) = {a}")
            return a
        elif n == 1:
            print(f"Fibonacci({n}) = {b}")
            return b
        else:
            return fib_helper(n - 1, b, a + b)
    print(f"Starting Fibonacci calculation for n={n}")
    # On passe a=Fib(0)=0 et b=Fib(1)=1 pour démarrer la récurrence correctement
    return fib_helper(n, 0, 1)

# Nouvelle fonction : retourne la trace des appels (liste de tuples (n, a, b))
def fibonacci_trace(n):
    traces = []
    def helper(n, a, b):
        traces.append((n, a, b))
        if n == 0:
            return a
        elif n == 1:
            return b
        else:
            return helper(n - 1, b, a + b)
    helper(n, 0, 1)
    return traces

# Nouvelle fonction : affiche étape par étape le cheminement pour Fibonacci(n)
def print_fibonacci_path(n):
    traces = fibonacci_trace(n)
    print(f"Cheminement pour Fibonacci({n}) :")
    for i, (cn, a, b) in enumerate(traces):
        print(f"  appel {i}: n={cn}, a={a}, b={b}")
    last_n, last_a, last_b = traces[-1]
    resultat = last_a if last_n == 0 else last_b
    print(f"Résultat final: Fibonacci({n}) = {resultat}")

print(f"Fibonacci de 10: {fibonacci(10)}")
print_fibonacci_path(10)
