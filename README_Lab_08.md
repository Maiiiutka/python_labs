# ЛР8 – ООП в Python: `@dataclass Student`, методы и сериализация

> **Цель:** изучить основы объектно-ориентированного программирования в Python,
> научиться описывать модели данных с помощью @dataclass, реализовывать методы 
> и валидацию, сериализовывать/десериализовывать объекты.\
> **Связь:** продолжаем работу с файлами и сериализацией из ЛР5, логику структуры 
> и оформления наследуем из предыдущих ЛР.
> Основная задача — реализовать полноценную модель студента, экспорт/импорт в JSON и корректные
> методы экземпляра.
___
## Результат ЛР

После выполнения ЛР8 в репозитории должны присутствовать:

### `src/lab08/models.py`
Модель **`Student`**, содержащая:

- декоратор `@dataclass`
- поля:
  - `fio`
  - `birthdate`
  - `group`
  - `gpa`
- методы:
  - `age()`
  - `to_dict()`
  - `from_dict()`
  - `__str__()`
- валидацию:
  - формата даты (`YYYY-MM-DD`)
  - диапазона среднего балла `0 ≤ gpa ≤ 5`

---

### `src/lab08/serialize.py`

Функции сериализации:

- `students_to_json(list[Student], path)`
- `students_from_json(path) -> list[Student]`

---

### `data/lab08/`

Должны находиться:

- пример входного JSON (`students_input.json`)
- пример выходного JSON (результат сериализации, `students_output.json`)

---

### `lab08/README.md`

Файл отчёта должен содержать:

- примеры запуска функций
- примеры JSON **до/после преобразования**
- описание структуры класса `Student` и логики его методов

---

## Структура репозитория (рекомендация)
```
python_labs/
├─ README.md                        # Общий отчет
├─ src/
│   ├─ lib
│   ├─ lab08/
|   |   ├─ models.py
|   |   ├─ serialize.py
│   │   ├─ _ _init_ _.py
|   └─  └─ README.md                # Отчет по ЛР8            
├─ data/
│   └─ lab08/
│       ├─ students_input.json
│       └─ students_output.json
├─ images /
    └── lab08
```

---

## Теоретическая часть: краткая справка по ООП в Python

### Классы и объекты

Python — динамический язык, но отлично поддерживает ООП:

``` python
class A:
    def hello(self):
        return "hi"
```

### Инкапсуляция

Python использует соглашения: 
 - `_field`  – защищённое
 - `__field` – приватное (name mangling)

### Декоратор @dataclass
Автоматически создаёт: 
 - `__init__` 
 - `__repr__` 
 - `__eq__` 
 - (опционально) `order=True`, `frozen=True`

Пример:

``` python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

### Сериализация

Python → словарь → JSON:

``` python
import json
json.dumps(obj)
```

---

## Задание

### A. Реализовать класс `Student` (`models.py`)

### Поля:

| Поле       | Тип   | Описание                |
|------------|-------|--------------------------|
| `fio`      | `str` | ФИО студента             |
| `birthdate`| `str` | Формат `YYYY-MM-DD`      |
| `group`    | `str` | Группа, напр. `SE-01`    |
| `gpa`      | `float` | Средний балл 0…5       |

---

### Методы:

- `age()` — вернуть количество полных лет  
- `to_dict()` — сериализация  
- `from_dict()` — десериализация  
- `__str__()` — красивый вывод  

---

### Валидация в `__post_init__`:

- корректный формат даты  
- диапазон `gpa`
---

Code
```
from dataclasses import dataclass, fields
from datetime import date, datetime
import json
from typing import Dict, Any


@dataclass
class Student:
    fio: str
    birthdate: str  # формат YYYY-MM-DD
    group: str
    gpa: float

    def __post_init__(self):
        # Валидация даты рождения
        try:
            datetime.strptime(self.birthdate, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD")

        # Валидация среднего балла
        if not 0 <= self.gpa <= 5:
            raise ValueError("GPA должен быть в диапазоне от 0 до 5")

    def age(self) -> int:
        """Возвращает количество полных лет на текущую дату"""
        birth_date = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
        today = date.today()

        # Вычисляю разницу в годах
        age_years = today.year - birth_date.year

        # Корректирую, если день рождения в этом году ещё не наступил
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age_years -= 1

        return age_years

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь"""
        return {
            'fio': self.fio,
            'birthdate': self.birthdate,
            'group': self.group,
            'gpa': self.gpa
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Десериализация из словаря"""
        # Фильтрую только нужные поля
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def __str__(self) -> str:
        """Красивый строковый вывод"""
        return (f"Студент: {self.fio}\n"
                f"Дата рождения: {self.birthdate} (Возраст: {self.age()} лет)\n"
                f"Группа: {self.group}\n"
                f"Средний балл: {self.gpa:.2f}")


# Пример использования
if __name__ == "__main__":
    # Создание объекта
    student1 = Student(
        fio="Иванов Иван Иванович",
        birthdate="2000-05-15",
        group="SE-01",
        gpa=4.2
    )

    print("Объект студента:")
    print(student1)
    print()

    # Сериализация в словарь
    student_dict = student1.to_dict()
    print("Словарь:", student_dict)

    # Сериализация в JSON
    student_json = json.dumps(student_dict, ensure_ascii=False, indent=2)
    print("JSON:")
    print(student_json)
    print()

    # Десериализация из словаря
    student2 = Student.from_dict(student_dict)
    print("Восстановленный объект:")
    print(student2)
    print()

    # Проверка валидации
    try:
        Student(fio="Тест", birthdate="2020-20-20", group="SE-01", gpa=4.0)
    except ValueError as e:
        print(f"Ошибка валидации даты: {e}")

    try:
        Student(fio="Тест", birthdate="2000-01-01", group="SE-01", gpa=6.0)
    except ValueError as e:
        print(f"Ошибка валидации GPA: {e}")
```

#### Основные моменты реализации

@dataclass: автоматически генерирует init, repr, eq методы.

post_init: Выполняется после инициализации, используется для валидации:

проверка формата даты с помощью datetime.strptime();

проверка диапазона GPA.

age(): вычисляет полные годы на текущую дату с учётом месяца и дня рождения.

to_dict(): преобразует объект в словарь для последующей сериализации в JSON.

from_dict(): классовый метод для создания объекта из словаря (альтернативный конструктор).

str(): возвращает форматированную строку с читаемым представлением объекта.

#### Валидация:

дата должна быть в формате YYYY-MM-DD;

GPA должен быть в диапазоне 0-5.

---
Screen
---
<img width="1186" height="574" alt="image" src="https://github.com/user-attachments/assets/c23965f3-9f68-4e4c-8fb9-ce6ee76d4f76" />



### B. Реализовать модуль `serialize.py`

#### `students_to_json(students, path)`

Сохраняет список студентов в JSON.

#### `students_from_json(path) -> list[Student]`

-   читает JSON-массив
-   валидирует
-   создаёт список `Student`

---

## Пример кода

### `models.py`

``` python
# imports

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        # TODO: добавить нормальную валидацию формата даты и диапазона gpa
        try:
            datetime.strptime(self.birthdate, "%Y/%m/%d")
        except ValueError:
            # (по-хорошему, тут должен быть raise ValueError(...))
            print("warning: birthdate format might be invalid")
        
        if not (0 <= self.gpa <= 10):
            raise ValueError("gpa must be between 0 and 10")

    def age(self) -> int:
        # TODO: добавить нормальную валидацию формата даты и диапазона gpa
        b = dself.birthdate
        today = date.today()
        return today.year - b.year

    def to_dict(self) -> dict:
        # TODO: проверить полноценность полей
        return {
            "fio": self.birthdate,
            "birthdate": self.group,
            "gpa": self.fio,
        }

    @classmethod
    def from_dict(cls, d: dict):
        # TODO: реализовать десереализацию из словаря
        return class

    def __str__(self):
        # TODO: f"{}, {}, {}"
        return self.fio, self.group, self.gpa
```

### `serialize.py`

``` python
# imports

def students_to_json(students, path):
    data = [s.to_dict() for s in students]
    json.dumps(data, ensure_ascii=False, indent=2)

def students_from_json(path):
    return []
```

---

Code

```
import json
from typing import List, Optional
from models import Student


def students_to_json(students: List[Student], path: str) -> None:
    """
    Сохраняет список студентов в JSON-файл.

    Args:
        students: Список объектов Student
        path: Путь к файлу для сохранения

    Raises:
        TypeError: Если передан не список или элементы не являются Student
        IOError: При ошибках записи в файл
    """
    if not isinstance(students, list):
        raise TypeError(f"Ожидается список, получен {type(students).__name__}")

    # Проверяю тип всех элементов
    for i, student in enumerate(students):
        if not isinstance(student, Student):
            raise TypeError(
                f"Элемент с индексом {i} не является объектом Student, "
                f"получен {type(student).__name__}"
            )

    # Сериализую всех студентов
    data = [student.to_dict() for student in students]

    # Записываю в файл
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise IOError(f"Ошибка записи в файл {path}: {str(e)}")


def students_from_json(path: str) -> List[Student]:
    """
    Читает JSON-массив из файла и создаёт список объектов Student.

    Args:
        path: Путь к JSON-файлу

    Returns:
        Список объектов Student

    Raises:
        IOError: При ошибках чтения файла
        json.JSONDecodeError: При невалидном JSON
        ValueError: При ошибках валидации данных студентов
        KeyError: При отсутствии обязательных полей
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except IOError as e:
        raise IOError(f"Ошибка чтения файла {path}: {str(e)}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Некорректный JSON в файле {path}",
            e.doc,
            e.pos
        )

    if not isinstance(data, list):
        raise TypeError(
            f"Ожидается JSON-массив, получен {type(data).__name__}"
        )

    students = []
    errors = []

    for i, item in enumerate(data):
        try:
            # Проверяю, что элемент является словарем
            if not isinstance(item, dict):
                raise TypeError(
                    f"Элемент с индексом {i} должен быть словарем, "
                    f"получен {type(item).__name__}"
                )

            # Создаю объект Student
            student = Student.from_dict(item)
            students.append(student)

        except (ValueError, TypeError, KeyError) as e:
            error_msg = f"Ошибка в элементе {i}: {str(e)}"
            errors.append(error_msg)

    # Если были ошибки при создании студентов, выбрасываю исключение
    if errors:
        error_summary = "\n".join(errors)
        raise ValueError(
            f"Не удалось создать всех студентов из файла {path}.\n"
            f"Ошибки:\n{error_summary}"
        )

    return students


# Пример использования
if __name__ == "__main__":
    # Создаю тестовых студентов
    test_students = [
        Student(
            fio="Иванов Иван Иванович",
            birthdate="2000-05-15",
            group="SE-01",
            gpa=4.2
        ),
        Student(
            fio="Петрова Мария Сергеевна",
            birthdate="2001-03-22",
            group="SE-02",
            gpa=4.8
        ),
        Student(
            fio="Сидоров Алексей Викторович",
            birthdate="1999-11-30",
            group="CS-01",
            gpa=3.9
        )
    ]

    # Тестирую сохранение в JSON
    print("Тестируем сохранение в JSON...")
    try:
        students_to_json(test_students, "students.json")
        print("Файл students.json успешно создан")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

    # Тестирую чтение из JSON
    print("\nТестируем чтение из JSON...")
    try:
        loaded_students = students_from_json("students.json")
        print(f"Успешно загружено {len(loaded_students)} студентов:")

        for student in loaded_students:
            print(f"- {student.fio} ({student.group}), GPA: {student.gpa}")

    except Exception as e:
        print(f"Ошибка при загрузке: {e}")

    # Тестирую обработку ошибок
    print("\nТестируем обработку ошибок...")

    # 1. Невалидный JSON
    try:
        with open("invalid.json", "w") as f:
            f.write("{это не валидный json}")
        students_from_json("invalid.json")
    except Exception as e:
        print(f"1. Невалидный JSON: {type(e).__name__}: {e}")

    # 2. JSON с неверной структурой (не список)
    try:
        with open("not_list.json", "w", encoding="utf-8") as f:
            json.dump({"name": "test"}, f)
        students_from_json("not_list.json")
    except Exception as e:
        print(f"2. JSON не список: {type(e).__name__}: {e}")

    # 3. JSON с неполными данными
    try:
        incomplete_data = [
            {"fio": "Тест", "birthdate": "2000-01-01", "group": "SE-01"},
            # отсутствует поле gpa
        ]
        with open("incomplete.json", "w", encoding="utf-8") as f:
            json.dump(incomplete_data, f)
        students_from_json("incomplete.json")
    except Exception as e:
        print(f"3. Неполные данные: {type(e).__name__}: {e}")

    # 4. JSON с невалидными данными
    try:
        invalid_data = [
            {"fio": "Тест", "birthdate": "не дата", "group": "SE-01", "gpa": 4.0}
        ]
        with open("invalid_data.json", "w", encoding="utf-8") as f:
            json.dump(invalid_data, f)
        students_from_json("invalid_data.json")
    except Exception as e:
        print(f"4. Невалидные данные: {type(e).__name__}: {e}")
```
Основные особенности реализации
students_to_json(students, path):
Валидация входных данных: проверяет, что передан список и все элементы - объекты Student.

Сериализация: использует метод to_dict() каждого студента.

Обработка ошибок: перехватывает ошибки записи в файл.

Кодировка UTF-8: сохраняет кириллические символы корректно.

Человекочитаемый формат: использует indent=2 для красивого форматирования.

students_from_json(path) -> list[Student]:
Чтение и парсинг JSON: с обработкой ошибок файловой системы и синтаксиса JSON.

Валидация структуры: проверяет, что JSON содержит массив.

Поэлементная обработка: создает объекты Student из каждого словаря.

Сбор ошибок: накапливает все ошибки валидации, а не останавливается на первой.

Комплексная обработка ошибок: включает проверку типов, обязательных полей и бизнес-логики.

Особенности обработки ошибок
Гранулярные исключения: разные типы ошибок (IO, JSON, валидация).

Информативные сообщения: содержат контекст (индекс элемента, путь к файлу).

Batch-обработка: при чтении пытается обработать все элементы, даже если некоторые содержат ошибки.

Консистентность: гарантирует, что либо возвращаются все студенты, либо исключение с описанием всех ошибок.

---
Screen
---
<img width="1159" height="438" alt="image" src="https://github.com/user-attachments/assets/12fa7dbd-1455-4673-9bfc-4948ac53ff7b" />

Пример students.json
<img width="550" height="737" alt="image" src="https://github.com/user-attachments/assets/6be9fc64-57f2-4d10-8551-ecc22d84b1df" />

Пример содержимого файла not_list.json
<img width="190" height="41" alt="image" src="https://github.com/user-attachments/assets/bb103a3e-c339-4d36-bacf-5d7cee40a2a9" />

Пример содержимого файла invalid_data.json
<img width="888" height="26" alt="image" src="https://github.com/user-attachments/assets/7811bfa1-9cae-408e-8019-9a2f8f90c7cf" />

Пример содержимого файла incomplete.json
<img width="515" height="25" alt="image" src="https://github.com/user-attachments/assets/8180f4ca-d958-49ca-8e75-33d660c6c3ad" />

Пример содержимого файла invalid.json
<img width="145" height="28" alt="image" src="https://github.com/user-attachments/assets/fa454894-371c-40d6-83df-27c2c46c285f" />

Пример входного JSON
<img width="371" height="708" alt="image" src="https://github.com/user-attachments/assets/647462bb-109e-434f-8625-1874a01cfa2d" />

Пример выходного JSON
<img width="373" height="709" alt="image" src="https://github.com/user-attachments/assets/a08c13b6-af1a-4e64-a0c4-615728ba6b42" />



## Что сдавать?

1.  **Код**:
    -   `src/lab08/models.py`
    -   `src/lab08/serialize.py`
2.  **README.md**:
    -   результаты
    -   примеры запуска
    -   примеры JSON
3.  **Файлы данных**:
    -   `students_input.json`
    -   `students_output.json`
4.  **Скриншоты работы**

---

## Критерий допуска
-   Лабораторная выполнена полностью\
-   README оформлен в стиле прошлых работ\

---

## Критерий приёмки
 - Корректность класса и методов — **20%**  
 - Корректность сереализации/десереализации — **20%**  
 - Ответы на вопросы по теории — **60%** 

---

## Полезные ссылки

-   Официальная документация `dataclasses`: https://docs.python.org/3/library/dataclasses.html\

-   Модуль `json`: https://docs.python.org/3/library/json.html\

-   Работа с датами `(datetime)`: https://docs.python.org/3/library/datetime.html
