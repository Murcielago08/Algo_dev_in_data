class Stack:
    """
    Implémentation d'une pile (LIFO - Last In First Out).
    """
    def __init__(self):
        """Initialise une nouvelle pile vide."""
        self.items = []
    
    def push(self, item):
        """
        Empile un nouvel élément au sommet de la pile.
        
        Args:
            item: L'élément à empiler
        """
        self.items.append(item)
    
    def pop(self):
        """
        Retire et retourne l'élément au sommet de la pile.
        
        Returns:
            L'élément au sommet ou None si la pile est vide
        """
        return self.items.pop() if not self.is_empty() else None
    
    def is_empty(self):
        """
        Vérifie si la pile est vide.
        
        Returns:
            bool: True si la pile est vide, False sinon
        """
        return len(self.items) == 0
    
    def peek(self):
        """
        Consulte l'élément au sommet sans le retirer.
        
        Returns:
            L'élément au sommet ou None si la pile est vide
        """
        return self.items[-1] if not self.is_empty() else None

def stack_days_of_week():
    """Stack days of the week"""
    stack = Stack()
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    for day in days:
        stack.push(day)
        print(f"Empilé: {day}")
    
    return stack

def unstack_and_display_elements(stack):
    """Unstack and display all elements"""
    print("\nDépilage des éléments:")
    while not stack.is_empty():
        print(f"Dépilé: {stack.pop()}")

def are_parentheses_balanced(expression):
    """
    Vérifie si les parenthèses dans une expression sont bien équilibrées.
    
    Args:
        expression (str): L'expression à vérifier
    
    Returns:
        bool: True si les parenthèses sont équilibrées, False sinon
        
    Examples:
        >>> are_parentheses_balanced("((()))")
        True
        >>> are_parentheses_balanced("(()")
        False
    """
    stack = Stack()
    
    for char in expression:
        if char == '(':
            stack.push(char)
        elif char == ')':
            if stack.is_empty():
                return False
            stack.pop()
    
    return stack.is_empty()

if __name__ == "__main__":
    # Test stack_days_of_week & unstack_and_display_elements
    stack = stack_days_of_week()
    unstack_and_display_elements(stack)
    
    # Test are_parentheses_balanced
    print("\nTest des expressions parenthésées:")
    expressions = ["((()))", "(()", ")(", "(()())"]
    for expr in expressions:
        print(f"'{expr}' est {'équilibrée' if are_parentheses_balanced(expr) else 'non équilibrée'}")
