import tkinter as tk
from tkinter import ttk, messagebox


words = [
    ("apple", "pomme", "яблоко"), ("dog", "chien", "собака"),
    ("house", "maison", "дом"), ("book", "livre", "книга"),
    ("water", "eau", "вода"), ("cat", "chat", "кот"),
    ("sun", "soleil", "солнце"), ("moon", "lune", "луна"),
    ("tree", "arbre", "дерево"), ("flower", "fleur", "цветок"),
    ("car", "voiture", "машина"), ("train", "train", "поезд"),
    ("plane", "avion", "самолёт"), ("ship", "bateau", "корабль"),
    ("food", "nourriture", "еда"), ("bread", "pain", "хлеб"),
    ("meat", "viande", "мясо"), ("fish", "poisson", "рыба"),
    ("milk", "lait", "молоко"), ("egg", "œuf", "яйцо"),
    ("hello", "bonjour", "привет"), ("goodbye", "au revoir", "пока"),
    ("thank you", "merci", "спасибо"), ("please", "s'il vous plaît", "пожалуйста"),
    ("friend", "ami", "друг"), ("family", "famille", "семья"),
    ("city", "ville", "город"), ("country", "pays", "страна"),
    ("time", "temps", "время"), ("day", "jour", "день"),
    ("night", "nuit", "ночь"), ("week", "semaine", "неделя"),
    ("year", "an", "год"), ("people", "gens", "люди"),
    ("man", "homme", "мужчина"), ("woman", "femme", "женщина"),
    ("child", "enfant", "ребёнок"), ("school", "école", "школа"),
    ("work", "travail", "работа"), ("money", "argent", "деньги")
]

# Глобальные переменные
current_index = 0
streak = 0
language = "english"


def show_word():
    global current_index
    if current_index < len(words):
        eng, fr, rus = words[current_index]
        word = fr if language == "french" else eng
        word_label.config(text=f"Переведите: {word}")
        progress_label.config(text=f"Слово {current_index + 1}/{len(words)}")
        entry.delete(0, tk.END)
        status_label.config(text="")
        entry.focus()  # Автоматический фокус на поле ввода
    else:
        messagebox.showinfo("Поздравляем!", "Вы изучили все слова!")
        current_index = 0
        show_word()


def check_answer():
    global current_index, streak
    user_answer = entry.get().strip().lower()
    correct_answer = words[current_index][2].lower()

    if user_answer == correct_answer:
        status_label.config(text="✅ Правильно!", foreground="green")
        streak += 1
        streak_label.config(text=f"Серия: {streak}", foreground="green")
        current_index += 1
        root.after(1000, show_word)
    else:
        status_label.config(text=f"❌ Неправильно! Правильно: {correct_answer}", foreground="red")
        streak = 0
        streak_label.config(text=f"Серия: {streak}", foreground="red")


def change_language(new_lang):
    """Меняет язык и сбрасывает прогресс"""
    global language, current_index, streak
    language = new_lang
    current_index = 0
    streak = 0
    streak_label.config(text=f"Серия: {streak}", foreground="green")
    show_word()


# Создание главного окна
root = tk.Tk()
root.title("Vocabulary Trainer Pro")
root.geometry("550x450")
root.resizable(False, False)

# Настройка стилей
style = ttk.Style()
style.configure("TButton", font=("Arial", 11), padding=6)
style.configure("TLabel", background="#f0f8ff", font=("Arial", 11))
style.configure("TFrame", background="#f0f8ff")
style.configure("TEntry", font=("Arial", 12))

# Основной фрейм
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both")

# Заголовок
title_label = ttk.Label(
    main_frame,
    text="Тренажёр слов ",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=10)

# Фрейм для кнопок языка
lang_frame = ttk.Frame(main_frame)
lang_frame.pack(pady=5)

eng_btn = ttk.Button(
    lang_frame,
    text="Английский → Русский",
    command=lambda: change_language("english"),
    style="TButton"
)
eng_btn.pack(side="left", padx=5)

fr_btn = ttk.Button(
    lang_frame,
    text="Французский → Русский",
    command=lambda: change_language("french"),
    style="TButton"
)
fr_btn.pack(side="left")

# Прогресс
progress_label = ttk.Label(main_frame, text="", font=("Arial", 12))
progress_label.pack()

# Слово для перевода
word_label = ttk.Label(
    main_frame,
    text="",
    font=("Arial", 14, "bold"),
    wraplength=400  # Перенос длинных слов
)
word_label.pack(pady=15)

# Поле ввода
entry = ttk.Entry(
    main_frame,
    font=("Arial", 12),
    width=30
)
entry.pack(pady=10)
entry.bind("<Return>", lambda e: check_answer())

# Кнопка проверки
check_btn = ttk.Button(
    main_frame,
    text="Проверить",
    command=check_answer,
    style="TButton"
)
check_btn.pack()

# Статус
status_label = ttk.Label(
    main_frame,
    text="",
    font=("Arial", 12)
)
status_label.pack(pady=10)

# Счетчик серии
streak_frame = ttk.Frame(main_frame)
streak_frame.pack()
ttk.Label(streak_frame, text="Текущая серия:").pack(side="left")
streak_label = ttk.Label(
    streak_frame,
    text="0",
    font=("Arial", 12, "bold"),
    foreground="green"
)
streak_label.pack(side="left")

# Подсказка
ttk.Label(
    main_frame,
    text="Нажмите Enter для проверки ответа",
    font=("Arial", 9)
).pack(pady=5)

# Запуск
show_word()
root.mainloop()