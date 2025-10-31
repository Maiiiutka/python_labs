# ЛР4 — Файлы: TXT/CSV и отчёты по текстовой статистике

> **Цель:** закрепить работу с файлами (чтение/запись, кодировки), автоматизировать сбор статистики по словам и выгружать её в CSV.  
> **Связь:** продолжаем ЛР3 — используем `src/lib/text.py` (`normalize`, `tokenize`, `count_freq`, `top_n`) как переиспользуемый модуль.

---

## Результат ЛР
- Модуль ввода/вывода `src/lab04/io_txt_csv.py` с чистыми функциями для чтения текста и записи CSV.  
- Скрипт `src/lab04/text_report.py`, который читает текст(ы) из файлов, считает частоты и сохраняет отчёты.  
- README с примерами запуска, плюс 1–2 тестовых файла в `data/`.  
- **Только стандартная библиотека** (`csv`, `pathlib`, `io`, `sys`, `argparse` — опционально). Python **3.хх+**.

---
Структура репозитория (в формате ЛР2)

Свой **отдельный репозиторий** на GitHub:
```
python_labs/
├─ README.md                 # Общий отчет
├─ src/                      # здесь — все скрипты по заданиям
│  ├─ lib/                   # переиспользуемые модули
│  │   └─ text.py            # из ЛР3
│  ├─ lab01/
|  ........
│  ├─ lab04/                 # (эта лабораторная)
│  │   ├─ io_txt_csv.py      # read_text / write_csv (+ ensure_parent_dir)
│  │   └─ text_report.py     # генерация data/report.csv + ★
│  ├─ lab05/
|  ........
│  └─ lab10/
├─ data/
│  └─ lab04/
│      ├─ input.txt          # вход для базовой версии
│      ├─ a.txt              # входы для ★ (несколько файлов)
│      └─ b.txt
└─ images/                   # сюда — скриншоты работы программ
   ├─ lab01
   ........           
   ├─ lab04/                 # Папка lab04 теперь - непустая
   |   ├─ img01.png          # пример запуска базовой версии
   |   ........
   |   └─ img05.png          # пример запуска со списком файлов (★)
   ├─ lab05
   ........
   └─ lab10
```


---
## Теория и формальные правила

### Нормализация и токенизация (берём из ЛР3)
- `norm(s)` = `casefold` → `ё→е` → заменить `\t\r\n` на пробел → схлопнуть пробелы.  
- `tokenize(norm(s))` = все подстроки по шаблону `\w+(?:-\w+)*` (разделители — не-`\w`).

### Частоты и сортировка
- Для токенов `T = [t₁,…,tₙ]` частота `f(w) = |{ i : tᵢ = w }|`.  
- Топ-N: сортировка пар `(w, f(w))` по ключу **`(-f(w), w)`** → берём первые N.

### Формат CSV-отчётов
- Базовый отчёт: **`word,count`**, строки отсортированы по `count ↓`, затем `word ↑`.  
- Вариант «несколько файлов» (★): **`file,word,count`**, отсортировано `file ↑`, затем `count ↓`, затем `word ↑`.  
- Кодировка файлов: по умолчанию `UTF-8` (в явном виде указываем при чтении/записи).

---
## Подсказки по коду (шаблоны)

### Чтение текста
```python
from pathlib import Path

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    p = Path(path)
    # FileNotFoundError и UnicodeDecodeError пусть «всплывают» — это нормально
    return p.read_text(encoding=encoding)
```

### Запись CSV 
```python
import csv
from pathlib import Path
from typing import Iterable, Sequence

def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    rows = list(rows)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)
```
### Генерация отчёта
```python
from collections import Counter

def frequencies_from_text(text: str) -> dict[str, int]:
    from lib.text import normalize, tokenize  # из ЛР3
    tokens = tokenize(normalize(text))
    return Counter(tokens)  # dict-like

def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
```
---

## Задание A — модуль `src/lab04/io_txt_csv.py`

Реализуйте (с докстрингами и типами):

1. `read_text(path: str | Path, encoding: str = "utf-8") -> str`  
   - Открыть файл на чтение в указанной кодировке и вернуть содержимое **как одну строку**.  
   - Обрабатывать ошибки: если файл не найден — поднимать `FileNotFoundError` (пусть падает), если кодировка не подходит — поднимать `UnicodeDecodeError` (пусть падает).  
   - НО: в докстринге опишите, как пользователь может выбрать другую кодировку (пример: `encoding="cp1251"`).

2. `write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None`  
   - Создать/перезаписать CSV с разделителем `,`.  
   - Если передан `header`, записать его первой строкой.  
   - Проверить, что каждая строка в `rows` имеет одинаковую длину (иначе `ValueError`).

★ _(опционально, но полезно)_ `ensure_parent_dir(path: str | Path) -> None`  
   - Создать родительские директории, если их нет (для удобства перед записью).

### Мини‑тесты (ручные, для README)
```py
from src.io_txt_csv import read_text, write_csv
txt = read_text("data/input.txt")  # должен вернуть строку
write_csv([("word","count"),("test",3)], "data/check.csv")  # создаст CSV
```

### Краевые случаи
- Пустой файл → возвращается пустая строка.  
- Файл очень большой → допускается читать целиком (наше ТЗ), но в README отметить, что в реале стоит читать построчно.  
- `write_csv` с пустым `rows` и `header=None` → создаётся пустой файл (0 строк). С `header=("a","b")` → файл содержит только заголовок.

---

Code

```
import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:

    """
    Читает содержимое текстового файла и возвращает его в виде одной строки.
    
    Открывает файл на чтение в указанной кодировке и возвращает всё содержимое
    как единую строку.
    
    Аргументы:
        path: Путь к файлу в виде строки или объекта Path
        encoding: Кодировка файла. По умолчанию "utf-8".
                 Другие варианты: "cp1251" (кириллица Windows),
                 "koi8-r" (русская), "iso-8859-1" (латиница)
    
    Возвращает:
        str: Содержимое файла в виде одной строки
        
    Выбрасывает исключения:
        FileNotFoundError: Если файл не существует
        UnicodeDecodeError: Если указанная кодировка не подходит для файла
        OSError: При других ошибках ввода-вывода
        
    Примеры:
        >>> content = read_text("data/input.txt")
        >>> russian_text = read_text("data/cyrillic.txt", encoding="cp1251")
    """

    path = Path(path)

    with open(path, 'r', encoding=encoding) as file:
        return file.read()

def write_csv(rows: list[tuple | list], 
    path: str | Path, 
    header: tuple[str, ...] | None = None) -> None:
 
    """
    Записывает данные в CSV файл с разделителем-запятой.
    
    Создает или перезаписывает CSV файл. Если передан заголовок (header),
    записывает его первой строкой. Все строки данных должны иметь одинаковое
    количество столбцов.
    
    Аргументы:
        rows: Список кортежей или списков, представляющих строки данных
        path: Путь к выходному файлу в виде строки или объекта Path
        header: Опциональный кортеж с названиями столбцов для заголовка
    
    Выбрасывает исключения:
        ValueError: Если строки имеют разную длину
        OSError: Если файл не может быть записан
        
    Примеры:
        >>> write_csv([("слово", "количество"), ("тест", 1)], "data/output.csv")
        >>> write_csv([(1, "яблоко"), (2, "банан")], "data/fruits.csv", 
        ...           header=("id", "фрукт"))
    """

    path = Path(path)
    
    make_parent_dir(path)
    
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if header is not None:
            writer.writerow(header)
        if rows:
            first_len = len(rows[0])
            for i, row in enumerate(rows):
                if len(row) != first_len:
                    raise ValueError(
                        f"All rows must have same length. "
                        f"Row 0 has {first_len} columns, but row {i} has {len(row)}")
            writer.writerows(rows)

def make_parent_dir(path: str | Path) -> None:

    """
    Создает родительские директории, если они не существуют.
    
    Вспомогательная функция для создания структуры директорий перед
    операциями записи файлов.
    
    Аргументы:
        path: Путь к файлу, для которого нужно создать родительские директории
        
    Пример:
        >>> make_parent_dir("data/подпапка/результат.txt")
        # Создает директории 'data/подпапка' если их нет
    """
        
    path = Path(path)
    parent_dir = path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    
    try:
        
        content = read_text("./data/Lab04/input.txt")
        print(f"Read {len(content)} characters")
        
       
        write_csv([("word", "count"), ("test", 3)], "data/check.csv")
        print("CSV file created successfully")
        
        
        write_csv(
            [("Melon", "mango"), ("watermelon", "apple")], 
            "data/fruits.csv", 
            header=("big_fruit", "fruit")
        )
        print("CSV with header created successfully")
        
     
        write_csv([], "data/empty.csv")  
        write_csv([], "data/header_only.csv", header=("a", "b"))  
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
    except Exception as e:
        print(f"Error: {e}")
```

Screen

<img width="1172" height="777" alt="image" src="https://github.com/user-attachments/assets/756756fe-e11d-44ee-839a-f88e9155bd31" />

---

## Задание B — скрипт `src/lab04/text_report.py`

Напишите скрипт, который:
1) Читает **один** входной файл `data/input.txt` (путь можно захардкодить или принять параметром командной строки — опишите в README).  
2) Нормализует текст (`lib/text.py`), токенизирует и считает частоты слов.  
3) Сохраняет `data/report.csv` c колонками: **`word,count`**, отсортированными: count ↓, слово ↑ (при равенстве).  
4) В консоль печатает краткое резюме:  
   - `Всего слов: <N>`  
   - `Уникальных слов: <K>`  
   - `Топ-5:` (список из `top_n` из ЛР3)

### Пример запуска
```bash
python src/lab04/text_report.py                 # читает data/input.txt, пишет data/report.csv
# или
python src/lab04/text_report.py --in data/in.txt --out data/out.csv
```

### Пример `report.csv`
```
word,count
привет,2
мир,1
```

### Краевые случаи
- `data/input.txt` не существует → понятная ошибка в консоли (исключение пусть всплывает или выведите `print()` и `sys.exit(1)` — опишите поведение в README).  
- Пустой вход → `report.csv` будет содержать только заголовок или будет пустым (примите решение и опишите — рекомендую **только заголовок**).  
- Нестандартная кодировка → укажите, как передать `--encoding cp1251` (если реализуете `argparse`).

---

Code

```
import sys
#from ...lib.text import *
#from .io_txt_csv import read_text, write_csv

if __name__ == "__main__":

    sys.path.append("./src")
    sys.path.append("./src/Sem1/Lab04")
    from io_txt_csv import read_text, write_csv
    from lib.text import *

    path = "./data/Lab04/input.txt"
    text = read_text(path)
    normalized = normalize(text)
    tokens = tokenize(normalized)
    counted = count_freq(tokens)

    header = ("word", "count")
    rows = [[word, count] for word, count in counted.items()]
    write_csv(rows, "./data/report.csv", header)

    total_words = len(tokens)
    unique_words = len(set(tokens))
    freq = count_freq(tokens)
    top_words = top_n(freq, 5)

    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5 слов:")
    for word, count in top_words:
        print(f"{word}: {count}")
```

Screen

<img width="1020" height="762" alt="image" src="https://github.com/user-attachments/assets/55dd6097-869c-481b-9337-7eab09bb9918" />

---

Вывод:
1. Модуль ввода-вывода (io_txt_csv.py)
-read_text() - надежная функция чтения текстовых файлов с поддержкой различных кодировок

-write_csv() - универсальная функция записи CSV-файлов с валидацией данных

-make_parent_dir() - вспомогательная функция для автоматического создания структуры директорий

2. Система генерации отчетов (text_report.py)
-Интеграция с модулем текстовой обработки из ЛР3

-Автоматический подсчет статистики слов

-Генерация структурированных CSV-отчетов

-Вывод сводной информации в консоль

3. Практические навыки, полученные в работе:
-Работа с файловой системой - использование pathlib для кроссплатформенных путей

-Обработка текстовых данных - чтение файлов в разных кодировках, обработка исключений

-Формирование CSV-отчетов - структурированный вывод данных с заголовками

-Модульная архитектура - переиспользование кода из предыдущих лабораторных работ

-Обработка краевых случаев - пустые файлы, отсутствующие директории, ошибки кодировки
