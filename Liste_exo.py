from collections import deque

def create_and_display_numbers_list():
    """
    Crée et affiche une liste de nombres de 1 à 10.
    
    Returns:
        list: Liste des nombres de 1 à 10
    """
    numbers = list(range(1, 11))
    print("Exercise 1 - List of numbers:", numbers)
    return numbers

def remove_even_numbers(numbers):
    """
    Supprime tous les nombres pairs d'une liste.
    
    Args:
        numbers (list): Liste de nombres à filtrer
    
    Returns:
        list: Liste ne contenant que les nombres impairs
    """
    odd_numbers = [num for num in numbers if num % 2 != 0]
    print("Exercise 2 - List with odd numbers only:", odd_numbers)
    return odd_numbers

def reverse_list(numbers):
    """
    Inverse l'ordre des éléments dans une liste.
    
    Args:
        numbers (list): Liste à inverser
    
    Returns:
        list: Liste avec les éléments dans l'ordre inverse
    """
    reversed_numbers = numbers[::-1]
    print("Exercise 3 - Reversed list:", reversed_numbers)
    return reversed_numbers

class TicketQueue:
    """
    Système de gestion de file d'attente avec tickets numérotés.
    Utilise une deque pour simuler une file d'attente FIFO.
    """
    
    def __init__(self):
        self.queue = deque()
        self.ticket_number = 0
    
    def take_ticket(self):
        """
        Délivre un nouveau ticket et l'ajoute à la file d'attente.
        
        Returns:
            int: Numéro du ticket délivré
        """
        self.ticket_number += 1
        self.queue.append(self.ticket_number)
        return self.ticket_number
    
    def serve_next(self):
        """
        Sert le prochain client dans la file.
        
        Returns:
            int: Numéro du ticket servi ou None si la file est vide
        """
        if self.queue:
            return self.queue.popleft()
        return None
    
    def display_queue(self):
        """
        Affiche l'état actuel de la file d'attente.
        
        Returns:
            list: Liste des tickets en attente
        """
        return list(self.queue)

def demonstrate_ticket_queue_system():
    """Demonstrate the ticket queue system"""
    queue = TicketQueue()
    
    # Simulate people taking tickets
    for _ in range(5):
        print(f"Ticket taken: {queue.take_ticket()}")
    
    print("Current queue:", queue.display_queue())
    
    # Serve next two people
    print("Serving:", queue.serve_next())
    print("Serving:", queue.serve_next())
    
    print("Remaining queue:", queue.display_queue())

if __name__ == "__main__":
    # Run all exercises
    numbers = create_and_display_numbers_list()
    odd_numbers = remove_even_numbers(numbers)
    reversed_numbers = reverse_list(odd_numbers)
    print("\nExercise 4 - Ticket Queue System:")
    demonstrate_ticket_queue_system()
