import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class LinkedList<T> implements Iterable<T> {
    private static class Node<T> {
        T value;
        Node<T> next;

        Node(T value, Node<T> next) {
            this.value = value;
            this.next = next;
        }

        @Override
        public String toString() {
            return "Node(" + value + ")";
        }
    }

    private Node<T> head;
    private int size;

    public LinkedList() {
        head = null;
        size = 0;
    }

    public int size() {
        return size;
    }

    public void append(T value) {
        Node<T> newNode = new Node<>(value, null);
        if (head == null) {
            head = newNode;
        } else {
            Node<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }

    public void prepend(T value) {
        head = new Node<>(value, head);
        size++;
    }

    public boolean remove(T value) {
        Node<T> prev = null;
        Node<T> current = head;
        
        while (current != null) {
            if (current.value.equals(value)) {
                if (prev == null) {
                    head = current.next;
                } else {
                    prev.next = current.next;
                }
                size--;
                return true;
            }
            prev = current;
            current = current.next;
        }
        return false;
    }

    public List<T> toList() {
        List<T> result = new ArrayList<>();
        for (T value : this) {
            result.add(value);
        }
        return result;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private Node<T> current = head;

            @Override
            public boolean hasNext() {
                return current != null;
            }

            @Override
            public T next() {
                T value = current.value;
                current = current.next;
                return value;
            }
        };
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("LinkedList([");
        Iterator<T> it = iterator();
        while (it.hasNext()) {
            sb.append(it.next());
            if (it.hasNext()) {
                sb.append(", ");
            }
        }
        return sb.append("])").toString();
    }

    public static void main(String[] args) {
        LinkedList<Integer> list = new LinkedList<>();
        list.append(10);
        list.append(20);
        list.prepend(5);
        System.out.println(list);          // LinkedList([5, 10, 20])
        System.out.println(list.size());   // 3
        System.out.println(list.toList()); // [5, 10, 20]
    }
}
