class FIFOQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """Ajoute un élément à la fin de la file."""
        self.queue.append(item)

    def dequeue(self):
        """Retire et retourne l'élément en tête de la file (le plus ancien)."""
        if self.is_empty():
            raise IndexError("La file est vide")
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def __str__(self):
        return str(self.queue)

# Exemple d'utilisation
fifo = FIFOQueue()
fifo.enqueue("A")
fifo.enqueue("B")
fifo.enqueue("C")
print("File après ajouts :", fifo)

print("Retrait :", fifo.dequeue())
print("File après retrait :", fifo)

print("Retrait :", fifo.dequeue())
print("File après retrait :", fifo)

print("Retrait :", fifo.dequeue())
print("File après retrait :", fifo)
