import timeit
import os

# --- РЕАЛІЗАЦІЯ АЛГОРИТМІВ ---

# 1. Алгоритм Боєра-Мура (Boyer-Moore)
def build_shift_table(pattern):
    """Створює таблицю зміщень для евристики поганого символу."""
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    n = len(text)
    m = len(pattern)
    
    if m == 0: return 0
    
    i = m - 1
    
    while i < n:
        j = 0
        while j < m and text[i - j] == pattern[m - 1 - j]:
            j += 1
        
        if j == m:
            return i - m + 1 # Знайдено входження
        else:
            # Зсув на основі таблиці або на 1, якщо символу немає в таблиці
            bad_char = text[i - j]
            shift = shift_table.get(bad_char, m)
            # Евристика: зсув має бути не менше 1 і враховувати поточне порівняння
            # Для спрощення використовуємо max(1, shift - j) або просто shift
            # Тут використовуємо базову логіку поганого символу
            i += shift

    return -1

# 2. Алгоритм Кнута-Морріса-Пратта (KMP)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    
    if M == 0: return 0

    lps = compute_lps(pattern)
    i = 0 # індекс для text
    j = 0 # індекс для pattern
    
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == M:
            return i - j # Знайдено входження
            # j = lps[j-1] # Якщо потрібно шукати далі
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1

# 3. Алгоритм Рабіна-Карпа (Rabin-Karp)
def rabin_karp_search(text, pattern):
    d = 256 # Кількість символів в алфавіті
    q = 101 # Просте число для хешування
    M = len(pattern)
    N = len(text)
    
    if M == 0: return 0
    
    p = 0 # хеш для патерну
    t = 0 # хеш для тексту
    h = 1
    
    # Значення h = pow(d, M-1) % q
    for i in range(M-1):
        h = (h * d) % q
        
    # Обчислення хешу для патерну і першого вікна тексту
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
        
    for i in range(N - M + 1):
        if p == t:
            # Якщо хеші співпадають, перевіряємо символи
            if text[i:i+M] == pattern:
                return i
        
        if i < N - M:
            t = (d*(t - ord(text[i])*h) + ord(text[i+M])) % q
            if t < 0:
                t = t + q
    return -1

# --- ТЕСТУВАННЯ ---

def read_file(filename):
    try:
        # Спочатку пробуємо відкрити як utf-8
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            # Якщо не вийшло, пробуємо "рідне" кодування Windows (cp1251)
            with open(filename, 'r', encoding='cp1251') as f:
                return f.read()
        except UnicodeDecodeError:
             print(f"Помилка: Не вдалося розпізнати кодування файлу '{filename}'.")
             return ""
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return ""

def measure_time(algorithm, text, pattern):
    # number=100 означає, що ми проженемо пошук 100 разів для точності
    timer = timeit.timeit(lambda: algorithm(text, pattern), number=100)
    return timer

def main():
    file1 = "стаття_1.txt"
    file2 = "стаття_2.txt"
    
    text1 = read_file(file1)
    text2 = read_file(file2)
    
    if not text1 or not text2:
        return

    # Підрядки для Статті 1 (Алгоритми)
    sub1_real = "алгоритм"       # Існує
    sub1_fake = "реактивний двигун" # Не існує

    # Підрядки для Статті 2 (Бази даних)
    sub2_real = "рекомендацій"   # Існує
    sub2_fake = "нейронна мережа"   # Не існує

    tasks = [
        ("Стаття 1", text1, sub1_real, "Існує"),
        ("Стаття 1", text1, sub1_fake, "Не існує"),
        ("Стаття 2", text2, sub2_real, "Існує"),
        ("Стаття 2", text2, sub2_fake, "Не існує")
    ]
    
    print(f"{'Стаття':<10} | {'Підрядок':<20} | {'Статус':<10} | {'Boyer-Moore':<12}| {'KMP':<12}| {'Rabin-Karp':<12}")
    print("-" * 90)

    for article_name, text, pattern, status in tasks:
        time_bm = measure_time(boyer_moore_search, text, pattern)
        time_kmp = measure_time(kmp_search, text, pattern)
        time_rk = measure_time(rabin_karp_search, text, pattern)
        
        # Визначаємо найшвидший для цього рядка
        fastest = min(time_bm, time_kmp, time_rk)
        
        # Форматування виводу
        print(f"{article_name:<10} | {pattern[:20]:<20} | {status:<10} | {time_bm:.5f} s   | {time_kmp:.5f} s   | {time_rk:.5f} s")

    print("\n" + "="*30)
    print("Висновки (автоматичний аналіз):")
    print("Порівняйте часові показники вище. Зазвичай:")
    print("- Boyer-Moore найшвидший для звичайного тексту, особливо коли підрядка немає.")
    print("- KMP стабільний, але часто повільніший за BM.")
    print("- Rabin-Karp зазвичай найповільніший через операції хешування.")

if __name__ == "__main__":
    main()