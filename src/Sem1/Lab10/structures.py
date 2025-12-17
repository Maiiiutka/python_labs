from collections import deque


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty Stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self):
        return len(self._data)


class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty Queue")
        return self._data.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self):
        return len(self._data)


s = Stack()
print("Stack empty:", s.is_empty())

s.push(10)
s.push(20)
s.push(30)
print("After pushes:", s)            # Stack([10, 20, 30])
print("Peek:", s.peek())             # 30

print("Pop:", s.pop())               # 30
print("Pop:", s.pop())               # 20
print("Pop:", s.pop())               # 10

print("Stack empty after pops:", s.is_empty())


print("\n=== TEST QUEUE ===")
q = Queue()
print("Queue empty:", q.is_empty())

q.enqueue("A")
q.enqueue("B")
q.enqueue("C")
print("After enqueue:", q)           # Queue(['A', 'B', 'C'])
print("Peek:", q.peek())             # A

print("Dequeue:", q.dequeue())       # A
print("Dequeue:", q.dequeue())       # B
print("Dequeue:", q.dequeue())       # C

print("Queue empty after dequeues:", q.is_empty())