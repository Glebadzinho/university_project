import numpy as np



def f(x):
    return (1 + 0.7 * x ** 2) / (1.5 + np.sqrt(2 * x ** 2 + 0.3))


# Метод 3/8
def three_eights(f, a, b, n):
    if n % 3 != 0:
        n = n + (3 - n % 3)  # n чтобы было кратно 3

    h = (b - a) / n
    integral = f(a) + f(b)

    for i in range(1, n):
        if i % 3 == 0:
            integral += 2 * f(a + i * h)
        else:
            integral += 3 * f(a + i * h)

    return 3 * h * integral / 8


# Пределы интегрирования
a, b = 0.8, 2.96

# Первый расчет
n1 = 9
I1 = three_eights(f, a, b, n1)

# Второй расчет
n2 = 12
I2 = three_eights(f, a, b, n2)

# Оценка погрешности
error = abs(I2 - I1) / 15  # Для метода 3/8 порядок точности 4

# Вывод результатов
print(f"Значение интеграла при n={n1}: {I1:.6f}")
print(f"Значение интеграла при n={n2}: {I2:.6f}")
print(f"Оценка погрешности: {error:.6f}")
print(f"Уточненное значение: {I2 + (I2 - I1) / 15:.6f}")

# Проверка с помощью scipy
from scipy.integrate import quad

I_exact, _ = quad(f, a, b)
print(f"\nТочное значение (scipy.integrate.quad): {I_exact:.6f}")