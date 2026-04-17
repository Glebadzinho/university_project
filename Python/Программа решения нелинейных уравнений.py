import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x ** 3 - 3 * x ** 2 + 3


def df(x):
    return 3 * x ** 2 - 6 * x


def d2f(x):
    return 6 * x - 6


# График для отделения корней
x = np.linspace(-2, 4, 400)
plt.plot(x, f(x))
plt.axhline(0, color='r', linestyle='--')
plt.grid()
plt.title('График функции f(x) = x³ - 3x² + 3')
plt.show()


# Улучшенный комбинированный метод
def combined_method(f, df, a, b, eps=0.001, max_iter=100):
    if f(a) * f(b) > 0:
        return None

    for _ in range(max_iter):
        try:
            # Метод Ньютона
            x0 = (a + b) / 2  # Берем середину интервала как начальное приближение
            if abs(df(x0)) > eps:  # Проверяем, что производная не нулевая
                x_newton = x0 - f(x0) / df(x0)
            else:
                x_newton = x0

            # Метод хорд
            x_chord = (a * f(b) - b * f(a)) / (f(b) - f(a))

            # Новое приближение - средневзвешенное
            x_new = (x_newton + x_chord) / 2

            # Проверка сходимости
            if abs(f(x_new)) < eps:
                return x_new

            # Обновление интервала
            if f(a) * f(x_new) < 0:
                b = x_new
            else:
                a = x_new

        except ZeroDivisionError:
            # Если возникает деление на ноль, используем метод бисекции
            x_new = (a + b) / 2
            if abs(f(x_new)) < eps:
                return x_new
            if f(a) * f(x_new) < 0:
                b = x_new
            else:
                a = x_new

    return (a + b) / 2


# Интервалы, определенные по графику
intervals = [(-1, 0), (1, 2), (2, 3.5)]
roots = []

for a, b in intervals:
    root = combined_method(f, df, a, b)
    if root is not None:
        roots.append(root)

print("Найденные корни с точностью 0.001:")
for i, root in enumerate(roots, 1):
    print(f"x{i} = {root:.3f}")

# Проверка
print("\nПроверка подстановкой:")
for root in roots:
    print(f"f({root:.3f}) = {f(root):.6f}")