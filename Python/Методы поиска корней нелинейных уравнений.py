import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


def f(x):
    return math.exp(-2*x) - 2*x + 1


def df(x):
    return -2*math.exp(-2*x) - 2


def dicot(a, b, eps):
    if f(a) * f(b) >= 0:
        print(f"Нет изменения знака на интервале [{a},{b}]")
        return None, 0
    inter = 0
    while (b - a)/2 > eps:
        c = (a + b) / 2
        if abs(f(c)) < eps:
            return c, inter
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        inter += 1
    return (a + b) / 2, inter


def hord(a, b, eps, max_iter=100):
    if f(a) * f(b) >= 0:
        print(f"Нет изменения знака на интервале [{a},{b}]")
        return None, 0
    inter = 0
    x_prev = a
    for _ in range(max_iter):
        denominator = f(b) - f(a)
        if abs(denominator) < 1e-12:
            print("Ошибка: знаменатель близок к нулю в методе хорд")
            return None, inter
        x = a - f(a) * (b - a) / denominator
        if abs(f(x)) < eps or abs(x - x_prev) < eps:
            return x, inter
        elif f(x) * f(a) < 0:
            b = x
        else:
            a = x
        x_prev = x
        inter += 1
    return None, inter


def newton(x0, eps, max_iter=100):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-12:
            print("Производная близка к нулю в методе Ньютона")
            return None, i
        x_next = x - fx / dfx
        if abs(x_next - x) < eps or abs(f(x_next)) < eps:
            return x_next, i
        x = x_next
    return None, max_iter


def simple_inter(x0, eps, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_next = (math.exp(-2*x) + 1) / 2
        if abs(x_next - x) < eps:
            return x_next, i
        x = x_next
    return None, max_iter


try:
    eps_inp = input('Введите погрешность (например 1e-6): ')
    eps = float(eps_inp)
    a = float(input('Введите левую границу: '))
    b = float(input('Введите правую границу: '))
    x0 = float(input('Введите начальное приближение к корню: '))

    # График
    x_gr = np.linspace(a - 1, b + 1, 100)
    y_gr = [f(x) for x in x_gr]
    plt.plot(x_gr, y_gr)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('График функции')
    plt.grid(True)
    plt.show()

    # Таблица значений
    x_gr2 = np.linspace(a, b, 20)
    y_gr2 = [f(x) for x in x_gr2]
    table_data = [[x, f"{y:.5f}"] for x, y in zip(x_gr2, y_gr2)]

    plt.figure('Таблица')
    plt.title('Таблица значений функции f(x)', fontsize=12)
    plt.table(cellText=table_data, loc='center',
              colLabels=['x', 'f(x)'],
              colColours=["palegreen"]*2,
              cellLoc='center',
              bbox=[0.15, 0, 0.7, 0.9])
    plt.axis('off')
    plt.show()

    # Вычисление корней
    dicot_kor, dicot_iter = dicot(a, b, eps)
    hord_kor, hord_iter = hord(a, b, eps)
    newton_kor, newton_iter = newton(x0, eps)
    simple_inter_kor, simple_inter_iter = simple_inter(x0, eps)

    # Подготовка данных для записи
    data = [
        ['Метод вычисления', 'Кол-во итераций', 'Корень'],
        ['Дихотомии', dicot_iter, f"{dicot_kor:.8f}" if dicot_kor is not None else "Не найден"],
        ['Хорд', hord_iter, f"{hord_kor:.8f}" if hord_kor is not None else "Не найден"],
        ['Метод Ньютона', newton_iter, f"{newton_kor:.8f}" if newton_kor is not None else "Не найден"],
        ['Итераций', simple_inter_iter, f"{simple_inter_kor:.8f}" if simple_inter_kor is not None else "Не найден"]
    ]

    # Запись в файл
    with open("result.txt", 'w', encoding='utf-8') as file:
        file.write(tabulate(data[1:], headers=data[0], tablefmt='grid'))

except ValueError as e:
    print(f"Ошибка ввода данных: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")