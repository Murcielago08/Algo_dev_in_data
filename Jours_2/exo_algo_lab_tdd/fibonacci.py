def fibonacci(n: int) -> int:
    """
    Calcule le n-ième nombre de la suite de Fibonacci de manière itérative.

    Args:
        n (int): Position dans la suite (doit être >= 0).

    Returns:
        int: Le n-ième nombre de Fibonacci.

    Raises:
        ValueError: Si n est négatif.
    """
    if n < 0:
        raise ValueError("Le nombre doit être positif ou nul.")
    if n in (0, 1):
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
