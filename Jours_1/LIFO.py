class LIFOStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        """Ajoute un élément au sommet de la pile."""
        self.stack.append(item)

    def pop(self):
        """Retire et retourne l'élément au sommet de la pile (le plus récent)."""
        if self.is_empty():
            raise IndexError("La pile est vide")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def __str__(self):
        return str(self.stack)

# Exemple d'utilisation
lifo = LIFOStack()
lifo.push("A")
lifo.push("B")
lifo.push("C")
print("Pile après ajouts :", lifo)

print("Retrait :", lifo.pop())
print("Pile après retrait :", lifo)

print("Retrait :", lifo.pop())
print("Pile après retrait :", lifo)

print("Retrait :", lifo.pop())
print("Pile après retrait :", lifo)
