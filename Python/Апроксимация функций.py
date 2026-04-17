import tkinter as tk
from tkinter import Label, Entry, Button, LabelFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import symbols, expand

def f(x):
    return x ** 3 * np.exp(2 * x)

def mt(a, b, c):
    lead = 1

    for i in range(len(a) * 2 - 2):
        for start in range(len(a)):
            for end in range(len(a)):
                if (start + end) == lead:
                    a[start][end] = b[i]
        lead += 1

    for i in range(len(a)):
        a[i].append(c[i])

    return a

def to_row_echelon_form(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    lead = 0

    for r in range(rows):
        if lead >= cols:
            break

        i = r
        while i < rows and matrix[i][lead] == 0:
            i += 1
        if i == rows:
            lead += 1
            continue

        if i != r:
            matrix[r], matrix[i] = matrix[i], matrix[r]

        if matrix[r][lead] != 0:
            pivot = matrix[r][lead]
            for j in range(cols):
                matrix[r][j] /= pivot

        for i in range(rows):
            if i != r:
                factor = matrix[i][lead]
                for j in range(cols):
                    matrix[i][j] -= factor * matrix[r][j]

        lead += 1

    return matrix

def MNK(a, b, n):
    h = (b - a) / n

    c1 = [0] * 11
    c2 = [0] * 6
    x = a
    c2[0] = f(x)

    while x <= b + 1e-10:
        for i in range(1, len(c1) + 1):
            c1[i - 1] += x ** i

        for i in range(len(c2)):
            c2[i] += float(f(x)) * x ** i

        x += h

    a_2 = [[n+1 for _ in range(3)] for _ in range(3)]
    res_a_2 = to_row_echelon_form(mt(a_2, c1, c2))

    a_3 = [[n+1 for _ in range(4)] for _ in range(4)]
    res_a_3 = to_row_echelon_form(mt(a_3, c1, c2))

    a_4 = [[n+1 for _ in range(5)] for _ in range(5)]
    res_a_4 = to_row_echelon_form(mt(a_4, c1, c2))

    a_5 = [[n+1 for _ in range(6)] for _ in range(6)]
    res_a_5 = to_row_echelon_form(mt(a_5, c1, c2))

    return res_a_2, res_a_3, res_a_4, res_a_5

# метод Лагранжа
def lagrange(a,b,n):
    delta_x = abs(a-b)/n
    x_sym = symbols('x')

    x_point = [(a + delta_x * (j+0.5)) for j in range(n)]
    y_values = [f(x_point[i]) for i in range(len(x_point))]

    def basis_lagrange(j, x_point, y_values):
        n = len(x_point)
        x = symbols('x')
        basis = 1

        for k in range(n):
            if j != k:
                basis *= (x - x_point[k])/(x_point[j] - x_point[k])

        return basis

    def lagrange_polynomial(x_points, y_values, x_sym):
        n = len(x_points)
        polynomial = 0
        for j in range(n):
            polynomial += y_values[j] * basis_lagrange(j, x_points, x_sym)
        return expand(polynomial)

    P = lagrange_polynomial(x_point, y_values, x_sym)
    x_vals = np.linspace(a, b, 500)
    y_vals = f(x_vals)
    y_interp = [P.subs(x_sym, x_val) for x_val in x_vals]

    return P, y_vals, y_interp

def itog(x, a2, a3, a4, a5):
    a2_res = 0
    a3_res = 0
    a4_res = 0
    a5_res = 0

    for i in range(len(a2)):
        a2_res += a2[i][-1] * x ** i

    for i in range(len(a3)):
        a3_res += a3[i][-1] * x ** i

    for i in range(len(a4)):
        a4_res += a4[i][-1] * x ** i

    for i in range(len(a5)):
        a5_res += a5[i][-1] * x ** i

    return a2_res, a3_res, a4_res, a5_res


def plot_graph_MNK():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        n = int(entry_n.get())
        if a >= b:
            raise ValueError("Начало интервала должно быть меньше конца интервала.")
        if n <= 0:
            raise ValueError("Количество точек должно быть положительным.")

        # Очистка предыдущего графика
        for widget in plt_frame_MNK.winfo_children():
            widget.destroy()

        # Создание нового графика
        fig, ax = plt.subplots(figsize=(8, 5))  # Размер графика
        canvas = FigureCanvasTkAgg(fig, master=plt_frame_MNK)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both")

        # Генерация значений x и y
        x_values = np.linspace(a, b, 500)
        y_values = f(x_values)

        # Очистка осей перед построением нового графика
        ax.clear()
        ax.plot(x_values, y_values, label='f(x) = x^3 * e^(2x)', color='blue')

        # Вычисление полиномов методом МНК
        a2, a3, a4, a5 = MNK(a, b, n)
        x_poly = np.linspace(a, b, 500)
        y2, y3, y4, y5 = zip(*[itog(x, a2, a3, a4, a5) for x in x_poly])

        ax.plot(x_poly, y2, label='Полином 2-го порядка', linestyle='--')
        ax.plot(x_poly, y3, label='Полином 3-го порядка', linestyle='-.')
        ax.plot(x_poly, y4, label='Полином 4-го порядка', linestyle=':')
        ax.plot(x_poly, y5, label='Полином 5-го порядка', linestyle='-.')

        ax.set_title('График функции и полиномов')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True)

        # Обновление интерфейса
        root.update()
    except ValueError as e:
        error_label.config(text=str(e))


def plot_lagrange_graph():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        n = int(entry_n.get())
        if a >= b:
            raise ValueError("Начало интервала должно быть меньше конца интервала.")
        if n <= 0:
            raise ValueError("Количество точек должно быть положительным.")

        # Очистка предыдущего графика
        for widget in plt_frame_MNK.winfo_children():
            widget.destroy()

        # Создание нового графика
        fig, ax = plt.subplots(figsize=(8, 5))  # Размер графика
        canvas = FigureCanvasTkAgg(fig, master=plt_frame_MNK)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both")

        # Вычисление полинома Лагранжа
        P, y_vals, y_interp = lagrange(a, b, n)
        x_values = np.linspace(a, b, 500)

        # Очистка осей перед построением нового графика
        ax.clear()
        ax.plot(x_values, y_vals, label='f(x) = x^3 * e^(2x)', color='blue')
        ax.plot(x_values, y_interp, label='Интерполяция Лагранжа', linestyle='--', color='red')

        ax.set_title('График истинной функции и интерполяции Лагранжа')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True)

        # Обновление интерфейса
        root.update()
    except ValueError as e:
        error_label.config(text=str(e))

# Создание главного окна
root = tk.Tk()
root.title('График функции')
root.geometry('1400x900')

# Окно для ввода данных
input_frame = LabelFrame(root, text="Ввод данных", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=10)

# Метки и поля ввода
Label(input_frame, text='Введите интервал и число n').grid(row=0, column=0, sticky='w', columnspan=2)

Label(input_frame, text='a = ').grid(row=1, column=0, sticky='e', padx=(0, 5))
entry_a = Entry(input_frame)
entry_a.grid(row=1, column=1, sticky='w')

Label(input_frame, text='b = ').grid(row=2, column=0, sticky='e', padx=(0, 5))
entry_b = Entry(input_frame)
entry_b.grid(row=2, column=1, sticky='w')

Label(input_frame, text='n = ').grid(row=3, column=0, sticky='e', padx=(0, 5))
entry_n = Entry(input_frame)
entry_n.grid(row=3, column=1, sticky='w')

Button(input_frame, text="График для МНК", command=plot_graph_MNK).grid(row=4, column=0, columnspan=2, pady=5)
Button(input_frame, text="График для Лагранжа", command=plot_lagrange_graph).grid(row=5, column=0, columnspan=2, pady=5)

error_label = Label(input_frame, text="", fg="red")
error_label.grid(row=5, column=0, columnspan=2)


'''ТАБЛИЧНАЯ ФУНКЦИЯ МНК'''
xx = np.linspace(0, 1, 8)
y = f(xx)
stt = 1

Label(input_frame, text='Таблично заданая функция', font=('Arial', 14, 'bold')).grid(row=0, column=2, sticky='w', padx=10)

for i in range(len(y)):
    Label(input_frame, text=f'Значение в точке {xx[i]:.3f} - {y[i]:.3f}', pady=2).grid(row=stt, column=2, sticky='w', padx=10)
    stt += 1

'''ВЫВОД ПОГРЕШНОСТЕЙ МНК'''
def abs_pog_MNK():
    a, b, n = int(entry_a.get()), int(entry_b.get()), int(entry_n.get())
    x = np.linspace(a, b, n)

    # Получение коэффициентов аппроксимации
    res_a_2, res_a_3, res_a_4, res_a_5 = MNK(a, b, n-1)

    Label(input_frame, text=f'Абс пог 2-5 степений метода МНК', font=('Arial', 14, 'bold')).grid(row=0, column=3, columnspan=4, padx=20)
    Label(input_frame, text=f'Относительная МНК', font=('Arial', 14, 'bold')).grid(row=0, column=7, columnspan=4, padx=20)

    # Вывод абсолютных погрешностей
    stt = 1
    for i in range(n):
        # абсолютная
        y = f(x[i])
        a2_res,a3_res,a4_res,a5_res = itog(x[i], res_a_2, res_a_3, res_a_4, res_a_5)
        Label(input_frame, text=f'{abs(a2_res - y):.4f}').grid(row=stt,column=3)
        Label(input_frame, text=f'{abs(a3_res - y):.4f}').grid(row=stt, column=4)
        Label(input_frame, text=f'{abs(a4_res - y):.4f}').grid(row=stt, column=5)
        Label(input_frame, text=f'{abs(a5_res - y):.4f}').grid(row=stt, column=6)

        # относительная
        Label(input_frame, text=f'{abs(a2_res - y) * 100:.4f}').grid(row=stt, column=7)
        Label(input_frame, text=f'{abs(a3_res - y) * 100:.4f}').grid(row=stt, column=8)
        Label(input_frame, text=f'{abs(a4_res - y) * 100:.4f}').grid(row=stt, column=9)
        Label(input_frame, text=f'{abs(a5_res - y) * 100:.4f}').grid(row=stt, column=10)
        stt += 1

"""вывод погрешностей МНК"""
btn_MNK = Button(input_frame, text='Вывод погрешностей МНК', command=abs_pog_MNK).grid(row=6, column=0, columnspan=2, pady=5)

'''АБС ПОГРЕШНОСТЬ ЛАГРАНЖА ЁХ'''
def ab_pog_LOGR():
    Label(input_frame, text=f'Абс и отн пог Логранжа', font=('Arial', 14, 'bold')).grid(row=0, column=11, padx=20,columnspan=2)
    a, b, n = int(entry_a.get()), int(entry_b.get()), int(entry_n.get())
    P, _, _ = lagrange(a,b,n)
    x_sym = symbols('x')
    x = np.linspace(a,b,n)
    y1= [P.subs(x_sym, x_val) for x_val in x]
    y2 = f(x)
    stt = 1

    for i in range(len(x)):
        Label(input_frame, text=f'{abs(y1[i]-y2[i]):.8f}, ').grid(row=stt, column=11,padx=2, sticky='e')
        Label(input_frame, text=f'{abs(((y1[i] - y2[i]))*100):.8f}').grid(row=stt, column=12, padx=2, sticky='w')
        stt+=1

"""вывод погрешностей Лагранжа"""
btn_LGJ = Button(input_frame, text='Вывод погрешностей Логранжа', command=ab_pog_LOGR).grid(row=7, column=0, columnspan=2, pady=5)

"""Окна для выводов графиков"""
plt_frame_MNK = LabelFrame(root, text="Построение графиков",width=500, height=500)
plt_frame_MNK.pack(padx=10, pady=10, fill="both", expand=True)


res_a_2, res_a_3, res_a_4, res_a_5 = MNK(0,1,5)
aa_1 = ''
aa_2 = ''
aa_3 = ''
aa_4 = ''

for i in range(len(res_a_2)):
    aa_1 += f'{res_a_2[i][-1]}, '

for i in range(len(res_a_3)):
    aa_2 += f'{res_a_3[i][-1]}, '

for i in range(len(res_a_4)):
    aa_3 += f'{res_a_4[i][-1]}, '

for i in range(len(res_a_5)):
    aa_4 += f'{res_a_5[i][-1]}, '

print(aa_1)
print(aa_2)
print(aa_3)
print(aa_4)

root.mainloop()