from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Node:
    """
    Représente un nœud dans la liste chaînée circulaire.
    
    Attributes:
        value: Valeur stockée dans le nœud
        next: Référence vers le nœud suivant
    """
    value: Any
    next: Optional['Node'] = None

class CircularLinkedList:
    """
    Implémentation d'une liste chaînée circulaire.
    La liste maintient une référence vers le premier élément (head) et forme un cercle.
    """
    
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0
    
    def append(self, value: Any) -> None:
        """
        Ajoute un nouvel élément à la fin de la liste.
        
        Args:
            value: Valeur à ajouter dans la liste
        """
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
        self.size += 1
    
    def rotate(self) -> None:
        """
        Fait une rotation de la liste d'une position vers la droite.
        Le deuxième élément devient le premier, et le premier devient le dernier.
        """
        if self.head and self.head.next != self.head:
            self.head = self.head.next
    
    def display(self) -> None:
        """
        Affiche tous les éléments de la liste dans l'ordre.
        Le format d'affichage est: valeur1 -> valeur2 -> ... -> (retour au début)
        """
        if not self.head:
            return
        current = self.head
        while True:
            print(current.value, end=" -> ")
            current = current.next
            if current == self.head:
                break
        print("(retour au début)")

def simulate_player_rotation():
    """
    Simule un jeu de rotation avec des joueurs dans un cercle.
    Crée une liste de joueurs et effectue plusieurs rotations pour
    démontrer le fonctionnement de la liste circulaire.
    """
    players = CircularLinkedList()
    player_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    
    print("Ajout des joueurs au cercle:")
    for name in player_names:
        players.append(name)
        print(f"Joueur {name} ajouté")
    
    print("\nPosition initiale:")
    players.display()
    
    print("\nSimulation de 3 tours de rotation:")
    for i in range(3):
        players.rotate()
        print(f"\nAprès rotation {i+1}:")
        players.display()

if __name__ == "__main__":
    simulate_player_rotation()
