import math


# --- Общие функции ---

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов Безу."""
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def mod_inverse(a, m):
    """Нахождение модульного обратного."""
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise Exception('модульное обратное не существует')
    return x % m


# --- Задание 1.1: Аддитивная группа кольца Z_16 ---
m1 = 16
print("--- Задание 1.1 (m = 16) ---")
for x in range(m1):
    # Нахождение порядка элемента
    order = 1
    current = x
    while current != 0:
        current = (current + x) % m1
        order += 1
    if x == 0:
        order = 1

    # Нахождение противоположного элемента
    opposite = (m1 - x) % m1

    # Вычисление x^2 и x^3 (в контексте кольца, это умножение)
    x_squared = (x * x) % m1
    x_cubed = (x * x * x) % m1

    print(f"Элемент x = {x}:")
    print(f"  Порядок: {order}")
    print(f"  Противоположный элемент: {opposite}")
    print(f"  x^2: {x_squared}")
    print(f"  x^3: {x_cubed}")
print("-" * 20)

# --- Задание 2.1: Обратимые элементы и делители нуля в Z_12 ---
m2 = 12
print("\n--- Задание 2.1 (m = 12) ---")
invertible_elements = []
zero_divisors = []

for x in range(m2):
    # Проверка на обратимость
    if math.gcd(x, m2) == 1:
        inv = mod_inverse(x, m2)
        invertible_elements.append((x, inv))
    # Проверка на делители нуля
    elif x != 0:
        for y in range(1, m2):
            if (x * y) % m2 == 0:
                zero_divisors.append(x)
                break

print("Обратимые элементы и их обратные:")
for val, inv in invertible_elements:
    print(f"  {val} (обратный: {inv})")

print("\nДелители нуля:")
print(f"  {sorted(list(set(zero_divisors)))}")
print("-" * 20)

# --- Задание 3.1: Порядки обратимых элементов в Z_22 и проверка на цикличность ---
m3 = 22
print("\n--- Задание 3.1 (m = 22) ---")
U_m = [x for x in range(1, m3) if math.gcd(x, m3) == 1]
phi = len(U_m)
is_cyclic = False

print(f"Мультипликативная группа U_{m3}: {U_m}")
print(f"Число обратимых элементов (φ({m3})): {phi}")

for a in U_m:
    order = 1
    current = a
    while current != 1:
        current = (current * a) % m3
        order += 1
    print(f"  Порядок элемента {a}: {order}")
    if order == phi:
        is_cyclic = True

if is_cyclic:
    print("\nГруппа является циклической.")
else:
    print("\nГруппа не является циклической.")
print("-" * 20)

# --- Задание 4.1: Вычисления в поле Z_7 ---
p4 = 7
print(f"\n--- Задание 4.1 (p = {p4}) ---")
# Выражение: (1 + 5^(-1) * 6)^(-2)
inv_5 = mod_inverse(5, p4)
base = (1 + inv_5 * 6) % p4
inv_base = mod_inverse(base, p4)
result4 = (inv_base * inv_base) % p4
print(f"Результат (1 + 5^(-1) * 6)^(-2) mod {p4} = {result4}")
print("-" * 20)

# --- Задание 5.1: Решение квадратного уравнения в Z_11 ---
p5 = 11
print(f"\n--- Задание 5.1 (p = {p5}) ---")
# Уравнение: x^2 - 5x + 9 = 0  (mod 11) => x^2 + 6x + 9 = 0 (mod 11)
solutions5 = []
for x in range(p5):
    if (x * x + 6 * x + 9) % p5 == 0:
        solutions5.append(x)

if solutions5:
    print(f"Корни уравнения x^2 - 5x + 9 = 0: {solutions5}")
else:
    print("Уравнение не имеет корней.")
print("-" * 20)

# --- Задание 6.1: Решение кубического уравнения в Z_17 ---
p6 = 17
a6 = 6
print(f"\n--- Задание 6.1 (p = {p6}, a = {a6}) ---")
# Уравнение: x^3 + 7x + 14 = 0 (mod 17)
# Проверка, что a=6 является корнем
check = (a6 ** 3 + 7 * a6 + 14) % p6
print(f"Проверка корня a=6: ({a6}^3 + 7*{a6} + 14) mod {p6} = {check}")

# Находим остальные корни
# (x^3 + 7x + 14) / (x-6) = x^2 + 6x + 5
solutions6 = [a6]
for x in range(p6):
    if (x ** 2 + 6 * x + 5) % p6 == 0 and x not in solutions6:
        solutions6.append(x)

print(f"Все корни уравнения: {sorted(solutions6)}")
print("-" * 20)

# --- Задание 7.1: Решение полиномиального уравнения в Z_5 ---
p7 = 5
print(f"\n--- Задание 7.1 (p = {p7}) ---")
# Уравнение: 16x^7 + 11x^6 - 9x^5 - 11x^3 - x - 4 = 0 (mod 5)
# Упрощенное: x^7 + x^6 + x^5 + 4x^3 + 4x + 1 = 0
# С использованием Малой теоремы Ферма (x^5 ≡ x):
# x^3 + x^2 + x + 4x^3 + 4x + 1 = 0
# 5x^3 + x^2 + 5x + 1 = 0 => x^2 + 1 = 0
solutions7 = []
for x in range(p7):
    if (x * x + 1) % p7 == 0:
        solutions7.append(x)

if solutions7:
    print(f"Корни уравнения 16x^7 + ... = 0: {solutions7}")
else:
    print("Уравнение не имеет корней.")
print("-" * 20)

# --- Задание 8.1: Решение системы линейных уравнений в Z_11 методом Крамера ---
p8 = 11
print(f"\n--- Задание 8.1 (в поле Z_{p8}) ---")
# Система:
# x1 + x2       = 1
# 2x1 +    2x3  = 1
# x1 + x2 + 2x3 = 1

# Матрица коэффициентов
A = [[1, 1, 0], [2, 0, 2], [1, 1, 2]]
b = [1, 1, 1]

# Определитель основной матрицы
det_A = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
         A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
         A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])) % p8

if det_A == 0:
    print("Система не имеет единственного решения.")
else:
    inv_det_A = mod_inverse(det_A, p8)

    # Определитель для x1
    A1 = [[b[0], A[0][1], A[0][2]], [b[1], A[1][1], A[1][2]], [b[2], A[2][1], A[2][2]]]
    det_A1 = (A1[0][0] * (A1[1][1] * A1[2][2] - A1[1][2] * A1[2][1]) -
              A1[0][1] * (A1[1][0] * A1[2][2] - A1[1][2] * A1[2][0]) +
              A1[0][2] * (A1[1][0] * A1[2][1] - A1[1][1] * A1[2][0])) % p8
    x1 = (det_A1 * inv_det_A) % p8

    # Определитель для x2
    A2 = [[A[0][0], b[0], A[0][2]], [A[1][0], b[1], A[1][2]], [A[2][0], b[2], A[2][2]]]
    det_A2 = (A2[0][0] * (A2[1][1] * A2[2][2] - A2[1][2] * A2[2][1]) -
              A2[0][1] * (A2[1][0] * A2[2][2] - A2[1][2] * A2[2][0]) +
              A2[0][2] * (A2[1][0] * A2[2][1] - A2[1][1] * A2[2][0])) % p8
    x2 = (det_A2 * inv_det_A) % p8

    # Определитель для x3
    A3 = [[A[0][0], A[0][1], b[0]], [A[1][0], A[1][1], b[1]], [A[2][0], A[2][1], b[2]]]
    det_A3 = (A3[0][0] * (A3[1][1] * A3[2][2] - A3[1][2] * A3[2][1]) -
              A3[0][1] * (A3[1][0] * A3[2][2] - A3[1][2] * A3[2][0]) +
              A3[0][2] * (A3[1][0] * A3[2][1] - A3[1][1] * A3[2][0])) % p8
    x3 = (det_A3 * inv_det_A) % p8

    print(f"Решение системы: x1 = {x1}, x2 = {x2}, x3 = {x3}")
print("-" * 20)