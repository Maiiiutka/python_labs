
# ЛР3 — Тексты и частоты слов (словарь/множество)

> **Цель:** нормализовать текст, аккуратно токенизировать, посчитать частоты слов и вывести топ-N.  
> **Связь:** продолжение ЛР2 (работа со списками) и подготовка к ЛР4 (файлы) — модуль `lib/text.py` будем переиспользовать.

---

## Результат ЛР
- Модуль `src/lib/text.py` с чистыми функциями: `normalize`, `tokenize`, `count_freq`, `top_n`.  
- Скрипт `src/lab03/text_stats.py`, читающий вход из **stdin** и печатающий базовую статистику.  
- README с **кодом** в виде текста, примерами входа/выхода и скриншотами запуска.  
- **Только стандартная библиотека** (никаких NLTK и т.п.). Python **3.хх+**.

---

## Задание A — `src/lib/text.py`

Реализуйте функции:

1. `normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str`  
   - Если `casefold=True` — привести к **casefold** (лучше, чем `lower` для Юникода).  
   - Если `yo2e=True` — заменить все `ё`/`Ё` на `е`/`Е`.  
   - Убрать невидимые управляющие символы (например, `\t`, `\r`) → заменить на пробелы, схлопнуть повторяющиеся пробелы в один.

2. `tokenize(text: str) -> list[str]`  
   - Разбить на «слова» по небуквенно-цифровым разделителям.  
   - В качестве слова считаем последовательности символов `\w` (буквы/цифры/подчёркивание) **плюс** дефис внутри слова (например, `по-настоящему`).  
   - Числа (например, `2025`) считаем словами.

3. `count_freq(tokens: list[str]) -> dict[str, int]`  
   - Подсчитать частоты, вернуть словарь `слово → количество`.

4. `top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]`  
   - Вернуть топ-N по убыванию частоты; при равенстве — по алфавиту слова.

### Тест-кейсы

**normalize**
- `"ПрИвЕт\nМИр\t"` → `"привет мир"` (casefold + схлопнуть пробелы)  
- `"ёжик, Ёлка"` (`yo2e=True`) → `"ежик, елка"`  
- `"Hello\r\nWorld"` → `"hello world"`  
- `"  двойные   пробелы  "` → `"двойные пробелы"`

**tokenize** *(предполагаем, что текст уже normalize)*
- `"привет мир"` → `["привет", "мир"]`  
- `"hello,world!!!"` → `["hello", "world"]`  
- `"по-настоящему круто"` → `["по-настоящему", "круто"]`  
- `"2025 год"` → `["2025", "год"]`  
- `"emoji 😀 не слово"` → `["emoji", "не", "слово"]` (эмодзи выпадают)

**count_freq + top_n**
- Токены `["a","b","a","c","b","a"]` → частоты `{"a":3,"b":2,"c":1}`;  
  `top_n(..., n=2)` → `[("a",3), ("b",2)]`  
- При равенстве частот: токены `["bb","aa","bb","aa","cc"]` → частоты `{"aa":2,"bb":2,"cc":1}`;  
  `top_n(..., n=2)` → `[("aa",2), ("bb",2)]` (алфавитная сортировка при равенстве).

---

*Code*

```

import re
from typing import Dict, List, Tuple

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    if not text:
        return ""
    
    result = text
    
    if yo2e:
        result = result.replace('ё', 'е').replace('Ё', 'Е')
    
    if casefold:
        result = result.casefold()
    
    control_chars = {'\\t', '\\r', '\\n'}
    for char in control_chars:
        result = result.replace(char, ' ')
    
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result


def tokenize(text: str):
    if not text:
        return []
    pattern = r'\w+(?:-\w+)*'
    tokens = re.findall(pattern, text)
    
    return tokens


def count_freq(tokens: List[str]):
    freq_dict = {}
    
    for token in tokens:
        if not token or not any(c.isalpha() for c in token):
            continue
            
        freq_dict[token] = freq_dict.get(token, 0) + 1
    
    return freq_dict


#def top_n(freq: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    if not freq:
        return []
    
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_items[:n]

def top_n(data, n: int = 5):
    freq = {}
    
    if isinstance(data, list):
        freq = count_freq(data)
    elif isinstance(data, dict):
        freq = data
    else:
        return []
    
    if not freq:
        return []
    
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    return sorted_items[:n]

x = int(input())

if x == 1:
    s = input()
    a = normalize(s)
    print(a)
elif x == 2:
    s = input()
    a = tokenize(s)
    print(a)
elif x == 3:
    s = input()
    a = count_freq(s)
    print(a)
elif x == 4:
    s = input()
    n = int(input())
    s_clean = s.strip('[]\"\'')
    items = [item.strip(' \"\'') for item in s_clean.split(',') if item.strip()]
    a = top_n(items, n)
    print(a)

```

*Screen*

<img width="495" height="397" alt="1" src="https://github.com/user-attachments/assets/e499e64e-fa64-49fb-9fa5-6c03409c4ab5" />
<img width="425" height="364" alt="2" src="https://github.com/user-attachments/assets/b0ccae31-dbcf-4f99-800c-8b6583d25bda" />
<img width="351" height="277" alt="3" src="https://github.com/user-attachments/assets/852287e5-e8bb-48ec-b017-7760b06c7198" />
<img width="442" height="356" alt="4" src="https://github.com/user-attachments/assets/7b26503c-0359-4595-9330-fbe1bf2b3c98" />

---

## Задание B — `src/text_stats.py` (скрипт со stdin)

Скрипт читает одну строку текста из **stdin** (или весь ввод до EOF — на ваш выбор, опишите в README), вызывает функции из `lib/text.py` и печатает:

1. `Всего слов: <N>`  
2. `Уникальных слов: <K>`  
3. `Топ-5:` — по строке на запись в формате `слово:кол-во` (по убыванию, как в `top_n`).

### Пример запуска
В терминале:
```
$ echo "Привет, мир! Привет!!!" | python src/text_stats.py
Всего слов: 3
Уникальных слов: 2
Топ-5:
привет:2
мир:1
```

--- 

*Code*

```

from lib.text import normalize, tokenize, count_freq, top_n

text = input("Введите текст: ")

normalized_text = normalize(text)
tokens = tokenize(normalized_text)

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

*Screen*

<img width="569" height="422" alt="5" src="https://github.com/user-attachments/assets/5e8de5d3-2163-4d87-b75f-566baed60400" />

---

### Вывод:
В лабораторной работе №3 успешно разработана система анализа текстовой статистики. Реализованы 4 основные функции: normalize() для нормализации текста, tokenize() для разбивки на слова, count_freq() для подсчета частот и top_n() для вывода наиболее частых слов. Создана программа text_stats.py, которая читает текст из stdin и выводит статистику: общее количество слов, количество уникальных слов и топ-5 самых частых слов. Все функции протестированы и готовы к переиспользованию в следующих лабораторных работах.
