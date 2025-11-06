class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def preorder(self, node, result=None):
        """Parcours RGD (Racine-Gauche-Droite)"""
        if result is None:
            result = []
        if node:
            result.append(node.value)  # Racine
            self.preorder(node.left, result)  # Gauche
            self.preorder(node.right, result)  # Droite
        return result

    def inorder(self, node, result=None):
        """Parcours GRD (Gauche-Racine-Droite)"""
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)  # Gauche
            result.append(node.value)  # Racine
            self.inorder(node.right, result)  # Droite
        return result

    def postorder(self, node, result=None):
        """Parcours GDR (Gauche-Droite-Racine)"""
        if result is None:
            result = []
        if node:
            self.postorder(node.left, result)  # Gauche
            self.postorder(node.right, result)  # Droite
            result.append(node.value)  # Racine
        return result

# Exemple d'utilisation
tree = BinaryTree()
tree.root = Node(1)
tree.root.left = Node(2)
tree.root.right = Node(3)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)

print("Arbre créé avec la structure suivante:")
print("       1")
print("      / \\")
print("     2   3")
print("    / \\")
print("   4   5")

print("\nParcours RGD (Preorder)  :", tree.preorder(tree.root))
print("Parcours GRD (Inorder)   :", tree.inorder(tree.root))
print("Parcours GDR (Postorder) :", tree.postorder(tree.root))
