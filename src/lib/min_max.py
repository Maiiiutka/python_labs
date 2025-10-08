def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """
    Вернуть кортеж (минимум, максимум). Если список пуст — ValueError.
    """
    if not nums:
        raise ValueError("Список не может быть пустым")
    
    min_val = nums[0]
    max_val = nums[0]
    
    for num in nums[1:]:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num
    
    return (min_val, max_val)