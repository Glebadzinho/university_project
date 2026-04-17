import numpy as np
import tkinter as tk
from tkinter import messagebox
import os

win = tk.Tk()
win.title('Бардин, лабораторная работа №3')
win.geometry('800x600')
win.config(bg='light pink')


lbl1 = tk.Label(win, text='', font=('arial', 13), bg='light pink')
lbl1.place(x=350, y=200)
lbl2 = tk.Label(win, text='', font=('arial', 13), bg='light pink')
lbl2.place(x=350, y=400)


A = np.array([[4.1, 5.2, -5.8],
              [3.8, -3.1, 4.0],
              [7.8, 5.3, -6.3]], dtype=float)

B = np.array([7.0, 5.3, 5.8], dtype=float)

AB = np.hstack((A, B.reshape(-1, 1)))


def is_matrix_valid(A, B):
    """Проверка корректности матрицы и вектора"""
    if A.shape[0] != A.shape[1]:
        return False, "Матрица должна быть квадратной"
    if A.shape[0] != B.shape[0]:
        return False, "Размерность вектора не соответствует матрице"
    if np.linalg.det(A) == 0:
        return False, "Определитель матрицы равен нулю (система вырождена)"
    return True, ""


def calculate_residual(A, x, B):
    """Вычисление невязки решения"""
    return np.linalg.norm(np.dot(A, x) - B)


def gauss():
    """Метод Гаусса с выбором ведущего элемента и проверками"""
    try:
        # Проверка корректности матрицы
        valid, msg = is_matrix_valid(A, B)
        if not valid:
            lbl1.config(text=f"Ошибка: {msg}")
            return None, 0

        AB_copy = AB.copy()
        n = len(AB_copy)
        cnt1 = 0
        x = np.zeros(n)

        # Прямой ход с выбором ведущего элемента
        for i in range(n):
            # Выбор ведущего элемента
            max_row = np.argmax(np.abs(AB_copy[i:n, i])) + i
            AB_copy[[i, max_row]] = AB_copy[[max_row, i]]

            if np.abs(AB_copy[i, i]) < 1e-10:
                lbl1.config(text="Ошибка: система вырождена")
                return None, 0

            for j in range(i + 1, n):
                factor = AB_copy[j, i] / AB_copy[i, i]
                AB_copy[j, i:] -= factor * AB_copy[i, i:]
                cnt1 += 1


        for i in range(n - 1, -1, -1):
            x[i] = (AB_copy[i, -1] - np.dot(AB_copy[i, i + 1:n], x[i + 1:n])) / AB_copy[i, i]

        # Проверка решения
        residual = calculate_residual(A, x, B)
        if residual > 1e-6:
            messagebox.showwarning("Предупреждение",
                                   f"Большая невязка решения: {residual:.2e}")

        result_text = '\n'.join([f'x{i + 1} = {val:.8f}' for i, val in enumerate(x)])
        lbl1.config(text=result_text)
        save_results(x, cnt1, 'Гаусса', residual)
        return x, cnt1

    except Exception as e:
        lbl1.config(text=f"Ошибка: {str(e)}")
        return None, 0


def jordan():
    """Метод Гаусса-Жордана с проверками"""
    try:
        # Проверка корректности матрицы
        valid, msg = is_matrix_valid(A, B)
        if not valid:
            lbl2.config(text=f"Ошибка: {msg}")
            return None, 0

        AB_copy = AB.copy()
        n = len(AB_copy)
        cnt2 = 0

        for i in range(n):
            # Выбор ведущего элемента
            max_row = np.argmax(np.abs(AB_copy[i:n, i])) + i
            AB_copy[[i, max_row]] = AB_copy[[max_row, i]]

            if np.abs(AB_copy[i, i]) < 1e-10:
                lbl2.config(text="Ошибка: система вырождена")
                return None, 0

            # Нормализация текущей строки
            pivot = AB_copy[i, i]
            AB_copy[i] = AB_copy[i] / pivot
            cnt2 += 1

            # Исключение переменной из других уравнений
            for j in range(n):
                if i != j:
                    factor = AB_copy[j, i]
                    AB_copy[j] -= factor * AB_copy[i]
                    cnt2 += 1

        x = AB_copy[:, -1]

        # Проверка решения
        residual = calculate_residual(A, x, B)
        if residual > 1e-6:
            messagebox.showwarning("Предупреждение",
                                   f"Большая невязка решения: {residual:.2e}")

        res_text = '\n'.join([f'x{i + 1} = {val:.8f}' for i, val in enumerate(x)])
        lbl2.config(text=res_text)
        save_results(x, cnt2, 'Гаусса-Жордана', residual)
        return x, cnt2

    except Exception as e:
        lbl2.config(text=f"Ошибка: {str(e)}")
        return None, 0


def save_results(x, iterations, method, residual=None):
    """Сохранение результатов с дополнительной информацией"""
    try:
        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(f'Метод: {method}\n')
            for i in range(len(x)):
                f.write(f'x{i + 1} = {x[i]:.10f}\n')

            if iterations is not None:
                f.write(f'Количество операций: {iterations}\n')

            if residual is not None:
                f.write(f'Невязка решения: {residual:.4e}\n')

            f.write('\n')
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить результаты: {e}")


def on_closing():
    """Действия при закрытии окна"""
    try:
        if os.path.exists('results.txt'):
            os.remove('results.txt')
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось удалить файл результатов: {e}")
    win.destroy()


# Создание кнопок
btn1 = tk.Button(win, text='Решить систему методом Гаусса',
                 command=gauss, bg='violet', font=('arial', 12))
btn1.pack(pady=40, padx=20)

btn2 = tk.Button(win, text='Решить систему методом Гаусса-Жордана',
                 command=jordan, bg='violet', font=('arial', 12))
btn2.pack(pady=40, padx=20)

win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()