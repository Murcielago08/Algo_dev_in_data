from typing import Any, Optional, Iterator

# liste_chaine.py
# Exemple simple d'une liste chaînée (singly linked list) en Python

class Node:
    def __init__(self, value: Any, next: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value!r})"

class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def append(self, value: Any) -> None:
        """Ajouter à la fin"""
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """Ajouter au début"""
        self.head = Node(value, self.head)
        self._size += 1

    def remove(self, value: Any) -> bool:
        """Supprimer la première occurrence de value. Retourne True si supprimé."""
        prev = None
        cur = self.head
        while cur:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def to_list(self) -> list:
        """Convertit en liste Python."""
        result = []
        cur = self.head
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result

    def __iter__(self) -> Iterator[Any]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def __repr__(self) -> str:
        return "LinkedList([" + ", ".join(repr(x) for x in self) + "])"

# Exemple d'utilisation
if __name__ == "__main__":
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.prepend(5)
    print(ll)          # LinkedList([5, 10, 20])
    print(len(ll))     # 3
    print(ll.to_list())# [5, 10, 20]