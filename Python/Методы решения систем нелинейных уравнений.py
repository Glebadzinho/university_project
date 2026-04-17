import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate



def f1(x, y):
    return np.sin(x - y) - x * y + 1


def f2(x, y):
    return x ** 2 - y ** 2 - 0.75


def yakobi(x0, y0, eps, max_iter=100):
    x, y = x0, y0
    for iter in range(max_iter):
        x_new = (np.sin(x - y) + 1) / y if y != 0 else x
        y_new = np.sqrt(x ** 2 - 0.75) if x ** 2 >= 0.75 else y

        if max(abs(x_new - x), abs(y_new - y)) < eps:
            return x_new, y_new, iter + 1

        x, y = x_new, y_new
    return x, y, max_iter


def gauss(x0, y0, eps, max_iter=100):
    x, y = x0, y0
    for iter in range(max_iter):
        x_new = (np.sin(x - y) + 1) / y if y != 0 else x
        y_new = np.sqrt(x_new ** 2 - 0.75) if x_new ** 2 >= 0.75 else y

        if max(abs(x_new - x), abs(y_new - y)) < eps:
            return x_new, y_new, iter + 1

        x, y = x_new, y_new
    return x, y, max_iter


def newton(x0, y0, eps, max_iter=100):
    x, y = x0, y0
    for iter in range(max_iter):
        try:
            J = np.array([
                [np.cos(x - y) - y, -np.cos(x - y) - x],
                [2 * x, -2 * y]
            ])
            F = np.array([-f1(x, y), -f2(x, y)])

            delta = np.linalg.solve(J, F)
            x += delta[0]
            y += delta[1]

            if np.linalg.norm(delta) < eps:
                return x, y, iter + 1

        except np.linalg.LinAlgError:
            print("Матрица Якоби вырождена")
            return x, y, iter + 1

    return x, y, max_iter


# Ввод данных
try:
    x0 = float(input('Введите начальное x0: '))
    y0 = float(input('Введите начальное y0: '))
    eps = float(input('Введите точность: '))
except ValueError:
    print("Ошибка ввода! Нужно вводить числа.")
    exit()

#График
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
F1 = np.sin(X - Y) - X*Y + 1
F2 = X**2 - Y**2 - 0.75
plt.contour(X, Y, F1, levels=[0], colors='r')
plt.contour(X, Y, F2, levels=[0], colors='b')
plt.xlabel('x'); plt.ylabel('y'); plt.grid()
plt.show()


#Таблица в файл
x_y,y_y,i_y=yakobi(x0, y0, eps)
x_g,y_g,i_g=gauss(x0, y0, eps)
x_n,y_n,i_n=newton(x0, y0, eps)
data = [['Метод вычисления','Кол-во итераций','X','Y'],['Якоби',str(i_y),str(x_y),str(y_y)],['Гаусс',str(i_g),str(x_g),str(y_g)],['Ньютона',str(i_n),str(x_n),str(y_n)]]
with open("result.txt",'w',encoding='utf-8') as file:
    file.write(tabulate(data[1:],headers=data[0],tablefmt='grid'))


#Аналитический вид системы уравнений вывести на форму
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
equation_text = "Система уравнений:\n\n" + \
                "1) sin(x - y) - x·y = -1\n" + \
                "2) x² - y² = 0.75"

plt.text(0.5, 0.5, equation_text, fontsize=14,
         ha='center', va='center', fontfamily='serif')
plt.title('Аналитический вид системы уравнений', pad=20)
plt.tight_layout()
plt.show()
