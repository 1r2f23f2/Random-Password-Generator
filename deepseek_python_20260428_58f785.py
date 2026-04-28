import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Хранилище истории
        self.history_file = "history.json"
        self.history = self.load_history()

        # Переменные
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        # Интерфейс
        self.create_widgets()
        self.update_history_table()

    def create_widgets(self):
        # Рамка параметров
        frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Ползунок длины
        ttk.Label(frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        self.length_slider = ttk.Scale(frame, from_=4, to=32, orient="horizontal",
                                       variable=self.length_var, command=self.update_length_label)
        self.length_slider.grid(row=0, column=1, padx=5, sticky="ew")
        self.length_label = ttk.Label(frame, text="12")
        self.length_label.grid(row=0, column=2, padx=5)
        self.update_length_label()

        # Чекбоксы
        ttk.Checkbutton(frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_symbols).grid(row=3, column=0, sticky="w")

        # Кнопка генерации
        ttk.Button(frame, text="Сгенерировать пароль", command=self.generate_password).grid(row=4, column=0, columnspan=3, pady=10)

        # Поле для вывода пароля
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, font=("Courier", 12), width=40).grid(row=5, column=0, columnspan=3, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        self.tree = ttk.Treeview(self.root, columns=("password", "length", "date"), show="headings")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.heading("date", text="Дата создания")
        self.tree.column("password", width=300)
        self.tree.column("length", width=80)
        self.tree.column("date", width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопка очистки истории
        ttk.Button(self.root, text="Очистить историю", command=self.clear_history).pack(pady=5)

    def update_length_label(self, *args):
        self.length_label.config(text=str(self.length_var.get()))

    def generate_password(self):
        length = self.length_var.get()
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Сохраняем в историю
        self.save_to_history(password, length)

    def save_to_history(self, password, length):
        self.history.append({
            "password": password,
            "length": length,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_history_to_file()
        self.update_history_table()

    def update_history_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.history[-20:]:  # показываем последние 20
            self.tree.insert("", "end", values=(entry["password"], entry["length"], entry["date"]))

    def clear_history(self):
        self.history.clear()
        self.save_history_to_file()
        self.update_history_table()
        messagebox.showinfo("История", "История очищена")

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history_to_file(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()