import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os
from datetime import datetime

# Константы
HISTORY_FILE = "history.json"
MIN_LEN = 4
MAX_LEN = 32

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x550")

        # Переменные настроек
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.history = []

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Слайдер длины
        tk.Label(self.root, text="Длина пароля:", font=("Arial", 10)).pack(pady=(10, 0))
        self.scale = tk.Scale(self.root, from_=MIN_LEN, to=MAX_LEN, orient=tk.HORIZONTAL, 
                              variable=self.length_var, length=300)
        self.scale.pack()

        # Чекбоксы
        frame_opts = tk.LabelFrame(self.root, text="Параметры", padx=10, pady=10)
        frame_opts.pack(pady=10)
        tk.Checkbutton(frame_opts, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w")
        tk.Checkbutton(frame_opts, text="Буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor="w")
        tk.Checkbutton(frame_opts, text="Спецсимволы (!@#$...)", variable=self.use_symbols).pack(anchor="w")

        # Кнопка генерации
        tk.Button(self.root, text="СГЕНЕРИРОВАТЬ", command=self.generate, 
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        # Вывод пароля
        self.entry_res = tk.Entry(self.root, font=("Courier", 14), justify="center")
        self.entry_res.pack(fill="x", padx=40, pady=5)

        # Таблица истории
        tk.Label(self.root, text="История генераций:").pack(pady=(10, 0))
        self.tree = ttk.Treeview(self.root, columns=("dt", "pw"), show="headings", height=8)
        self.tree.heading("dt", text="Дата и время")
        self.tree.heading("pw", text="Пароль")
        self.tree.column("dt", width=150)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def generate(self):
        # Валидация длины
        length = self.length_var.get()
        if not (MIN_LEN <= length <= MAX_LEN):
            messagebox.showerror("Ошибка", f"Длина должна быть от {MIN_LEN} до {MAX_LEN}")
            return

        # Пул символов
        pool = ""
        if self.use_digits.get(): pool += string.digits
        if self.use_letters.get(): pool += string.ascii_letters
        if self.use_symbols.get(): pool += string.punctuation

        if not pool:
            messagebox.showwarning("Внимание", "Выберите хотя бы один тип символов!")
            return

        # Генерация
        password = "".join(random.choice(pool) for _ in range(length))
        self.entry_res.delete(0, tk.END)
        self.entry_res.insert(0, password)

        # Сохранение
        record = {"date": datetime.now().strftime("%d.%m.%Y %H:%M"), "password": password}
        self.history.insert(0, record)
        self.update_table()
        self.save_history()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.history:
            self.tree.insert("", tk.END, values=(row["date"], row["password"]))

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_table()
            except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
 
