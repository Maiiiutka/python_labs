from collections import deque

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self._size += 1
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node
        self._size += 1

    def prepend(self, value):
        new_node = Node(value, next=self.head)
        self.head = new_node
        self._size += 1

    def insert(self, idx, value):
        if idx < 0 or idx > self._size:
            raise IndexError("index out of range")

        if idx == 0:
            self.prepend(value)
            return

        if idx == self._size:
            self.append(value)
            return

        current = self.head
        for _ in range(idx - 1):
            current = current.next

        new_node = Node(value, next=current.next)
        current.next = new_node
        self._size += 1

    def remove_at(self, idx):
        if idx < 0 or idx >= self._size:
            raise IndexError("index out of range")

        if idx == 0:
            removed = self.head
            self.head = self.head.next
            self._size -= 1
            return removed.value

        current = self.head
        for _ in range(idx - 1):
            current = current.next

        removed = current.next
        current.next = removed.next
        self._size -= 1
        return removed.value

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"SinglyLinkedList({list(self)})"
    

print("=== TEST LINKED LIST ===")
lst = SinglyLinkedList()

print("Empty list:", list(lst), "size =", len(lst))

# append
lst.append(10)
lst.append(20)
lst.append(30)
print("After append:", list(lst), "size =", len(lst))

# prepend
lst.prepend(5)
print("After prepend:", list(lst), "size =", len(lst))

# insert in middle
lst.insert(2, 15)  # [5, 10, 15, 20, 30]
print("After insert idx=2:", list(lst), "size =", len(lst))

# insert at start
lst.insert(0, 1)
print("After insert idx=0:", list(lst))

# insert at end
lst.insert(len(lst), 40)
print("After insert at end:", list(lst))

# remove_at
removed = lst.remove_at(3)
print(f"Removed index 3 ({removed}) →", list(lst), "size =", len(lst))

# iteration test
print("Iterate values:")
for value in lst:
    print(" ->", value)