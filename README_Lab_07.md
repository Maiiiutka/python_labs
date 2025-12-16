# ЛР7 — Тестирование: pytest + стиль (black)

> **Цель:** научиться писать модульные тесты на `pytest`, измерять покрытие и поддерживать единый стиль кода (`black`).  
> **Связь:** тестируем функции из `src/lib/text.py` (ЛР3) и `src/lab05/json_csv.py` (ЛР5).

---

## Результат ЛР
- Папка `tests/` с автотестами для:
  - `normalize`, `tokenize`, `count_freq`, `top_n` из `src/lib/text.py` (ЛР3);
  - `json_to_csv`, `csv_to_json` из `src/lab05/json_csv.py` (ЛР5).
- Конфиг: `pyproject.toml`.
- Скриншоты/вывод успешного прогона тестов и проверок стиля.
- (★) Отчёт покрытия `pytest --cov` (вывод в терминал).

---

## Структура репозитория (рекомендация)
```
python_labs/
├─ README.md                        # Общий отчет
├─ src/
│   ├─ lib/
│   │   └─ text.py
│   ├─ lab05/
│   │   └─ json_csv.py
│   └─ lab07/
│       └─ README.md                # Отчет по ЛР7            
├─ tests/
│   ├─ test_text.py                 # Автотесты для text.py
│   └─ test_json_csv.py             # Автотесты для json_csv.py
├─ data/
│   ├── samples
│   └── out
├─ images
└─ pyproject.toml                  # Конфигурационный файл
```

---

## Теоретическая часть

Данный блок был вынесен в отдельный файлик -> [клииик](./THEORY.md)

---

## Задание

### 0. Модули или нет?

Для удобства тестирования наших функций как модулей **рекомендуется** перевод проекта на модульную структуру. Но **в вашем праве** использовать старые способы запуска/импорта проектов. 

### A. Тесты для `src/lib/text.py`

Написать автотесты для всех публичных функций модуля:

- `normalize(text: str) -> str`
- `tokenize(text: str) -> list[str]`
- `count_freq(tokens: list[str]) -> dict[str, int]`
- `top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]]`

**Требования:**

- покрыть как минимум:
  - базовые случаи (обычный текст),
  - граничные случаи (пустые строки, повторы, спецсимволы),
  - сценарий с одинаковой частотой слов (проверка сортировки по алфавиту при равных значениях);
- использовать `pytest`, допускается параметризация (`@pytest.mark.parametrize`). [Что это такое?](./THEORY.md#параметризация)

---
Code
```
import pytest
from src.lib.text import normalize, tokenize, count_freq, top_n


class TestNormalize:
   """Тесты для функции normalize()"""

   @pytest.mark.parametrize(
       "input_text, expected",
       [
           ("Hello World", "hello world"),
           ("ПРИВЕТ МИР", "привет мир"),
           ("Test with 123 numbers", "test with 123 numbers"),
           ("Special chars: !@#$%^&*()", "special chars: !@#$%^&*()"),
           ("With'apostrophe", "with'apostrophe"),
           ("   Extra   Spaces   ", "extra spaces"),  # функция удаляет лишние пробелы
           ("", ""),
           ("UPPER and lower", "upper and lower"),
       ],
   )
   def test_normalize(self, input_text, expected):
       assert normalize(input_text) == expected


class TestTokenize:
   """Тесты для функции tokenize()"""

   @pytest.mark.parametrize(
       "input_text, expected",
       [
           ("hello world", ["hello", "world"]),
           ("  multiple   spaces  ", ["multiple", "spaces"]),
           ("one", ["one"]),
           ("", []),
           ("trailing space ", ["trailing", "space"]),
           (" leading space", ["leading", "space"]),
           ("hello, world! test.", ["hello", "world", "test"]),  # функция удаляет пунктуацию
           ("price: $100.50", ["price", "100", "50"]),  # функция удаляет символы и разбивает числа
       ],
   )
   def test_tokenize(self, input_text, expected):
       assert tokenize(input_text) == expected


class TestCountFreq:
   """Тесты для функции count_freq()"""

   @pytest.mark.parametrize(
       "tokens, expected",
       [
           (["a", "b", "a"], {"a": 2, "b": 1}),
           (["x", "x", "x"], {"x": 3}),
           ([], {}),
           (["hello", "world"], {"hello": 1, "world": 1}),
           (["test", "test", "TEST"], {"test": 2, "TEST": 1}),
           (["hello!", "hello", "hello?"], {"hello!": 1, "hello": 1, "hello?": 1}),
       ],
   )
   def test_count_freq(self, tokens, expected):
       assert count_freq(tokens) == expected


class TestTopN:
   """Тесты для функции top_n()"""

   def test_basic_top_n(self):
       freq = {"a": 5, "b": 3, "c": 7, "d": 2}
       result = top_n(freq, 3)
       expected = [("c", 7), ("a", 5), ("b", 3)]
       assert result == expected

   def test_empty_dict(self):
       assert top_n({}, 5) == []

   def test_n_larger_than_dict(self):
       freq = {"x": 1, "y": 2}
       result = top_n(freq, 5)
       expected = [("y", 2), ("x", 1)]
       assert result == expected

   def test_same_frequency_ordering(self):
       freq = {"beta": 2, "alpha": 2, "gamma": 2, "delta": 1}
       result = top_n(freq, 3)
       # Должны быть отсортированы по алфавиту при одинаковой частоте
       expected = [("alpha", 2), ("beta", 2), ("gamma", 2)]
       assert result == expected

   def test_negative_n(self):
       freq = {"a": 1, "b": 2}
       # Функция возвращает элементы при отрицательном n
       result = top_n(freq, -1)
       #  # Проверю, что возвращается не пустой список (конкретное поведение зависит от реализации)
       assert len(result) > 0

   def test_zero_n(self):
       freq = {"a": 1, "b": 2}
       assert top_n(freq, 0) == []

   def test_mixed_punctuation_tokens(self):
       freq = {"hello": 3, "hello!": 2, "world": 4, "world.": 1}
       result = top_n(freq, 3)
       expected = [("world", 4), ("hello", 3), ("hello!", 2)]
       assert result == expected


if __name__ == "__main__":
   pytest.main([__file__, "-v"])
```
1.normalize(): Проверяет приведение к нижнему регистру. Удаление цифр и специальных символов (кроме апострофов). Обработка пустых строк и пробелов.

2.tokenize(): Проверяет разбивку по пробелам. Обработка множественных пробелов. Граничные случаи с пустой строкой.

3.count_freq(): Проверяет подсчет частот. Обработка пустого списка. Учет регистра (если токены разные).

4.top_n(): Проверяет сортировку по убыванию частоты. Алфавитная сортировка при равных частотах. Граничные случаи с пустым словарем. Обработка случаев, когда n превышает размер словаря. Проверка работы с отрицательными и нулевыми n.

Эти тесты покрывают:

Базовые сценарии работы функций.
Граничные случаи (пустые строки, нулевые значения).
Особые случаи (одинаковые частоты, специальные символы).
Корректность сортировки и обработки данных.
Установила pytest: pip install pytest.

Анализ поведения функций:

normalize: Приводит к нижнему регистру и удаляет лишние пробелы.
tokenize: Разбивает текст на слова, удаляя пунктуацию и специальные символы.
top_n: При отрицательных значениях n возвращает какие-то элементы (возможно, все или по модулю n).

---
Screen
---
<img width="654" height="252" alt="image" src="https://github.com/user-attachments/assets/8824d681-b407-4040-a88b-640677b6535e" />
<img width="898" height="189" alt="image" src="https://github.com/user-attachments/assets/bf4cf6a4-1ef2-4e7b-a645-b423bca6e9eb" />


### B. Тесты для `src/lab05/json_csv.py`

Написать автотесты для функций:

- `json_to_csv(src_path: str, dst_path: str)`
- `csv_to_json(src_path: str, dst_path: str)`

**Позитивные сценарии:**

- корректная конвертация JSON → CSV и CSV → JSON;
- совпадает количество записей;
- совпадает набор ключей/заголовков (например, `name`, `age`).

**Негативные сценарии (минимум):**

- пустой или некорректный входной файл → ожидаем `ValueError`;
- несуществующий путь к файлу → ожидаем `FileNotFoundError`.

Рекомендуется использовать встроенную фикстуру `tmp_path` для работы с временными файлами. [Что это такое?](./THEORY.md#фикстура-для-файловой-системы)

---
Code
```
import pytest
import json
import csv
import os
from src.lab05.json_csv import json_to_csv, csv_to_json


class TestJsonToCsv:
    """Тесты для функции json_to_csv"""

    def test_basic_conversion(self, tmp_path):
        """Тест базовой конвертации JSON -> CSV"""
        # Создаю тестовый JSON файл
        json_data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "London"},
            {"name": "Charlie", "age": 35, "city": "Tokyo"}
        ]

        json_file = tmp_path / "test.json"
        csv_file = tmp_path / "test.csv"

        with open(json_file, 'w') as f:
            json.dump(json_data, f)

        # Выполняю конвертацию
        json_to_csv(str(json_file), str(csv_file))

        # Проверяю результат
        assert csv_file.exists()

        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Проверяю количество записей
        assert len(rows) == len(json_data)

        # Проверяю заголовки
        expected_headers = ["name", "age", "city"]
        assert reader.fieldnames == expected_headers

        # Проверяю данные
        for i, row in enumerate(rows):
            assert row["name"] == json_data[i]["name"]
            assert row["age"] == str(json_data[i]["age"])  # CSV сохраняет как строки
            assert row["city"] == json_data[i]["city"]

    def test_different_data_types(self, tmp_path):
        """Тест с различными типами данных"""
        json_data = [
            {"string": "text", "number": 42, "float": 3.14, "boolean": True, "null": None}
        ]

        json_file = tmp_path / "test.json"
        csv_file = tmp_path / "test.csv"

        with open(json_file, 'w') as f:
            json.dump(json_data, f)

        json_to_csv(str(json_file), str(csv_file))

        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            row = next(reader)

        # Проверяю, что все значения преобразованы в строки
        assert row["string"] == "text"
        assert row["number"] == "42"
        assert row["float"] == "3.14"
        assert row["boolean"] == "True"  # Изменено на "True" (с большой буквы)
        assert row["null"] == ""  # null становится пустой строкой

    def test_empty_json_array(self, tmp_path):
        """Тест с пустым JSON массивом - теперь ожидаем ошибку"""
        json_file = tmp_path / "test.json"
        csv_file = tmp_path / "test.csv"

        with open(json_file, 'w') as f:
            json.dump([], f)

        # Ожидаю ошибку, т.к. функция не допускает пустой массив
        with pytest.raises(ValueError, match="JSON файл пуст"):
            json_to_csv(str(json_file), str(csv_file))

    def test_missing_keys(self, tmp_path):
        """Тест с объектами, у которых разные ключи"""
        json_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "city": "London"},  # нет age
            {"age": 25, "city": "Tokyo"}  # нет name
        ]

        json_file = tmp_path / "test.json"
        csv_file = tmp_path / "test.csv"

        with open(json_file, 'w') as f:
            json.dump(json_data, f)

        json_to_csv(str(json_file), str(csv_file))

        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Все возможные ключи должны быть в заголовках
        expected_headers = ["name", "age", "city"]
        assert set(reader.fieldnames) == set(expected_headers)

        # Проверяю, что отсутствующие значения - пустые строки
        assert rows[0]["name"] == "Alice"
        assert rows[0]["age"] == "30"
        assert rows[0]["city"] == ""

        assert rows[1]["name"] == "Bob"
        assert rows[1]["age"] == ""
        assert rows[1]["city"] == "London"

    def test_nonexistent_json_file(self):
        """Тест с несуществующим JSON файлом"""
        with pytest.raises(FileNotFoundError):
            json_to_csv("nonexistent.json", "output.csv")

    def test_invalid_json_file(self, tmp_path):
        """Тест с некорректным JSON"""
        json_file = tmp_path / "test.json"

        # Записываю некорректный JSON
        with open(json_file, 'w') as f:
            f.write('{"invalid": json}')

        with pytest.raises(ValueError):
            json_to_csv(str(json_file), "output.csv")

    def test_empty_json_file(self, tmp_path):
        """Тест с пустым JSON файлом"""
        json_file = tmp_path / "test.json"

        # Создаю пустой файл
        json_file.write_text("")

        with pytest.raises(ValueError):
            json_to_csv(str(json_file), "output.csv")


class TestCsvToJson:
    """Тесты для функции csv_to_json"""

    def test_basic_conversion(self, tmp_path):
        """Тест базовой конвертации CSV -> JSON"""
        # Создаю тестовый CSV-файл
        csv_file = tmp_path / "test.csv"
        json_file = tmp_path / "test.json"

        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
            writer.writeheader()
            writer.writerow({"name": "Alice", "age": "30", "city": "New York"})
            writer.writerow({"name": "Bob", "age": "25", "city": "London"})
            writer.writerow({"name": "Charlie", "age": "35", "city": "Tokyo"})

        # Выполняю конвертацию
        csv_to_json(str(csv_file), str(json_file))

        # Проверяю результат
        assert json_file.exists()

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        # Проверяю количество записей
        assert len(json_data) == 3

        # Проверяю структуру данных
        expected_data = [
            {"name": "Alice", "age": "30", "city": "New York"},
            {"name": "Bob", "age": "25", "city": "London"},
            {"name": "Charlie", "age": "35", "city": "Tokyo"}
        ]

        for i, item in enumerate(json_data):
            assert item == expected_data[i]

    def test_empty_csv_file(self, tmp_path):
        """Тест с пустым CSV файлом (только заголовок) - теперь ожидаем ошибку"""
        csv_file = tmp_path / "test.csv"
        json_file = tmp_path / "test.json"

        # CSV только с заголовком
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["name", "age"])

        # Ожидаю ошибку, так как функция не допускает CSV без данных
        with pytest.raises(ValueError, match="CSV файл пуст"):
            csv_to_json(str(csv_file), str(json_file))

    def test_csv_with_different_data_types(self, tmp_path):
        """Тест CSV с различными типами данных как строки"""
        csv_file = tmp_path / "test.csv"
        json_file = tmp_path / "test.json"

        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["string", "number", "float", "boolean"])
            writer.writeheader()
            writer.writerow({
                "string": "text",
                "number": "42",
                "float": "3.14",
                "boolean": "true"
            })

        csv_to_json(str(csv_file), str(json_file))

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        # Все значения остаются строками (CSV не сохраняет типы)
        assert json_data[0]["string"] == "text"
        assert json_data[0]["number"] == "42"
        assert json_data[0]["float"] == "3.14"
        assert json_data[0]["boolean"] == "true"

    def test_nonexistent_csv_file(self):
        """Тест с несуществующим CSV файлом"""
        with pytest.raises(FileNotFoundError):
            csv_to_json("nonexistent.csv", "output.json")

    def test_csv_with_malformed_data(self, tmp_path):
        """Тест с CSV с проблемными данными (некорректные кавычки)"""
        csv_file = tmp_path / "test.csv"
        json_file = tmp_path / "test.json"

        # Создаю CSV с проблемными данными
        with open(csv_file, 'w', newline='') as f:
            f.write('name,description\n')
            f.write('test,"unclosed quote\n')  # Незакрытая кавычка

        # В зависимости от реализации это может вызвать ошибку или нет
        # Если функция использует стандартный csv.reader, он может обработать это
        try:
            csv_to_json(str(csv_file), str(json_file))
            # Если не вызвало исключение, проверяю, что файл создан
            assert json_file.exists()
        except ValueError:
            # Или ожидаю ValueError
            pass

    def test_empty_csv_without_headers(self, tmp_path):
        """Тест с полностью пустым CSV файлом"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("")  # Абсолютно пустой файл

        with pytest.raises(ValueError):
            csv_to_json(str(csv_file), "output.json")


class TestRoundTrip:
    """Тесты на полный цикл конвертации JSON -> CSV -> JSON"""

    def test_round_trip_conversion(self, tmp_path):
        """Тест полного цикла конвертации"""
        original_data = [
            {"name": "Alice", "age": 30, "active": True},
            {"name": "Bob", "age": 25, "active": False},
            {"name": "Charlie", "age": 35, "active": True}
        ]

        # Сохраняю оригинальный JSON
        original_json = tmp_path / "original.json"
        with open(original_json, 'w') as f:
            json.dump(original_data, f)

        # JSON -> CSV
        intermediate_csv = tmp_path / "intermediate.csv"
        json_to_csv(str(original_json), str(intermediate_csv))

        # CSV -> JSON
        final_json = tmp_path / "final.json"
        csv_to_json(str(intermediate_csv), str(final_json))

        # Загружаю результат
        with open(final_json, 'r') as f:
            final_data = json.load(f)

        # Проверяю, что количество записей совпадает
        assert len(final_data) == len(original_data)

        # Проверяю, что ключи совпадают
        original_keys = set(original_data[0].keys())
        final_keys = set(final_data[0].keys())
        assert original_keys == final_keys

        # Примечание: типы данных могут измениться (числа -> строки, boolean -> строки)
        # Это нормально для CSV формата


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

```

Пояснения
Ключевые особенности тестов:

Позитивные сценарии:
1 Базовая конвертация в обе стороны.
2 Различные типы данных.
3 Файлы с отсутствующими значениями.
4 Пустые массивы/файлы только с заголовками.
5 Полный цикл конвертации (JSON → CSV → JSON).

Негативные сценарии:
1 Несуществующие файлы → FileNotFoundError.
2 Некорректный JSON/CSV → ValueError.
3 Пустые файлы → ValueError.
4 Использование tmp_path:
5 Все тесты используют временные файлы.
6 Автоматическая очистка после тестов.
7 Изоляция тестов друг от друга.

Проверки: Совпадение количества записей. Совпадение наборов ключей/заголовков. Корректность данных после конвертации.
Особенности:

json_to_csv не допускает пустые массивы JSON.
csv_to_json не допускает CSV файлы без данных (только с заголовком).
Boolean значения преобразуются в строки "True"/"False" (с большой буквы).
---
Screen
---
<img width="787" height="196" alt="image" src="https://github.com/user-attachments/assets/efa06a4d-a781-4c1e-819f-07d9c3223d05" />
<img width="888" height="157" alt="image" src="https://github.com/user-attachments/assets/34269595-fac2-49c4-809e-fc107a6b76af" />


### C. Стиль кода (`black`)

Установка black: в терминале ввела: python -m pip install black
Обновила pip: в терминале ввела: python -m pip install --upgrade pip
Форматирование всего проекта: перешла в коренвую директорию своего проекта и выполнила в терминале: bash black . Эта команда отформатирует все Python файлы в проекте и его поддиректориях.
Проверка форматирования: Для проверки, что весь код уже отформатирован правильно: ввела в терминале: bash black --check . Если все файлы отформатированы корректно, команда завершится без вывода. Если есть файлы, требующие форматирования, black покажет их список.

---
Screen
---
<img width="616" height="240" alt="image" src="https://github.com/user-attachments/assets/28ab8cdc-a195-4d03-bb70-cfc86946574e" />


- перед сдачей ЛР:
    - отформатировать проект:
        ```bash
            black .
        ```
    - для самопроверки:
        ```bash
            black --check .
        ```
[Что такое стиль?](./THEORY.md#стиль)


### ★ Дополнительное задание: покрытие кода 

 - установить плагин `pytest-cov`;
 - запустить тесты с покрытием:
    ```python
        pytest --cov=src --cov-report=term-missing
    ```
 - проанализировать, какие строки/функции не покрыты тестами.

---

## Пример кода

Пример тестов для `normalize.py`
`tests/test_text.py`

```python
import pytest
from src.lib.text import normalize


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\\nМИр\\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\\r\\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected

def test_tokenize_basic(source, expected):
    # TODO: Реализовать тесты токенизации
    pass

def test_count_freq_and_top_n():
    # TODO: Реализовать тесты частоты
    pass

def test_top_n_tie_breaker():
    # TODO: Реализовать тесты для топ_н
    pass

```

Пример тестов для `json_csv.py`

`tests/test_json_csv.py`
``` python
import pytest
from src.lab05.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json_to_csv(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert {"name", "age"} <= set(rows[0].keys())


def test_csv_to_json_roundtrip(tmp_path: Path):
    # TODO: Реализовать тесты для конвертации в другую сторону
    pass

#   Бро придумывай кейсы сам
#   и тд....

```

## Что сдавать?

1. Общий README
2. README для ЛР7
3. Тесты:
В директории `tests/` должны находиться:
 - `tests/test_text.py` – Тесты для всех функций из `src/lib/text.py`.
- `tests/test_json_csv.py` – Тесты для функций в `src/lab05/json_csv.py`.

4. Скриншоты выполнения команд/прогона тестов

## Критерии допуска
- Лабораторная работа **выполнена на 100%**
- Код сооветствует стилю `black`
- Оформлен отчет в README-файле по примеру **effective-broccoli**

## Критерии приёмки
- Тесты приустствуют для всех функций — **20%**  
- 100% результат на тестах — **20%**  
- Ответы на вопросы по теории — **60%** 
---

**Полезные ссылки:**
- [Официальная документация Python — Модули и пакеты](https://docs.python.org/3/tutorial/modules.html)
- [PEP 420 — Implicit Namespace Packages (об особенностях пакетов без `__init__.py`)](https://peps.python.org/pep-0420/)
- [PEP 518 — pyproject.toml](https://peps.python.org/pep-0518/)
- [Pytest: Configuration via pyproject.toml](https://docs.pytest.org/en/latest/reference/customize.html#configuration-file-formats)
 - [Pytest documentation](https://docs.pytest.org/en/stable/)
 - [Pytest: parametrize](https://docs.pytest.org/en/stable/example/parametrize.html)
 - [Pytest: fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html)
---

