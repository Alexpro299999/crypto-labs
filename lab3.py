# Для выполнения Задания 2 (Шифр Хилла) требуется установка библиотеки NumPy
# Вы можете установить ее, выполнив в терминале команду: pip install numpy
import numpy as np

# --- ОБЩИЕ НАСТРОЙКИ ---
# Алфавит из 29 букв, где 'я' = 0, 'а' = 1, ...
ALPHABET = "яабвгдежзиклмнопрстуфхцчшъыэю"
MOD = len(ALPHABET)

# Словари для преобразования символов в числа и обратно
CHAR_TO_NUM = {char: i for i, char in enumerate(ALPHABET)}
NUM_TO_CHAR = {i: char for i, char in enumerate(ALPHABET)}

# --- ПЕРСОНАЛЬНЫЕ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ---
LAST_NAME = "Ушаков"
FIRST_NAME = "Александр"
PATRONYMIC = "Алексеевич"
FATHER_NAME = "Алексей"
VARIANT = 16

# --- ФОРМИРОВАНИЕ СТРОК ДЛЯ ШИФРОВАНИЯ ---
# Объединяем ФИО в одну строку, приводим к нижнему регистру и нормализуем
# согласно алфавиту (ё -> е, й -> и)
FULL_NAME = (LAST_NAME + FIRST_NAME + PATRONYMIC).lower().replace('ё', 'е').replace('й', 'и')
NORMALIZED_FATHER_NAME = FATHER_NAME.lower().replace('ё', 'е').replace('й', 'и')


def solve_task_1():
    """
    Задание 1: Аффинный шифр.
    - Сообщение: первые 3 буквы ФИО.
    - Ключ y = ax + b, где a = i + 5, b = a⁻¹ mod 29.
    """
    print("--- Задание 1: Аффинный шифр ---")
    message = FULL_NAME[:3]

    a = VARIANT + 5
    # Согласно таблице обратных элементов в Z29 (стр. 7 PDF), 21⁻¹ ≡ 18 (mod 29)
    b = 18

    print(f"Исходное сообщение: '{message}'")
    print(f"Ключ: a = {a}, b = {b}")

    encrypted_message = ""
    for char in message:
        x = CHAR_TO_NUM[char]
        y = (a * x + b) % MOD
        encrypted_message += NUM_TO_CHAR[y]

    print(f"Результат шифрования: '{encrypted_message}'\n")


def solve_task_2():
    """
    Задание 2: Шифр Хилла.
    - Сообщение: первые 3 буквы ФИО.
    - Ключ: матрица K с параметром i.
    """
    print("--- Задание 2: Шифр Хилла ---")
    message = FULL_NAME[:3]

    # Формируем ключ-матрицу
    key_matrix = np.array([
        [1, 2, 3],
        [0, 4, 5],
        [0, 0, VARIANT + 3]
    ])

    print(f"Исходное сообщение: '{message}'")
    print(f"Ключ-матрица:\n{key_matrix}")

    # Преобразуем сообщение в числовой вектор
    message_vector = np.array([CHAR_TO_NUM[char] for char in message])

    # Умножаем матрицу на вектор и берем остаток от деления
    encrypted_vector = (key_matrix @ message_vector) % MOD

    # Преобразуем числовой результат обратно в строку
    encrypted_message = "".join([NUM_TO_CHAR[num] for num in encrypted_vector])

    print(f"Результат шифрования: '{encrypted_message}'\n")


def solve_task_3():
    """
    Задание 3: Шифр «Сумма оцифровок».
    - Сообщение: первые 4 буквы ФИО.
    - Ключ: Имя отца ("Алексей").
    """
    print("--- Задание 3: Шифр «Сумма оцифровок» ---")
    message = FULL_NAME[:4]
    key = NORMALIZED_FATHER_NAME

    # Если ключ длиннее сообщения, обрезаем его
    if len(key) > len(message):
        key = key[:len(message)]

    print(f"Исходное сообщение: '{message}'")
    print(f"Ключ: '{key}'")

    encrypted_message = ""
    for i in range(len(message)):
        message_num = CHAR_TO_NUM[message[i]]
        key_num = CHAR_TO_NUM[key[i]]

        # Складываем числовые значения и берем остаток от деления
        encrypted_num = (message_num + key_num) % MOD
        encrypted_message += NUM_TO_CHAR[encrypted_num]

    print(f"Результат шифрования: '{encrypted_message}'\n")


def solve_task_4():
    """
    Задание 4: Шифр перестановкой.
    - Сообщение: первые 4 буквы ФИО.
    - Перестановка: (1 3 5)(2 4 6) на блоках длиной 6.
    """
    print("--- Задание 4: Шифр перестановкой ---")
    message = FULL_NAME[:4]
    block_size = 6
    padding_char = 'а'  # Символ для дополнения блока

    # Дополняем сообщение до длины блока
    padded_message = message.ljust(block_size, padding_char)

    print(f"Исходное сообщение: '{message}'")
    print(f"Сообщение с дополнением: '{padded_message}'")

    # Перестановка означает: 1->3, 3->5, 5->1 и 2->4, 4->6, 6->2
    # Правило шифрования: "На i-е место ставим ti-ю букву исходного блока"
    # c[i] = p[t(i)]
    perm_map = {1: 3, 2: 4, 3: 5, 4: 6, 5: 1, 6: 2}
    print(f"Перестановка: (1->3->5->1), (2->4->6->2)")

    encrypted_list = [''] * block_size
    # Индексы в Python начинаются с 0, а в задании с 1
    for i in range(1, block_size + 1):
        source_index = perm_map[i] - 1
        dest_index = i - 1
        encrypted_list[dest_index] = padded_message[source_index]

    encrypted_message = "".join(encrypted_list)

    print(f"Результат шифрования: '{encrypted_message}'\n")


# --- ЗАПУСК РЕШЕНИЙ ---
if __name__ == '__main__':
    solve_task_1()
    solve_task_2()
    solve_task_3()
    solve_task_4()