def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """
    Вернуть отсортированный список уникальных значений (по возрастанию).
    """
    # Используем set для получения уникальных значений, затем сортируем
    return sorted(set(nums))