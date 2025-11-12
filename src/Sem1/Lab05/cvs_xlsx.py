import csv
from pathlib import Path
from openpyxl import Workbook

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    
    Args:
        csv_path: Путь к исходному CSV файлу
        xlsx_path: Путь для сохранения XLSX файла
        
    Raises:
        FileNotFoundError: Если исходный файл не существует
        ValueError: Если CSV пустой или отсутствует заголовок
    """
    
    # Создание Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Чтение CSV
    with open(csv_path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            ws.append(row)
    
    # Сохранение
    Path(xlsx_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path)


if __name__ == "__main__":
    # Тестирование функции
    try:
        csv_to_xlsx("./data/Lab05/samples/people.csv", "./data/Lab05/out/people.xlsx")
        print("CSV -> XLSX успешно")
        
        # Дополнительный пример
        csv_to_xlsx("./data/Lab05/samples/cities.csv", "./data/Lab05/out/cities.xlsx")
        print("CSV -> XLSX (cities) успешно")
        
    except Exception as e:
        print(f"Ошибка: {e}")