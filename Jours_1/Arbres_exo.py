from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None

def build_sample_tree() -> Node:
    """Construire un petit Binary Search Tree (au moins 5 nœuds)."""
    # Structure:
    #         40
    #        /  \
    #      20    60
    #     /  \   /
    #   10   30 50
    root = Node(40)
    root.left = Node(20)
    root.right = Node(60)
    root.left.left = Node(10)
    root.left.right = Node(30)
    root.right.left = Node(50)
    return root

def inorder_traversal(node: Optional[Node]) -> None:
    """Parcours in-order (gauche, racine, droite) — affiche les valeurs séparées par un espace."""
    if node is None:
        return
    inorder_traversal(node.left)
    print(node.value, end=' ')
    inorder_traversal(node.right)

def search_bst(node: Optional[Node], value: int) -> Optional[Node]:
    """Recherche itérative d'une valeur dans un BST — retourne le Node ou None."""
    current = node
    while current:
        if value == current.value:
            return current
        elif value < current.value:
            current = current.left
        else:
            current = current.right
    return None

# New: functions to build a BST from numbers and return a sorted list
def insert_bst(root: Optional[Node], value: int) -> Node:
    """Insère une valeur dans le BST et retourne la racine."""
    if root is None:
        return Node(value)
    current = root
    while True:
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
                break
            current = current.left
        else:
            if current.right is None:
                current.right = Node(value)
                break
            current = current.right
    return root

def build_bst_from_list(values: list[int]) -> Optional[Node]:
    """Construit un BST à partir d'une liste de valeurs (ordre d'insertion préservé)."""
    root: Optional[Node] = None
    for v in values:
        root = insert_bst(root, v)
    return root

def bst_to_sorted_list(root: Optional[Node]) -> list[int]:
    """Retourne la liste triée des valeurs du BST (parcours in-order)."""
    result: list[int] = []
    def _inorder(n: Optional[Node]):
        if n is None:
            return
        _inorder(n.left)
        result.append(n.value)
        _inorder(n.right)