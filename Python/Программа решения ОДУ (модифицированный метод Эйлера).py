import numpy as np


# Определяем правую часть дифф уравнения
def f(x, y):
    return 0.158 * (x ** 2 + np.sin(0.8 * x)) + 1.164 * y


# модифицированный Эйлер
def improved_euler(f, x0, y0, x_end, h, decimals=4):
    n = int((x_end - x0) / h) + 1
    x = np.linspace(x0, x_end, n)
    y = np.zeros(n)
    y[0] = y0

    for i in range(n - 1):
        # Первый прогноз (Эйлер)
        y_pred = y[i] + h * f(x[i], y[i])

        # усреднение
        y[i + 1] = y[i] + h * (f(x[i], y[i]) + f(x[i + 1], y_pred)) / 2

        # 4 знаков после запятой
        y[i + 1] = round(y[i + 1], decimals)

    return x, y



x0 = 0.2
y0 = 0.25
x_end = 1.2
h = 0.1


x, y = improved_euler(f, x0, y0, x_end, h)


print("Результаты решения дифференциального уравнения:")
print("----------------------------------------")
print("  x     |    y(x)   ")
print("--------|-----------")
for xi, yi in zip(x, y):
    print(f" {xi:.1f}    |  {yi:.4f}")

# Дополнительная проверка
print("\nЗначение y(1.2) =", y[-1])