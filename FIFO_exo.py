from collections import deque
from dataclasses import dataclass
from typing import Any

class Queue:
    """
    Implémentation d'une file (FIFO - First In First Out).
    Utilise une deque pour stocker les éléments.
    """
    def __init__(self):
        """Initialise une nouvelle file vide."""
        self.items = deque()
    
    def enqueue(self, item):
        """
        Ajoute un élément à la fin de la file.
        Args:
            item: L'élément à ajouter
        """
        self.items.append(item)
    
    def dequeue(self):
        """
        Retire et retourne le premier élément de la file.
        Returns:
            Le premier élément ou None si la file est vide
        """
        return self.items.popleft() if not self.is_empty() else None
    
    def is_empty(self):
        """
        Vérifie si la file est vide.
        Returns:
            bool: True si la file est vide, False sinon
        """
        return len(self.items) == 0
    
    def size(self):
        """
        Retourne le nombre d'éléments dans la file.
        Returns:
            int: Le nombre d'éléments
        """
        return len(self.items)

def create_queue_with_numbers():
    """Create a queue and add 5 numbers"""
    queue = Queue()
    numbers = [10, 20, 30, 40, 50]
    
    for num in numbers:
        queue.enqueue(num)
        print(f"Ajouté: {num}")
    
    return queue

def process_queue_elements(queue):
    """Remove and display all elements"""
    print("\nTraitement des éléments:")
    while not queue.is_empty():
        print(f"Retiré: {queue.dequeue()}")

def reverse_queue_with_stack(queue):
    """Inverse l'ordre des éléments d'une Queue en utilisant une Stack."""
    stack = []
    # vider la queue dans la pile
    while not queue.is_empty():
        stack.append(queue.dequeue())
    # remettre les éléments dans la queue depuis la pile (ordre inversé)
    while stack:
        queue.enqueue(stack.pop())

@dataclass
class Customer:
    id: int
    name: str
    service_type: str

def simulate_customer_service_system():
    """Simulate a customer service system"""
    service_queue = Queue()
    
    # Add some customers
    customers = [
        Customer(1, "Alice", "Dépôt"),
        Customer(2, "Bob", "Retrait"),
        Customer(3, "Charlie", "Information"),
        Customer(4, "David", "Dépôt")
    ]
    
    # Add customers to queue
    for customer in customers:
        service_queue.enqueue(customer)
        print(f"Client ajouté: {customer.name} - Service: {customer.service_type}")
    
    # Serve customers
    print("\nTraitement des clients:")
    while not service_queue.is_empty():
        customer = service_queue.dequeue()
        print(f"En train de servir: {customer.name} - Service: {customer.service_type}")

if __name__ == "__main__":
    # Test create_queue_with_numbers & process_queue_elements
    queue = create_queue_with_numbers()
    process_queue_elements(queue)
    
    # Test simulate_customer_service_system
    print("\nSimulation du système de service client:")
    simulate_customer_service_system()

    # New: démonstration - inverser une queue avec une stack
    print("\nExercice avancé - Inverser une queue avec une stack:")
    q = Queue()
    for num in [1, 2, 3, 4, 5]:
        q.enqueue(num)
    print("File initiale :", list(q.items))
    reverse_queue_with_stack(q)
    print("File inversée :", list(q.items))
    print("Lecture des éléments après inversion :")
    while not q.is_empty():
        print(f"Retiré: {q.dequeue()}")
