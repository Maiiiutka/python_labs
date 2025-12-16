# ЛР10 — Структуры данных: Stack, Queue, Linked List и бенчмарки

> **Цель:** реализовать базовые структуры данных (стек, очередь, связный список),
> сравнить их производительность и научиться думать в терминах асимптотики (O(1), O(n)).  

---

## Результат ЛР

После выполнения ЛР10 в репозитории должны появиться:

### `src/lab10/structures.py`

Реализация:
- `class Stack` — стек на базе `list`:
- `class Queue` — очередь на базе `collections.deque`:

---

### `src/lab10/linked_list.py`
Реализация:
- `class Node` — узел односвязного списка
- `class SinglyLinkedList` — **односвязный список**.

---

### `lab10/README.md`

Отчёт по ЛР10 должен содержать:

- краткую теорию:
  - что такое стек / очередь / связный список
  - типичные операции и их сложность
- описание реализованных классов **с примерами использования**
- выводы по бенчмаркам:
  - какая структура медленнее/быстрее и **почему**

---

### `images/lab10/`

Скриншоты:
- примеры использования структур в интерпретаторе через `python -m`

---

## Рекомендуемая структура репозитория

```text
python_labs/
├─ README.md
├─ src/
│   ├─ lab08/
│   ├─ lab09/
│   └─ lab10/
│       ├─ structures.py      # Stack и Queue
│       └─ linked_list.py     # SinglyLinkedList 
├─ data
└─ images/
    └─ lab10/
```

## Теоретическая часть
[клииик](./THEORY.md)

## Задание

### A. Реализовать `Stack` и `Queue` (`src/lab10/structures.py`)

Нужно реализовать два класса: `Stack` и `Queue`.

#### `class Stack`

**Назначение:** структура данных «стек» (LIFO) на базе `list`.

**Атрибуты:**

- `self._data: list[Any]` — внутренний список для хранения элементов стека.  
  Семантика: вершина стека — последний элемент списка (`self._data[-1]`).

**Методы (минимум):**

- `push(item) -> None`  
  Добавить элемент на вершину стека.

- `pop() -> Any`  
  Снять верхний элемент стека и вернуть его.  
  Если стек пуст — выбросить понятное исключение (например, `IndexError` с вменяемым сообщением).

- `peek() -> Any | None`  
  Вернуть верхний элемент **без удаления**.  
  Если стек пуст — вернуть `None` (или тоже бросать исключение, но тогда это нужно описать в README).

- `is_empty() -> bool`  
  Вернуть `True`, если стек пуст, иначе `False`.

- (опционально) `__len__(self) -> int` — количество элементов в стеке.

---

#### `class Queue`

**Назначение:** структура данных «очередь» (FIFO) на базе `collections.deque`.

**Атрибуты:**

- `self._data: deque[Any]` — двусторонняя очередь из `collections.deque`.  
  Семантика: голова очереди — левый край структуры, `dequeue` берёт элементы слева.

**Методы (минимум):**

- `enqueue(item) -> None`  
  Добавить элемент в конец очереди.

- `dequeue() -> Any`  
  Взять элемент из начала очереди и вернуть его.  
  Если очередь пустая — выбросить понятное исключение (например, `IndexError`).

- `peek() -> Any | None`  
  Вернуть первый элемент **без удаления**.  
  Если очередь пустая — вернуть `None` (или бросить исключение, но это нужно явно описать).

- `is_empty() -> bool`  
  Вернуть `True`, если очередь пуста.

- (опционально) `__len__(self) -> int` — количество элементов в очереди.

---

Code

```
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
```

---
Screen
---
<img width="328" height="151" alt="image" src="https://github.com/user-attachments/assets/28f6b1fc-a3ae-45a5-ac7c-0b078ed6db66" />



### B. Реализовать `SinglyLinkedList` (`src/lab10/linked_list.py`)

Нужно реализовать односвязный список и его узел.

#### `class Node`

**Назначение:** узел односвязного списка.

**Атрибуты:**

- `self.value: Any` — значение элемента.
- `self.next: Node | None` — ссылка на следующий узел или `None`, если это последний узел.

---

#### `class SinglyLinkedList`

**Назначение:** односвязный список, состоящий из узлов `Node`.

**Атрибуты:**

- `self.head: Node | None` — голова списка (первый элемент) или `None`, если список пуст.
- (опционально) `self.tail: Node | None` — хвост списка (последний элемент) для ускорения `append`.
- `self._size: int` — количество элементов в списке.

**Методы (минимум):**

- `append(value) -> None`  
  Добавить элемент в конец списка.  
  При наличии `tail` — за `O(1)`, без него — допустимо `O(n)` проходом от `head`.

- `prepend(value) -> None`  
  Добавить элемент в начало списка за `O(1)`.

- `insert(idx: int, value) -> None`  
  Вставить элемент по индексу `idx`.  
  Требования:
  - допускается вставка в начало (`idx == 0`) и в конец (`idx == len(list)`);
  - при индексе вне диапазона `[0, len(list)]` — выбросить `IndexError`.

- `remove(value) -> None` **или** `remove_at(idx: int) -> None`  
  На выбор:
  - либо удалить **первое вхождение** значения `value` (если нет — можно ничего не делать или бросать исключение, задокументировав поведение);
  - либо удалить элемент по индексу `idx` (при некорректном индексе — `IndexError`).

- `__iter__(self)`  
  Возвращает итератор по значениям в списке (в порядке от головы к хвосту).

- `__len__(self) -> int`  
  Возвращает количество элементов (`self._size`).

- `__repr__(self) -> str`  
  Возвращает строковое представление, например:  
  `SinglyLinkedList([1, 2, 3])`.

---

Code

```
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
```

---
Screen
---
<img width="340" height="152" alt="image" src="https://github.com/user-attachments/assets/97c20c79-27e2-4fd4-8add-751752e0fc50" />
