class MathUtils:
    """
    Module utilitaire regroupant des fonctions mathématiques :
    - factorial(n)
    - is_prime(n)
    - gcd(a, b)
    """

    @staticmethod
    def factorial(n: int) -> int:
        """Calcule le factoriel de n (n!)"""
        if n < 0:
            raise ValueError("Le nombre doit être positif ou nul.")
        if n in (0, 1):
            return 1

        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def is_prime(n: int) -> bool:
        """Vérifie si n est un nombre premier."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calcule le plus grand commun diviseur (algorithme d'Euclide)."""
        while b:
            a, b = b, a % b
        return abs(a)
