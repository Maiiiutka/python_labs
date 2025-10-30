def flatten(mat: list[list | tuple]) -> list:
    """
    «Расплющить» список списков/кортежей в один список по строкам (row-major).
    Если встретилась строка/элемент, который не является списком/кортежем — TypeError.
    """
    result = []
    
    for item in mat:
        # Проверяем, является ли элемент списком или кортежем
        if not isinstance(item, (list, tuple)):
            raise TypeError(f"Элемент {item} не является списком или кортежем")
        
        # Добавляем все элементы вложенного списка/кортежа в результат
        result.extend(item)
    
    return result