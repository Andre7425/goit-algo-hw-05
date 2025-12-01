def binary_search(arr, target):
    """
    Виконує двійковий пошук у відсортованому масиві дробових чисел.
    
    Args:
        arr (list[float]): Відсортований список чисел.
        target (float): Значення, яке шукаємо.
        
    Returns:
        tuple: (кількість_ітерацій, верхня_межа)
               верхня_межа - це найменший елемент у масиві, який >= target.
               Якщо всі елементи менші за target, повертає None.
    """
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        
        # Якщо елемент посередині менший за ціль,
        # то шукаємо в правій половині (нам потрібні більші значення).
        if arr[mid] < target:
            low = mid + 1
        else:
            # Якщо arr[mid] >= target, то це потенційний кандидат на "upper_bound".
            # Ми запам'ятовуємо його.
            upper_bound = arr[mid]
            
            # Але, можливо, зліва є ще менший елемент, який все одно >= target.
            # Тому ми продовжуємо пошук у лівій частині, щоб знайти "найменший з більших".
            high = mid - 1

    return (iterations, upper_bound)

# --- ТЕСТУВАННЯ ---

if __name__ == "__main__":
    # Відсортований масив дробових чисел
    sorted_floats = [0.1, 0.5, 1.3, 2.4, 3.6, 4.8, 5.5, 6.2, 7.9, 8.1]
    
    # Тестові сценарії
    test_targets = [
        3.0,  # Очікуємо upper_bound = 3.6
        6.2,  # Точне співпадіння, очікуємо upper_bound = 6.2
        0.05, # Менше за всі елементи, очікуємо upper_bound = 0.1
        10.0  # Більше за всі елементи, очікуємо upper_bound = None
    ]

    print(f"Масив: {sorted_floats}\n")

    for t in test_targets:
        result = binary_search(sorted_floats, t)
        print(f"Ціль: {t:<5} -> Ітерацій: {result[0]}, Верхня межа: {result[1]}")