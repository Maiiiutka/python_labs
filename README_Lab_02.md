# ЛР2 — Коллекции и матрицы (list/tuple/set/dict)

## Цели и результат
- Освоить операции над списками, кортежами, множествами и словарями.
- Научиться работать с 2D-списками (матрицами) — транспонирование, суммы по строкам/столбцам.
- Аккуратно форматировать текстовые представления записей (на примере студента).
---

## Требования и ограничения
- **Только стандартная библиотека Python** (без `numpy/pandas`, и т. п.).
- Версия Python: **3.11+**.
- Стиль: имена в `snake_case`, докстринги у функций, простые проверки входных данных.
- Ввод/вывод — через примеры в `README.md` (см. тест-кейсы).
- Желательно вынести переиспользуемые функции в `src/lib/` — пригодятся в следующих ЛР.

---

## Задание 1 — `arrays.py`
Реализуйте функции:

1. `min_max(nums: list[float | int]) -> tuple[float | int, float | int]`  
   Вернуть кортеж `(минимум, максимум)`. Если список пуст — `ValueError`.

2. `unique_sorted(nums: list[float | int]) -> list[float | int]`  
   Вернуть **отсортированный** список **уникальных** значений (по возрастанию).

3. `flatten(mat: list[list | tuple]) -> list`  
   «Расплющить» список списков/кортежей в один список по строкам (row-major).
   Если встретилась строка/элемент, который не является списком/кортежем — `TypeError`.

### Тест-кейсы (минимум)
**min_max**
- `[3, -1, 5, 5, 0]` → `(-1, 5)`
- `[42]` → `(42, 42)`
- `[-5, -2, -9]` → `(-9, -2)`
- `[]` → `ValueError`
- `[1.5, 2, 2.0, -3.1]` → `(-3.1, 2)`

**unique_sorted**
- `[3, 1, 2, 1, 3]` → `[1, 2, 3]`
- `[]` → `[]`
- `[-1, -1, 0, 2, 2]` → `[-1, 0, 2]`
- `[1.0, 1, 2.5, 2.5, 0]` → `[0, 1.0, 2.5]` *(допускаем смешение int/float)*

**flatten**
- `[[1, 2], [3, 4]]` → `[1, 2, 3, 4]`
- `[[1, 2], (3, 4, 5)]` → `[1, 2, 3, 4, 5]`
- `[[1], [], [2, 3]]` → `[1, 2, 3]`
- `[[1, 2], "ab"]` → `TypeError` *(«строка не строка строк матрицы»)*

---

*Code*

```
import sys
def min_max(nums: list[float | int]): 
    return float(min(nums)) if float(min(nums)) % 1 != 0 else int(min(nums)) ,float(max(nums)) if float(max(nums)) % 1 != 0 else int(max(nums))

def unique_sorted(nums: list[float | int]):
    return sorted(set(nums))

def flatten(mat: list[list | tuple]):
    result = []
    for item in mat:
        result.extend(item)
    return result

buk = "abcdefghijklmnopqrstuvwxyz"
cif = "0123456789"

print("What function you are going to use?")
print("min_max - 1, unique_sorted - 2, flatten - 3")
c = int(input())
if c == 1 or c == 2:
    print("Write your numbers in one line with spaces")
    m = []
    d = input().replace(",", " ").split()
    for i in range(len(d)):
        m.append(int(d[i]) if d[i].count(".") == 0 else float(d[i]))

s = []
if c == 3:
    print("how many lists you want, write number")
    z = input()
    if str(z) not in cif:
        print("ValueError")
        sys.exit() 
    z = int(z)
    print(f"write numbers in one line {z} times")
    for j in range(z):
        l = []
        y = input().replace(","," ").split()
        for v in range(len(y)):
            if str(y[v]) in buk:
                print("TypeError")
                sys.exit() 
            if y[v].count("0") == 0 and y[v].count("1") == 0 and y[v].count("2") == 0 and y[v].count("3") == 0 and y[v].count("4") == 0 and y[v].count("5") == 0 and y[v].count("6") == 0 and y[v].count("7") == 0 and y[v].count("8") == 0 and y[v].count("9") == 0:
                break
            l.append(int(y[v]) if y[v].count(".") == 0 else float(y[v]))
        s.append(l)




if c == 1:
    print(min_max(m) if len(m) > 0 else "ErrorValue")
elif c == 2:
        print(unique_sorted(m) if len(m) > 0 else [])
else:
    print(flatten(s))
```

*Screen*

<img width="624" height="452" alt="Arrays" src="https://github.com/user-attachments/assets/fdf07b1a-4e3e-4574-8f52-1392d1300420" />

<img width="1094" height="871" alt="image" src="https://github.com/user-attachments/assets/f868c1e7-ec8e-40d9-aa72-c1ecd0f78276" />

<img width="1045" height="846" alt="image" src="https://github.com/user-attachments/assets/b1d8ab32-e1e1-4eec-9c98-02bd55a69a5e" />

---

## Задание B — `matrix.py`
Реализуйте функции (для **прямоугольных** матриц — одинаковая длина строк):

1. `transpose(mat: list[list[float | int]]) -> list[list]`  
   Поменять строки и столбцы местами. Пустая матрица `[]` → `[]`.  
   Если матрица «рваная» (строки разной длины) — `ValueError`.

2. `row_sums(mat: list[list[float | int]]) -> list[float]`  
   Сумма по каждой строке. Требуется прямоугольность (см. выше).

3. `col_sums(mat: list[list[float | int]]) -> list[float]`  
   Сумма по каждому столбцу. Требуется прямоугольность.

### Тест-кейсы (минимум)
**transpose**
- `[[1, 2, 3]]` → `[[1], [2], [3]]`
- `[[1], [2], [3]]` → `[[1, 2, 3]]`
- `[[1, 2], [3, 4]]` → `[[1, 3], [2, 4]]`
- `[]` → `[]`
- `[[1, 2], [3]]` → `ValueError` (рваная матрица)

**row_sums**
- `[[1, 2, 3], [4, 5, 6]]` → `[6, 15]`
- `[[-1, 1], [10, -10]]` → `[0, 0]`
- `[[0, 0], [0, 0]]` → `[0, 0]`
- `[[1, 2], [3]]` → `ValueError` (рваная)

**col_sums**
- `[[1, 2, 3], [4, 5, 6]]` → `[5, 7, 9]`
- `[[-1, 1], [10, -10]]` → `[9, -9]`
- `[[0, 0], [0, 0]]` → `[0, 0]`
- `[[1, 2], [3]]` → `ValueError` (рваная)

---

*Code*

```

def transpose(mat: list[list[float | int]]):
    result = []
    if mat == []:
        return []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ValueError"
    for i in range(len(mat[0])):
        new_mat = []
        for j in range(len(mat)):
            new_mat.append(mat[j][i])
        result.append(new_mat)
    return result

def row_sums(mat: list[list[float | int]]):
    result = []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ErrorValue"
    if mat == []:
        return []
    for i in range(len(mat)):
        s = sum(mat[i])
        result.append(s)
    return result 

def col_sums(mat: list[list[float | int]]):
    result = []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ValueError"
    for i in range(len(mat[0])):
        new_mat = 0
        for j in range(len(mat)):
            new_mat += mat[j][i]
        result.append(new_mat)
    return result 

print(transpose([[1, 2], [3, 4]]))
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[1, 2, 3], [4, 5, 6]]))

```

*Screen*

<img width="1214" height="862" alt="image" src="https://github.com/user-attachments/assets/31d99ad6-aeb1-42ff-b076-e89561d97a60" />

---

## Задание C — `tuples.py`
Работаем с «записями» как с кортежами.

1. Определите тип записи студента как кортеж:  
   `(fio: str, group: str, gpa: float)`

2. Реализуйте `format_record(rec: tuple[str, str, float]) -> str`  
   Вернуть строку вида:  
   `Иванов И.И., гр. BIVT-25, GPA 4.60`  
   **Правила:**
   - ФИО может быть `«Фамилия Имя Отчество»` или `«Фамилия Имя»` — инициалы формируются из 1–2 имён (в верхнем регистре).
   - Лишние пробелы нужно убрать (`strip`, «схлопнуть» внутри).
   - GPA печатается с **2 знаками** (округление правилами Python).

### Тест-кейсы (минимум)
- `("Иванов Иван Иванович", "BIVT-25", 4.6)` → `"Иванов И.И., гр. BIVT-25, GPA 4.60"`
- `("Петров Пётр", "IKBO-12", 5.0)` → `"Петров П., гр. IKBO-12, GPA 5.00"`
- `("Петров Пётр Петрович", "IKBO-12", 5.0)` → `"Петров П.П., гр. IKBO-12, GPA 5.00"`
- `("  сидорова  анна   сергеевна ", "ABB-01", 3.999)` → `"Сидорова А.С., гр. ABB-01, GPA 4.00"`
- Некорректные записи (пустое ФИО, пустая группа, неверный тип GPA) → `ValueError`/`TypeError` по усмотрению (описать в докстринге).

---

*Code*

```

buk = "abcdefghijklmnopqrstuvwxyz"
def format_record(rec: tuple[str, str, float]):
    result = []
    FIO = rec[0].split()
    FIO_LEN = len(FIO)
    if FIO_LEN == 0:
        return "ValueError"
    elif FIO_LEN == 3:
        c = rec[0].split()
        second = c[1][0] + "."
        third = c[2][0] + "."
        NEW_FIO = c[0][0].upper() + c[0][1:].lower() + " " + second.upper() + third.upper()
    elif FIO_LEN == 2:
        c = rec[0].split()
        second = c[1][0] + "."
        NEW_FIO = c[0][0].upper() + c[0][1:].lower() + " " + second.upper()
    result.append(NEW_FIO)
    if rec[1] == "":
        return "ValueError"
    else:
        NEW_GROUP = "гр." + " " + rec[1]
    result.append(NEW_GROUP)
    GPU_STR = str(rec[2])
    for j in GPU_STR:
        if GPU_STR.count(".") == 1:
            if j not in buk:
                NEW_GPU = f"GPU {round(float(rec[2]), 2):.2f}"
        else:
            return "ErrorValue"
    result.append(NEW_GPU)
    return result[0] +"," + " " + result[1]+ "," + " " +result[2]


print(format_record(("ИВАНОВ ИВАН ИВАНОВИЧ", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))

```

*Screen*

<img width="1091" height="870" alt="image" src="https://github.com/user-attachments/assets/051a723b-a052-4c27-84ce-14f7fee67314" />

---
