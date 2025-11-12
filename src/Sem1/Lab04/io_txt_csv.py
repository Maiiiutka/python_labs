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