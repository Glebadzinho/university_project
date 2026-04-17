from itertools import permutations
import tkinter as tk


def is_valid(grid):
    for col in range(4):
        column = [grid[row][col] for row in range(4)]
        if len(set(column)) != 4:
            return False
    return True


def generate_grids():
    letters = ['a', 'b', 'c', 'd']
    solutions = []
    for row1 in permutations(letters):
        for row2 in permutations(letters):
            for row3 in permutations(letters):
                for row4 in permutations(letters):
                    grid = [row1, row2, row3, row4]
                    if is_valid(grid):
                        solutions.append(grid)
    return solutions


def show_solutions():
    solutions = generate_grids()
    result_window = tk.Toplevel(root)
    result_window.title("Решения")

    text = tk.Text(result_window, width=30, height=20)
    text.pack()

    text.insert(tk.END, f"Всего решений: {len(solutions)}\n\n")

    for i, sol in enumerate(solutions[:5]):  # Показываем первые 5 решений
        text.insert(tk.END, f"Решение {i + 1}:\n")
        for row in sol:
            text.insert(tk.END, ' '.join(row) + '\n')
        text.insert(tk.END, '\n')


# Создаем главное окно
root = tk.Tk()
root.title("Расстановка 16 букв")

label = tk.Label(root, text="Нажмите кнопку, чтобы найти решения:")
label.pack(pady=10)

button = tk.Button(root, text="Найти решения", command=show_solutions)
button.pack(pady=10)

root.mainloop()