import math
import re

# -- ОБЩИЕ АЛФАВИТЫ И ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ --

# Русский алфавит из 33 букв
ALPHABET_33 = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

# Русский алфавит из 30 букв (е=ё, и=й, ъ=ь)
ALPHABET_30 = "абвгдежзиклмнопрстуфхцчшщъыэюя"

# Русский алфавит из 29 букв (е=ё, и=й, ъ=ь, ш=щ)
ALPHABET_29 = "абвгдежзиклмнопрстуфхцчшъыэюя"

# Русский алфавит из 25 букв (со слиянием гласных и некоторых согласных)
ALPHABET_25 = "абвгдежзиклмнопрстуфхцчшюя"  # Примерный, как в PDF


def prepare_text(text):
    """Приводит текст к нижнему регистру и убирает все, кроме букв."""
    text = text.lower()
    return re.sub(r'[^а-яё]', '', text)


# --- ЗАДАНИЕ 1: ШИФР ЦЕЗАРЯ ---

def caesar_cipher(text, shift, alphabet):
    """
    Шифрует текст шифром Цезаря с заданным сдвигом и алфавитом.
    """
    encrypted_text = []
    alphabet_len = len(alphabet)
    for char in text:
        if char in alphabet:
            current_pos = alphabet.find(char)
            new_pos = (current_pos + shift) % alphabet_len
            encrypted_text.append(alphabet[new_pos])
        else:
            encrypted_text.append(char)
    return "".join(encrypted_text)


def task_1(full_name_str):
    """
    Выполняет Задание 1.
    Зашифруйте шифром Цезаря со сдвигом на 6 букв Вашу «фамилияимяотчество»
    1. в алфавите из 33 букв русского алфавита
    2. в алфавите из букв, входящих в ФИО.
    """
    print("--- ЗАДАНИЕ 1: Шифр Цезаря ---")

    # Подготовка текста и параметров
    shift = 6
    prepared_name = prepare_text(full_name_str)
    print(f"Исходное сообщение: {prepared_name}")

    # 1. Шифрование с полным русским алфавитом (33 буквы)
    encrypted_full_alphabet = caesar_cipher(prepared_name, shift, ALPHABET_33)
    print(f"1. Шифротекст (алфавит 33 буквы): {encrypted_full_alphabet}")

    # 2. Создание алфавита из букв ФИО и шифрование
    fio_alphabet = "".join(sorted(list(set(prepared_name))))
    encrypted_fio_alphabet = caesar_cipher(prepared_name, shift, fio_alphabet)
    print(f"   Алфавит из ФИО ({len(fio_alphabet)} букв): {fio_alphabet}")
    print(f"2. Шифротекст (алфавит из ФИО): {encrypted_fio_alphabet}")
    print("-" * 30 + "\n")


# --- ЗАДАНИЕ 2: АТБАШ + ПЛЕЙФЕР ---

def atbash_cipher(text, alphabet):
    """Шифрует текст шифром Атбаш."""
    reversed_alphabet = alphabet[::-1]
    # Создаем таблицу для перевода символов
    translation_table = str.maketrans(alphabet, reversed_alphabet)
    return text.translate(translation_table)


def generate_playfair_matrix(keyword, alphabet, rows, cols):
    """Генерирует матрицу для шифра Плейфера."""
    key = "".join(dict.fromkeys(keyword + alphabet))  # Ключ без дублей + остаток алфавита
    matrix = [list(key[i:i + cols]) for i in range(0, len(key), cols)]
    return matrix


def find_char_coords(matrix, char):
    """Находит координаты символа в матрице."""
    for r, row_list in enumerate(matrix):
        for c, value in enumerate(row_list):
            if value == char:
                return r, c
    return None, None


def playfair_encrypt(text, keyword, alphabet, rows, cols):
    """Шифрует текст шифром Плейфера."""
    matrix = generate_playfair_matrix(keyword, alphabet, rows, cols)

    # Подготовка текста: разбиение на биграммы, обработка дублей и нечетной длины
    text = text.replace('ё', 'е').replace('й', 'и').replace('ъ', 'ь')
    i = 0
    prepared_text = []
    while i < len(text):
        char1 = text[i]
        if i + 1 == len(text):
            prepared_text.append(char1 + 'х')  # Добавляем 'х' если нечетная длина
            break
        char2 = text[i + 1]
        if char1 == char2:
            prepared_text.append(char1 + 'х')
            i += 1
        else:
            prepared_text.append(char1 + char2)
            i += 2

    # Шифрование биграмм
    ciphertext = []
    for pair in prepared_text:
        r1, c1 = find_char_coords(matrix, pair[0])
        r2, c2 = find_char_coords(matrix, pair[1])

        if r1 is None or r2 is None: continue  # Пропускаем символы не из алфавита

        if r1 == r2:  # Правило 1: одна строка
            ciphertext.append(matrix[r1][(c1 + 1) % cols])
            ciphertext.append(matrix[r2][(c2 + 1) % cols])
        elif c1 == c2:  # Правило 2: один столбец
            ciphertext.append(matrix[(r1 + 1) % rows][c1])
            ciphertext.append(matrix[(r2 + 1) % rows][c2])
        else:  # Правило 3: прямоугольник
            ciphertext.append(matrix[r1][c2])
            ciphertext.append(matrix[r2][c1])

    return "".join(ciphertext)


def task_2(full_name_str):
    """
    Выполняет Задание 2.
    Взять по три последние буквы ФИО. Зашифровать шифром Атбаш,
    а затем результат - шифром Плейфера с ключом "Евклид" в алфавите 30 букв.
    """
    print("--- ЗАДАНИЕ 2: Атбаш + Плейфер ---")

    # Подготовка
    prepared_name = prepare_text(full_name_str)
    message = prepared_name[-3:]
    keyword = "евклид"
    alphabet = ALPHABET_30.replace('ё', '').replace('й', '').replace('ъ', '')
    print(f"Исходное сообщение (3 последние буквы): {message}")

    # Шаг 1: Шифр Атбаш
    atbash_encrypted = atbash_cipher(message, alphabet)
    print(f"1. Результат после шифра Атбаш: {atbash_encrypted}")

    # Шаг 2: Шифр Плейфера
    playfair_encrypted = playfair_encrypt(atbash_encrypted, keyword, alphabet, 5, 6)
    print(f"2. Итоговый шифротекст (после Плейфера): {playfair_encrypted}")
    print("-" * 30 + "\n")


# --- ЗАДАНИЕ 3: УИТСТОН + МАРШРУТНОЕ ШИФРОВАНИЕ ---

def generate_wheatstone_matrix(key, alphabet, n, m):
    """Генерирует матрицу для шифра Уитстона."""
    # Убираем дубликаты из ключа
    unique_key = "".join(dict.fromkeys(key))
    # Убираем из алфавита буквы, которые есть в ключе
    remaining_alphabet = "".join([c for c in alphabet if c not in unique_key])

    full_sequence = unique_key + remaining_alphabet

    # Заполняем матрицу
    matrix = []
    for i in range(n):
        row = list(full_sequence[i * m: (i + 1) * m])
        # Если строка неполная, дополняем недостающими символами (например, '-')
        while len(row) < m:
            row.append('-')
        matrix.append(row)

    return matrix


def wheatstone_encrypt(text, key1, key2, first_name, father_name):
    """Шифрует текст шифром Уитстона."""
    # 1. Создание алфавита
    alphabet_text = prepare_text(text + first_name + father_name)
    alphabet = "".join(sorted(list(set(alphabet_text))))
    omega_len = len(alphabet)

    # 2. Определение размеров матриц
    n = int(math.sqrt(omega_len))
    m = math.ceil(omega_len / n)

    # 3. Создание матриц
    matrix1 = generate_wheatstone_matrix(key1, alphabet, n, m)
    matrix2 = generate_wheatstone_matrix(key2, alphabet, n, m)

    # 4. Подготовка текста
    if len(text) % 2 != 0:
        text += text[0]  # Добавляем первую букву в конец, как в примере

    bigrams = [text[i:i + 2] for i in range(0, len(text), 2)]

    # 5. Шифрование
    ciphertext = []
    for pair in bigrams:
        r1, c1 = find_char_coords(matrix1, pair[0])
        r2, c2 = find_char_coords(matrix2, pair[1])

        if r1 is None or r2 is None: continue

        if r1 == r2:  # В одной строке
            ciphertext.append(matrix1[r1][c2])
            ciphertext.append(matrix2[r2][c1])
        else:  # В разных строках и столбцах (прямоугольник)
            ciphertext.append(matrix1[r1][c2])
            ciphertext.append(matrix2[r2][c1])

    return "".join(ciphertext)


def route_encrypt(text, key):
    """Шифрует текст маршрутным шифрованием."""
    key_len = len(key)

    # Создание таблицы соответствия: буква ключа -> номер столбца
    sorted_key = sorted(list(set(key)))
    key_order_map = {letter: i for i, letter in enumerate(sorted_key)}

    # Получаем порядок чтения столбцов
    # Пример "ДЕКАРТ": А(1) Д(2) Е(3) К(4) Р(5) Т(6) -> порядок [3,0,1,2,4,5]
    indexed_key = sorted([(char, i) for i, char in enumerate(key)])
    read_order = [item[1] for item in indexed_key]

    # Заполнение таблицы текстом
    num_rows = math.ceil(len(text) / key_len)
    # Дополняем текст, чтобы он полностью заполнил таблицу
    padded_text = text.ljust(num_rows * key_len, ' ')

    # Чтение по столбцам в нужном порядке
    ciphertext = []
    for col_idx in read_order:
        for row_idx in range(num_rows):
            char = padded_text[row_idx * key_len + col_idx]
            if char != ' ':  # Игнорируем добавленные пробелы
                ciphertext.append(char)

    return "".join(ciphertext)


def task_3(full_name_str, first_name_str, father_name_str):
    """
    Выполняет Задание 3.
    Взять все буквы ФИО. Зашифровать шифром Уитстона (ключи: Имя, Имя Отца).
    Результат зашифровать маршрутным шифрованием с ключом "Декарт".
    """
    print("--- ЗАДАНИЕ 3: Уитстон + Маршрутное шифрование ---")

    # Подготовка
    message = prepare_text(full_name_str)
    key1 = prepare_text(first_name_str)
    key2 = prepare_text(father_name_str)
    route_key = "декарт"
    print(f"Исходное сообщение: {message}")
    print(f"Ключ 1 (Имя): {key1}, Ключ 2 (Имя Отца): {key2}")

    # Шаг 1: Шифр Уитстона
    wheatstone_encrypted = wheatstone_encrypt(message, key1, key2, first_name_str, father_name_str)
    print(f"1. Результат после шифра Уитстона: {wheatstone_encrypted}")

    # Шаг 2: Маршрутное шифрование
    route_encrypted = route_encrypt(wheatstone_encrypted, route_key)
    print(f"2. Итоговый шифротекст (после маршрутного): {route_encrypted}")
    print("-" * 30 + "\n")


# --- ЗАДАНИЕ 4: ШИФР ПОЛИБИЯ (4 ВАРИАНТА) ---

def generate_polybius_square(alphabet, rows, cols, by_row=True):
    """Генерирует квадрат Полибия и карты для быстрого поиска."""
    letter_to_coords = {}
    coords_to_letter = {}

    if by_row:
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if idx < len(alphabet):
                    char = alphabet[idx]
                    letter_to_coords[char] = (r + 1, c + 1)
                    coords_to_letter[(r + 1, c + 1)] = char
    else:  # by_col
        for c in range(cols):
            for r in range(rows):
                idx = c * rows + r
                if idx < len(alphabet):
                    char = alphabet[idx]
                    letter_to_coords[char] = (r + 1, c + 1)
                    coords_to_letter[(r + 1, c + 1)] = char

    return letter_to_coords, coords_to_letter


def task_4(full_name_str):
    """
    Выполняет Задание 4.
    Взять три последние буквы ФИО. Зашифровать шифром Полибия 4 методами.
    """
    print("--- ЗАДАНИЕ 4: Вариации шифра Полибия ---")

    prepared_name = prepare_text(full_name_str)
    message = prepared_name[-3:]
    print(f"Исходное сообщение (3 последние буквы): {message}")

    # --- Метод 1: Соседний снизу символ ---
    alphabet1 = ALPHABET_29.replace('ё', '').replace('й', '').replace('ъ', 'ь').replace('щ', 'ш')
    rows1, cols1 = 5, 6
    l2c1, c2l1 = generate_polybius_square(alphabet1, rows1, cols1)

    encrypted1 = []
    for char in message:
        if char in l2c1:
            r, c = l2c1[char]
            new_r = (r % rows1) + 1  # Циклический сдвиг вниз
            encrypted1.append(c2l1.get((new_r, c), '?'))
    print(f"1. Метод 'соседний снизу': {''.join(encrypted1)}")

    # --- Метод 2: Преобразование координат ---
    alphabet2 = alphabet1  # Тот же алфавит на 29 букв
    l2c2, c2l2 = generate_polybius_square(alphabet2, rows1, cols1)

    cols_list = []
    rows_list = []
    for char in message:
        if char in l2c2:
            r, c = l2c2[char]
            # В примере координаты (столбец, строка), следуем ему
            cols_list.append(str(c))
            rows_list.append(str(r))

    # Считываем "по строкам": сначала все столбцы, потом все строки
    coord_stream = "".join(cols_list) + "".join(rows_list)
    coord_pairs = [coord_stream[i:i + 2] for i in range(0, len(coord_stream), 2)]

    encrypted2 = []
    for pair in coord_pairs:
        # Координаты в таблице (строка, столбец)
        r, c = int(pair[0]), int(pair[1])
        encrypted2.append(c2l2.get((c, r), '?'))  # Переворачиваем пару для поиска
    print(f"2. Метод 'преобразование координат': {''.join(encrypted2)}")

    # --- Метод 3: Таблица Полибия и шифр Цезаря ---
    alphabet3 = ALPHABET_25.replace('о', 'а').replace('ё', 'е').replace('э', 'е').replace('з', 'ж').replace('й',
                                                                                                            'и').replace(
        'ы', 'и').replace('щ', 'ш').replace('ь', 'ъ')
    l2c3, c2l3 = generate_polybius_square(alphabet3, 5, 5)

    coord_stream3 = []
    for char in message:
        if char in l2c3:
            r, c = l2c3[char]
            coord_stream3.append(str(c) + str(r))  # столбец, строка

    coord_str = "".join(coord_stream3)
    # Цезарь для цифр со сдвигом 3 влево
    shift = -3
    shifted_coord_str = coord_str[abs(shift):] + coord_str[:abs(shift)]

    shifted_pairs = [shifted_coord_str[i:i + 2] for i in range(0, len(shifted_coord_str), 2)]
    encrypted3 = []
    for pair in shifted_pairs:
        c, r = int(pair[0]), int(pair[1])
        encrypted3.append(c2l3.get((r, c), '?'))
    print(f"3. Метод 'Полибий + Цезарь': {''.join(encrypted3)}")

    # --- Метод 4: Таблица Полибия и шифр Цезаря с ключом ---
    keyword4 = "цифирь"
    alphabet4 = ALPHABET_30.replace('ё', '').replace('й', '').replace('ъ', 'ь')
    key_sequence = "".join(dict.fromkeys(keyword4 + alphabet4))
    l2c4, c2l4 = generate_polybius_square(key_sequence, 5, 6)

    coord_stream4 = []
    for char in message:
        if char in l2c4:
            r, c = l2c4[char]
            coord_stream4.append(str(c) + str(r))

    coord_str4 = "".join(coord_stream4)
    shifted_coord_str4 = coord_str4[abs(shift):] + coord_str4[:abs(shift)]

    shifted_pairs4 = [shifted_coord_str4[i:i + 2] for i in range(0, len(shifted_coord_str4), 2)]
    encrypted4 = []
    for pair in shifted_pairs4:
        c, r = int(pair[0]), int(pair[1])
        encrypted4.append(c2l4.get((r, c), '?'))
    print(f"4. Метод 'Полибий + Цезарь с ключом': {''.join(encrypted4)}")
    print("-" * 30 + "\n")


# --- ГЛАВНЫЙ БЛОК ДЛЯ ЗАПУСКА ---

if __name__ == "__main__":
    LAST_NAME = "Ушаков"

    # 2. Ваше Имя
    FIRST_NAME = "Александр"

    # 3. Полное Отчество (используется для составления общей строки)
    PATRONYMIC = "Алексеевич"

    # 4. ИМЯ вашего отца (используется как ключ в Задании 3)
    FATHER_NAME = "Алексей"

    # Собираем строку "фамилияимяотчество" из трех частей
    FULL_NAME = LAST_NAME + FIRST_NAME + PATRONYMIC

    # Запуск всех заданий
    task_1(FULL_NAME)
    task_2(FULL_NAME)
    task_3(FULL_NAME, FIRST_NAME, FATHER_NAME)
    task_4(FULL_NAME)