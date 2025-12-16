# ЛР9 — «База данных» на CSV: класс `Group`, CRUD-операции и CLI

> **Цель:** реализовать простейшее хранилище данных студентов на основе
> CSV-файла, отработать CRUD-операции (Create / Read / Update / Delete) 
> и научиться работать с ними через отдельный класс `Group`.
> **Связь:** ЛР9 использует Student из ЛР8 и утилиты работы с CSV из ЛР4–ЛР5.
> Также создаёт основу для CLI-утилиты в ЛР10.

---
## Результат ЛР

После выполнения ЛР8 в репозитории должны присутствовать:

### `src/lab09/group.py`

Класс **`Group`**, реализующий CRUD-операции над студентами:

- инициализацию с путём к CSV-файлу (`__init__`)
- чтение всех записей из CSV
- методы:
  - `add(student: Student)` — добавление студента
  - `list() -> list[Student]` — получить всех студентов
  - `find(substr: str)` — поиск по подстроке в ФИО
  - `remove(fio: str)` — удаление по ФИО
  - `update(fio: str, **fields)` — обновление полей существующей записи

---
### `src/lab09/__init__.py`

- файл инициализации пакета `lab09`

---
### `data/lab09/students.csv`

CSV-файл — «база данных» студентов, содержащий:

- строку-заголовок:  
  `fio,birthdate,group,gpa`
- одну или несколько строк с данными студентов, например:  
  `Иванов Иван,2003-10-10,БИВТ-21-1,4.3`

---
### `images/lab09/`

Каталог со скриншотами, демонстрирующими работу ЛР9:

- добавление студента
- вывод списка
- поиск / обновление / удаление записей

---
### Формат CSV

Файл хранится по пути `data/lab09/students.csv`.

Структура:

```csv
fio,birthdate,group,gpa
Иванов Иван,2003-10-10,SE-01,4.3
...
```
---

## Структура репозитория (рекомендации)
```text
python_labs/
├─ README.md
├─ src/
│   ├─ lab08
│   ├─ lab09/
│   │   ├─ group.py          # класс Group + CRUD
│   │   └─ __init__.py
│   └─ ...
├─ data/
│   ├─ lab08
│   └─ lab09/
│       └─ students.csv      # «база данных» студентов
└─ images/
    ├─ lab08
    └─ lab09
```

---
## Теоретическая часть: CRUD

CRUD — стандартный набор операций:

| Операция | Назначение                       |
|----------|----------------------------------|
| Create   | Добавление записи                |
| Read     | Получение списка / поиск         |
| Update   | Изменение существующей записи    |
| Delete   | Удаление                         |

В этой ЛР каждая операция будет реализована как метод класса `Group`.

---

## Задание

### A. Реализовать класс **`Group`**, содержащий:

- поля (атрибуты экземпляра):
  - `path` — путь к CSV-файлу с данными студентов

- методы:
  - `__init__(storage_path)` — инициализация группы и файла-хранилища
  - `list()` — вернуть **всех** студентов в виде списка `Student`
  - `add(student)` — добавить нового студента в CSV
  - `find(substr)` — найти студентов по подстроке в `fio`
  - `remove(fio)` — удалить запись(и) с данным `fio`
  - `update(fio, **fields)` — обновить поля существующего студента

- внутренние вспомогательные методы (опционально):
  - `_read_all()` — прочитать все строки из CSV
  - `_ensure_storage_exists()` — создать файл с заголовком, если его ещё нет

- валидация:
  - наличие строки-заголовка в CSV (`fio,birthdate,group,gpa`)
  - соответствие каждой строки корректному объекту `Student`

Code
```
import csv
import os
from datetime import datetime
from typing import List, Optional, Dict, Any


class Student:
    """Вспомогательный класс для представления студента"""

    def __init__(self, fio: str, birthdate: str, group: str, gpa: str):
        self.fio = fio
        self.birthdate = birthdate
        self.group = group
        self.gpa = gpa

    def __repr__(self):
        return f"Student(fio='{self.fio}', birthdate='{self.birthdate}', group='{self.group}', gpa='{self.gpa}')"

    def to_dict(self) -> Dict[str, str]:
        """Конвертирует объект Student в словарь"""
        return {
            'fio': self.fio,
            'birthdate': self.birthdate,
            'group': self.group,
            'gpa': self.gpa
        }


class Group:
    """Класс для работы с группой студентов, хранящейся в CSV-файле"""

    # Ожидаемые заголовки CSV файла
    HEADER = ['fio', 'birthdate', 'group', 'gpa']

    def __init__(self, storage_path: str):
        """
        Инициализация группы и файла-хранилища

        Args:
            storage_path: путь к CSV-файлу с данными студентов
        """
        self.path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """
        Создает файл с заголовком, если его ещё нет

        Создает CSV файл с заголовками, если файл не существует.
        Если файл существует, проверяет корректность заголовков.
        """
        # Если файл не существует, создаю его с заголовком
        if not os.path.exists(self.path):
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()
        else:
            # Проверяю существующий файл на наличие корректного заголовка
            try:
                with open(self.path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    if reader.fieldnames != self.HEADER:
                        raise ValueError(
                            f"Неверный формат CSV файла. Ожидаемые заголовки: {self.HEADER}, "
                            f"полученные: {reader.fieldnames}"
                        )
            except csv.Error as e:
                raise ValueError(f"Ошибка чтения CSV файла: {e}")

    def _read_all(self) -> List[Dict[str, str]]:
        """
        Читает все строки из CSV и возвращает список словарей

        Returns:
            Список словарей, где каждый словарь представляет студента

        Raises:
            ValueError: если строка содержит неверное количество полей
        """
        students = []
        with open(self.path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Проверка заголовка
            if reader.fieldnames != self.HEADER:
                raise ValueError(f"Неверный формат заголовка CSV файла")

            for i, row in enumerate(reader, start=2):  # start=2 для учета заголовка
                # Проверяю, что все поля присутствуют
                if len(row) != len(self.HEADER):
                    raise ValueError(
                        f"Строка {i}: неверное количество полей. "
                        f"Ожидалось {len(self.HEADER)}, получено {len(row)}"
                    )

                # Проверяю, что все поля заполнены
                for field in self.HEADER:
                    if field not in row or row[field] is None:
                        raise ValueError(f"Строка {i}: отсутствует поле '{field}'")

                students.append(row)

        return students

    def list(self) -> List[Student]:
        """
        Возвращает всех студентов в виде списка объектов Student

        Returns:
            Список объектов Student

        Raises:
            ValueError: если данные в CSV некорректны
        """
        students_data = self._read_all()
        students = []

        for data in students_data:
            # Валидация данных при создании объекта Student
            try:
                # Проверяю GPA (должно быть числом)
                gpa = data['gpa']
                if not self._is_valid_gpa(gpa):
                    raise ValueError(f"Некорректное значение GPA: {gpa}")

                student = Student(
                    fio=data['fio'],
                    birthdate=data['birthdate'],
                    group=data['group'],
                    gpa=gpa
                )
                students.append(student)
            except Exception as e:
                raise ValueError(f"Ошибка при создании студента из данных {data}: {e}")

        return students

    def add(self, student: Student) -> None:
        """
        Добавляет нового студента в CSV файл

        Args:
            student: объект Student для добавления

        Raises:
            ValueError: если студент с таким ФИО уже существует
        """
        # Проверяю валидность GPA
        if not self._is_valid_gpa(student.gpa):
            raise ValueError(f"Некорректное значение GPA: {student.gpa}")

        # Проверяю, нет ли уже студента с таким ФИО
        existing_students = self.list()
        for existing in existing_students:
            if existing.fio == student.fio:
                raise ValueError(f"Студент с ФИО '{student.fio}' уже существует")

        # Добавляю студента в файл
        with open(self.path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.HEADER)
            writer.writerow(student.to_dict())

    def find(self, substr: str) -> List[Student]:
        """
        Находит студентов по подстроке в ФИО

        Args:
            substr: подстрока для поиска в поле fio

        Returns:
            Список объектов Student, у которых в ФИО содержится substr
        """
        all_students = self.list()
        result = []

        # Поиск без учета регистра
        substr_lower = substr.lower()
        for student in all_students:
            if substr_lower in student.fio.lower():
                result.append(student)

        return result

    def remove(self, fio: str) -> int:
        """
        Удаляет запись(и) с данным ФИО

        Args:
            fio: полное ФИО для удаления

        Returns:
            Количество удаленных записей
        """
        all_students = self.list()
        # Оставляю только студентов, у которых ФИО не совпадает с искомым
        students_to_keep = [s for s in all_students if s.fio != fio]
        removed_count = len(all_students) - len(students_to_keep)

        if removed_count > 0:
            # Перезаписываю файл с оставшимися студентами
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()
                for student in students_to_keep:
                    writer.writerow(student.to_dict())

        return removed_count

    def update(self, fio: str, **fields: Any) -> int:
        """
        Обновляет поля существующего студента

        Args:
            fio: ФИО студента для обновления
            **fields: поля для обновления (ключ-значение)

        Returns:
            Количество обновленных записей

        Raises:
            ValueError: если переданы некорректные поля
        """
        # Проверяю, что все передаваемые поля допустимы
        for field in fields.keys():
            if field not in self.HEADER:
                raise ValueError(f"Недопустимое поле: '{field}'. Допустимые поля: {self.HEADER}")

        # Проверяю валидность GPA, если оно передано
        if 'gpa' in fields and not self._is_valid_gpa(str(fields['gpa'])):
            raise ValueError(f"Некорректное значение GPA: {fields['gpa']}")

        all_students = self.list()
        updated_count = 0

        # Обновляю студентов с заданным ФИО
        for student in all_students:
            if student.fio == fio:
                updated_count += 1
                for field, value in fields.items():
                    setattr(student, field, str(value))

        if updated_count > 0:
            # Перезаписываю файл с обновленными данными
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()
                for student in all_students:
                    writer.writerow(student.to_dict())

        return updated_count

    def _is_valid_gpa(self, gpa_str: str) -> bool:
        """
        Проверяет валидность GPA

        Args:
            gpa_str: строка с GPA

        Returns:
            True если GPA валидно, иначе False
        """
        try:
            gpa = float(gpa_str)
            return 0.0 <= gpa <= 5.0  # Предполагаю 5-балльную систему
        except (ValueError, TypeError):
            return False


# Пример использования
if __name__ == "__main__":
    # Создаю группу (файл будет создан автоматически)
    group = Group("students.csv")

    # Добавляю студентов
    student1 = Student("Иванов Иван Иванович", "2000-05-15", "Группа 101", "4.5")
    student2 = Student("Петров Петр Петрович", "2001-03-20", "Группа 101", "3.8")

    try:
        group.add(student1)
        group.add(student2)
    except ValueError as e:
        print(f"Ошибка при добавлении: {e}")

    # Вывожу всех студентов
    print("Все студенты:")
    for student in group.list():
        print(f"  {student}")

    # Ищу студентов по подстроке
    print("\nПоиск 'Иванов':")
    for student in group.find("Иванов"):
        print(f"  {student}")

    # Обновляю данные студента
    print(f"\nОбновляем студента {student1.fio}:")
    updated = group.update(student1.fio, gpa="4.8", group="Группа 102")
    print(f"  Обновлено записей: {updated}")

    # Проверяю обновление
    print("\nПосле обновления:")
    for student in group.list():
        print(f"  {student}")

    # Удаляю студента
    print(f"\nУдаляем студента {student2.fio}:")
    removed = group.remove(student2.fio)
    print(f"  Удалено записей: {removed}")

    print("\nОставшиеся студенты:")
    for student in group.list():
        print(f"  {student}")
```

#### Основные особенности реализации
Валидация данных:
Проверка наличия и корректности заголовков CSV.

Проверка количества полей в каждой строке.

Валидация GPA (должно быть числом от 0 до 5).

Проверка уникальности ФИО при добавлении.

Вспомогательные методы:
_read_all(): читает и валидирует все данные из CSV.

_ensure_storage_exists(): создает файл с заголовком при необходимости.

_is_valid_gpa(): проверяет корректность GPA.

Обработка ошибок:
Все операции содержат проверки и выбрасывают исключения при некорректных данных.

Учет номера строки при обработке CSV для отладки ошибок.

Совместимость:
Используется стандартная библиотека CSV.

Поддержка UTF-8 кодировки.

Типизация для лучшей читаемости кода.

Класс корректно обрабатывает:

Создание нового файла.

Чтение существующего файла.

Добавление, обновление, удаление и поиск записей.

Валидацию данных на каждом этапе.

---
Screen
---

<img width="867" height="505" alt="image" src="https://github.com/user-attachments/assets/f432668f-a9b4-4c77-8fed-410b7383bca3" />
<img width="407" height="591" alt="image" src="https://github.com/user-attachments/assets/3dbb7731-f3e1-42fb-93b8-8491460ffafb" />
<img width="334" height="55" alt="image" src="https://github.com/user-attachments/assets/6a5e61d4-4a49-4bd1-b155-cf8ad4d5e167" />


### ★ Дополнительное задание (со звёздочкой)
#### Расширенная аналитика по группе

Добавить в класс `Group` **аналитический метод**, собирающий статистику по студентам.

#### Метод `stats(self) -> dict`

Метод должен возвращать словарь следующей структуры:

```python
{
    "count": <общее количество студентов>,
    "min_gpa": <минимальный gpa>,
    "max_gpa": <максимальный gpa>,
    "avg_gpa": <средний gpa>,
    "groups": {
        "БИВТ-21-1": <число студентов>,
        "БИВТ-21-2": <число студентов>,
        ...
    },
    "top_5_students": [
        {"fio": "...", "gpa": ...},
        ...
    ]
}
```


## Пример кода 

``` python
import csv
from pathlib import Path
from src.lab08.models import Student

class Group:
    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8") 

    def _read_all(self):
        # TODO: реализовать чтение строк из csv 

    def list(self):
        # TODO: реализовать метод list()

    def add(self, student: Student):
         # TODO: реализовать метод add()

    def find(self, substr: str):
        # TODO: реализовать метод find()
        return [r for r in rows if substr in r["fio"]]  

    def remove(self, fio: str):
        # TODO: реализовать метод remove()
        for i, r in enumerate(rows):
            if r["fio"] == fio:
                rows.pop(i)
                break

    def update(self, fio: str, **fields):
        # TODO: реализовать метод update()
```

Code
```
import csv
import os
import statistics
from datetime import datetime
from typing import List, Dict, Any, Optional


class Student:
    """Вспомогательный класс для представления студента"""

    def __init__(self, fio: str, birthdate: str, group: str, gpa: str):
        self.fio = fio
        self.birthdate = birthdate
        self.group = group
        self.gpa = float(gpa)  # Преобразую в float для вычислений

    def __repr__(self):
        return f"Student(fio='{self.fio}', birthdate='{self.birthdate}', group='{self.group}', gpa={self.gpa})"

    def to_dict(self) -> Dict[str, str]:
        """Конвертирует объект Student в словарь"""
        return {
            'fio': self.fio,
            'birthdate': self.birthdate,
            'group': self.group,
            'gpa': str(self.gpa)  # Обратно в строку
        }


class Group:
    """Класс для работы с группой студентов, хранящейся в CSV-файле"""

    # Ожидаемые заголовки CSV файла
    HEADER = ['fio', 'birthdate', 'group', 'gpa']

    def __init__(self, storage_path: str):
        """
        Инициализация группы и файла-хранилища

        Args:
            storage_path: путь к CSV-файлу с данными студентов
        """
        self.path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Создает файл с заголовком, если его ещё нет"""
        if not os.path.exists(self.path):
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()

    def _read_all(self) -> List[Dict[str, str]]:
        """Читает все строки из CSV и возвращает список словарей"""
        students = []
        with open(self.path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        return students

    def list(self) -> List[Student]:
        """Возвращает всех студентов в виде списка объектов Student"""
        students_data = self._read_all()
        return [Student(**data) for data in students_data]

    def stats(self) -> Dict[str, Any]:
        """
        Собирает статистику по студентам

        Returns:
            Словарь со статистикой:
            {
                "count": общее количество студентов,
                "min_gpa": минимальный gpa,
                "max_gpa": максимальный gpa,
                "avg_gpa": средний gpa,
                "groups": распределение по группам {группа: количество},
                "top_5_students": топ-5 студентов с самым высоким GPA
            }
        """
        students = self.list()

        if not students:
            # Если студентов нет, возвращаю пустую статистику
            return {
                "count": 0,
                "min_gpa": 0.0,
                "max_gpa": 0.0,
                "avg_gpa": 0.0,
                "groups": {},
                "top_5_students": []
            }

        # Базовая статистика
        gpa_values = [student.gpa for student in students]

        # Распределение по группам
        groups_distribution = {}
        for student in students:
            group_name = student.group
            groups_distribution[group_name] = groups_distribution.get(group_name, 0) + 1

        # Топ-5 студентов по GPA
        sorted_students = sorted(students, key=lambda x: x.gpa, reverse=True)
        top_5 = [
            {"fio": student.fio, "gpa": student.gpa}
            for student in sorted_students[:5]
        ]

        # Расчет медианы GPA (дополнительно)
        median_gpa = statistics.median(gpa_values) if len(gpa_values) >= 1 else 0.0

        # Расчет моды групп (дополнительно)
        if groups_distribution:
            most_common_group = max(groups_distribution.items(), key=lambda x: x[1])
        else:
            most_common_group = ("Нет данных", 0)

        # Расчет стандартного отклонения GPA (дополнительно)
        if len(gpa_values) > 1:
            std_dev_gpa = statistics.stdev(gpa_values)
        else:
            std_dev_gpa = 0.0

        # Возвращаю основную и расширенную статистику
        return {
            # Основная статистика (по заданию)
            "count": len(students),
            "min_gpa": min(gpa_values),
            "max_gpa": max(gpa_values),
            "avg_gpa": sum(gpa_values) / len(gpa_values),
            "groups": groups_distribution,
            "top_5_students": top_5,

            # Дополнительная статистика
            "median_gpa": median_gpa,
            "std_dev_gpa": std_dev_gpa,
            "most_common_group": most_common_group[0],
            "students_in_most_common_group": most_common_group[1],
            "gpa_range": max(gpa_values) - min(gpa_values)
        }

    def add(self, student: Student) -> None:
        """Добавляет нового студента в CSV файл"""
        with open(self.path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.HEADER)
            writer.writerow(student.to_dict())

    def find(self, substr: str) -> List[Student]:
        """Находит студентов по подстроке в ФИО"""
        all_students = self.list()
        substr_lower = substr.lower()
        return [s for s in all_students if substr_lower in s.fio.lower()]

    def remove(self, fio: str) -> int:
        """Удаляет запись(и) с данным ФИО"""
        all_students = self.list()
        students_to_keep = [s for s in all_students if s.fio != fio]
        removed_count = len(all_students) - len(students_to_keep)

        if removed_count > 0:
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()
                for student in students_to_keep:
                    writer.writerow(student.to_dict())

        return removed_count

    def update(self, fio: str, **fields: Any) -> int:
        """Обновляет поля существующего студента"""
        all_students = self.list()
        updated_count = 0

        for student in all_students:
            if student.fio == fio:
                updated_count += 1
                for field, value in fields.items():
                    if field in self.HEADER:
                        setattr(student, field, str(value))

        if updated_count > 0:
            with open(self.path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.HEADER)
                writer.writeheader()
                for student in all_students:
                    writer.writerow(student.to_dict())

        return updated_count


# Демонстрация работы метода stats()
def demonstrate_stats():
    """Функция для демонстрации работы метода stats()"""

    # Создаю тестовый файл
    test_file = "test_students.csv"

    # Удаляю файл, если он существует
    if os.path.exists(test_file):
        os.remove(test_file)

    # Создаю группу
    group = Group(test_file)

    # Добавляю тестовых студентов
    test_students = [
        Student("Иванов Иван Иванович", "2000-05-15", "БИВТ-21-1", "4.5"),
        Student("Петров Петр Петрович", "2001-03-20", "БИВТ-21-1", "3.8"),
        Student("Сидорова Анна Сергеевна", "1999-11-30", "БИВТ-21-2", "4.2"),
        Student("Кузнецов Алексей Дмитриевич", "2000-07-22", "БИВТ-21-3", "3.5"),
        Student("Смирнова Екатерина Владимировна", "2001-01-10", "БИВТ-21-2", "4.7"),
        Student("Васильев Василий Васильевич", "2000-12-05", "БИВТ-21-1", "4.9"),
        Student("Николаева Ольга Игоревна", "2001-04-18", "БИВТ-21-3", "3.9"),
        Student("Алексеев Дмитрий Сергеевич", "1999-08-25", "БИВТ-21-2", "4.0"),
        Student("Павлова Мария Андреевна", "2000-02-14", "БИВТ-21-1", "4.3"),
        Student("Федоров Артем Викторович", "2001-06-30", "БИВТ-21-3", "3.6"),
    ]

    for student in test_students:
        group.add(student)

    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ МЕТОДА stats()")
    print("=" * 60)

    # Получаю статистику
    statistics = group.stats()

    # Вывожу основную статистику
    print(f"\n ОБЩАЯ СТАТИСТИКА:")
    print(f"   Всего студентов: {statistics['count']}")
    print(f"   Минимальный GPA: {statistics['min_gpa']:.2f}")
    print(f"   Максимальный GPA: {statistics['max_gpa']:.2f}")
    print(f"   Средний GPA: {statistics['avg_gpa']:.2f}")

    print(f"\n РАСПРЕДЕЛЕНИЕ ПО ГРУППАМ:")
    for group_name, count in statistics['groups'].items():
        percentage = (count / statistics['count']) * 100
        print(f"   {group_name}: {count} студентов ({percentage:.1f}%)")

    print(f"\n ТОП-5 СТУДЕНТОВ:")
    for i, student in enumerate(statistics['top_5_students'], 1):
        print(f"   {i}. {student['fio']} - GPA: {student['gpa']:.2f}")

    # Вывожу дополнительную статистику
    print(f"\n ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА:")
    print(f"   Медианный GPA: {statistics['median_gpa']:.2f}")
    print(f"   Стандартное отклонение GPA: {statistics['std_dev_gpa']:.2f}")
    print(f"   Разброс GPA: {statistics['gpa_range']:.2f}")
    print(f"   Самая многочисленная группа: {statistics['most_common_group']}")
    print(f"   Студентов в ней: {statistics['students_in_most_common_group']}")

    # Пример аналитики на основе статистики
    print(f"\n АНАЛИТИКА:")
    if statistics['std_dev_gpa'] < 0.5:
        print("   GPA студентов распределен равномерно")
    else:
        print("   Есть значительный разброс в успеваемости студентов")

    if statistics['avg_gpa'] > 4.0:
        print("   Средний уровень успеваемости высокий")
    elif statistics['avg_gpa'] > 3.0:
        print("   Средний уровень успеваемости удовлетворительный")
    else:
        print("   Средний уровень успеваемости низкий")

    # Визуализация распределения GPA (текстовая)
    print(f"\n ГИСТОГРАММА GPA (грубо):")
    gpa_ranges = {
        "5.0": 0,
        "4.0-4.9": 0,
        "3.0-3.9": 0,
        "2.0-2.9": 0,
        "0.0-1.9": 0
    }

    students = group.list()
    for student in students:
        gpa = student.gpa
        if gpa == 5.0:
            gpa_ranges["5.0"] += 1
        elif gpa >= 4.0:
            gpa_ranges["4.0-4.9"] += 1
        elif gpa >= 3.0:
            gpa_ranges["3.0-3.9"] += 1
        elif gpa >= 2.0:
            gpa_ranges["2.0-2.9"] += 1
        else:
            gpa_ranges["0.0-1.9"] += 1

    for range_name, count in gpa_ranges.items():
        bar = "█" * count
        print(f"   {range_name:8} | {bar} ({count})")

    print("=" * 60)

    # Удаляю тестовый файл
    os.remove(test_file)


# Пример использования в основном коде
if __name__ == "__main__":
    demonstrate_stats()

    # Пример интеграции в существующий код
    print("\n\nПример использования в основном классе:")

    # Создаю реальный файл
    group = Group("../../data/lab09/students_stats.csv")

    # Добавляю несколько студентов
    group.add(Student("Иванов Иван", "2000-01-01", "БИВТ-21-1", "4.5"))
    group.add(Student("Петров Петр", "2000-02-02", "БИВТ-21-2", "3.8"))
    group.add(Student("Сидоров Сидор", "2000-03-03", "БИВТ-21-1", "4.2"))

    # Получаю статистику
    stats = group.stats()
    print(f"\nСтатистика по группе:")
    print(f"Количество: {stats['count']}")
    print(f"Средний GPA: {stats['avg_gpa']:.2f}")
    print(f"Распределение по группам: {stats['groups']}")
```

#### Основные особенности реализации метода stats():
Основная статистика (по заданию):
count - общее количество студентов.

min_gpa - минимальный GPA.

max_gpa - максимальный GPA.

avg_gpa - средний GPA.

groups - распределение по группам.

top_5_students - топ-5 студентов с самым высоким GPA.

Дополнительная аналитика:
median_gpa - медианный GPA.

std_dev_gpa - стандартное отклонение GPA.

most_common_group - самая многочисленная группа.

students_in_most_common_group - количество студентов в ней.

gpa_range - разброс GPA.

Обработка крайних случаев:
Проверка на пустой список студентов.

Корректная работа с пустыми данными.

Преобразование типов (GPA из строки в float).

Визуализация данных:
Текстовая гистограмма распределения GPA.

Процентное распределение по группам.

Аналитические выводы на основе статистики.

---
Screen
---

<img width="571" height="647" alt="image" src="https://github.com/user-attachments/assets/642c5609-6be0-45f9-8f09-b2bd56e9edd2" />


## Что сдавать

1.  **Код**:
    -   `src/lab09/group.py`
2.  **README.md**:
    -   результаты
    -   примеры запуска
    -   примеры JSON
3.  **Файлы данных**:
    -   `students.csv`
4.  **Скриншоты работы**

---

## Критерий допуска
-   Лабораторная выполнена полностью\
-   README оформлен в стиле прошлых работ\

---

## Критерий приёмки
 - Корректность класса и методов `crud` — **20%**  
 - Корректность `csv` — **20%**  
 - Ответы на вопросы по теории — **60%** 
