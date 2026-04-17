import math


def f(x):
    return math.log(x + math.sqrt(x**2 + 8))


def left_rect(a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(n):
        x = a + i * h
        total += f(x) * h
    return total


def mid_rect(a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(n):
        x = a + (i + 0.5) * h
        total += f(x) * h
    return total


def right_rect(a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(1, n+1):
        x = a + i * h
        total += f(x) * h
    return total


def trapezoid(a, b, n):
    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        x = a + i * h
        total += f(x)
    return total * h


def simpson(a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            total += 2 * f(x)
        else:
            total += 4 * f(x)
    return total * h / 3


def compute(method, a, b, eps=1e-3):
    n = 4
    prev = method(a, b, n)
    while True:
        n *= 2
        curr = method(a, b, n)
        if abs(curr - prev) < eps:
            return curr, n
        prev = curr


a, b = 0, 1
methods = {
    "Левых прямоугольников": left_rect,
    "Средних прямоугольников": mid_rect,
    "Правых прямоугольников": right_rect,
    "Трапеций": trapezoid,
    "Симпсона": simpson
}

print("Приближенные значения интеграла:")
for name, method in methods.items():
    result, n = compute(method, a, b)
    print(f"{name}: {result:.6f} (n={n})")

exact = -3 + 2*math.sqrt(2) + math.log(4)
print(f"\nТочное значение: {exact:.6f}")