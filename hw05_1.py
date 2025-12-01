class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """Видаляє пару ключ-значення з таблиці."""
        key_hash = self.hash_function(key)
        
        # Перевіряємо, чи є записи за цим хешем
        if self.table[key_hash] is not None:
            # Проходимо по списку в пошуках ключа
            for i in range(len(self.table[key_hash])):
                if self.table[key_hash][i][0] == key:
                    # Видаляємо елемент за індексом
                    self.table[key_hash].pop(i)
                    return True # Успішно видалено
        
        return False # Ключ не знайдено

# --- ТЕСТУВАННЯ ---

H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print("--- Початковий стан ---")
print(f"Apple: {H.get('apple')}")
print(f"Orange: {H.get('orange')}")
print(f"Banana: {H.get('banana')}")

print("\n--- Видалення ---")
print(f"Видаляємо 'orange': {H.delete('orange')}")  # Має повернути True
print(f"Видаляємо 'cherry' (не існує): {H.delete('cherry')}") # Має повернути False

print("\n--- Перевірка після видалення ---")
print(f"Apple: {H.get('apple')}")   # 10
print(f"Orange: {H.get('orange')}") # None (бо видалено)
print(f"Banana: {H.get('banana')}") # 30