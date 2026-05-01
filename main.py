import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ===== ПРЕДОПРЕДЕЛЁННЫЕ ЗАДАЧИ =====
PREDEFINED_TASKS = [
    {"text": "Прочитать статью по Python", "type": "учёба"},
    {"text": "Сделать зарядку 15 минут", "type": "спорт"},
    {"text": "Ответить на рабочие письма", "type": "работа"},
    {"text": "Посмотреть лекцию по алгоритмам", "type": "учёба"},
    {"text": "Пробежка 3 км", "type": "спорт"},
    {"text": "Составить план на неделю", "type": "работа"},
    {"text": "Решить задачу на LeetCode", "type": "учёба"},
    {"text": "Отжимания 30 раз", "type": "спорт"},
    {"text": "Провести встречу с командой", "type": "работа"},
    {"text": "Выучить 10 новых слов", "type": "учёба"},
    {"text": "Сходить в спортзал", "type": "спорт"},
    {"text": "Сделать отчёт", "type": "работа"}
]

HISTORY_FILE = "tasks_history.json"
CUSTOM_FILE = "custom_tasks.json"

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        self.history = self.load_history()
        self.custom_tasks = self.load_custom_tasks()

        self.create_widgets()
        self.update_history_display()

    # ===== РАБОТА С JSON (с обработкой ошибок) =====
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки истории: {e}")
                return []
        return []

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_custom_tasks(self):
        if os.path.exists(CUSTOM_FILE):
            try:
                with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_custom_tasks(self):
        try:
            with open(CUSTOM_FILE, "w", encoding="utf-8") as f:
                json.dump(self.custom_tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")

    def get_all_tasks(self):
        return PREDEFINED_TASKS + self.custom_tasks

    # ===== ИНТЕРФЕЙС =====
    def create_widgets(self):
        # Рамка генерации
        gen_frame = ttk.LabelFrame(self.root, text="🎲 Генератор задач", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.generate_btn = ttk.Button(gen_frame, text="✨ Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        self.task_display = tk.Text(gen_frame, height=3, wrap="word", font=("Arial", 11), relief="sunken", borderwidth=1)
        self.task_display.pack(fill="x", padx=5, pady=5)
        self.task_display.config(state="disabled")

        # Рамка добавления задачи
        add_frame = ttk.LabelFrame(self.root, text="📝 Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Описание:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.task_entry = ttk.Entry(add_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Тип:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.type_var = tk.StringVar(value="учёба")
        type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, values=["учёба", "спорт", "работа"], state="readonly", width=15)
        type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.add_btn = ttk.Button(add_frame, text="➕ Добавить", command=self.add_custom_task)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        self.filter_var = tk.StringVar(value="все")
        filters = [("📋 Все", "все"), ("📚 Учёба", "учёба"), ("🏃 Спорт", "спорт"), ("💼 Работа", "работа")]
        for i, (text, value) in enumerate(filters):
            rb = ttk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=value, command=self.apply_filter)
            rb.grid(row=0, column=i, padx=10, pady=5)

        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="📜 История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("№", "Дата", "Задача", "Тип")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        self.tree.heading("№", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Задача", text="Задача")
        self.tree.heading("Тип", text="Тип")
        self.tree.column("№", width=40)
        self.tree.column("Дата", width=150)
        self.tree.column("Задача", width=400)
        self.tree.column("Тип", width=80)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.clear_btn = ttk.Button(btn_frame, text="🗑 Очистить историю", command=self.clear_history)
        self.clear_btn.pack(side="left", padx=5)

    # ===== ГЕНЕРАЦИЯ =====
    def generate_task(self):
        all_tasks = self.get_all_tasks()
        if not all_tasks:
            messagebox.showwarning("Внимание", "Нет доступных задач. Добавьте свои!")
            return

        task = random.choice(all_tasks)

        self.task_display.config(state="normal")
        self.task_display.delete(1.0, tk.END)
        icon = "📚" if task["type"] == "учёба" else "🏃" if task["type"] == "спорт" else "💼"
        self.task_display.insert(1.0, f"{icon} {task['text']}\nТип: {task['type']}")
        self.task_display.config(state="disabled")

        self.history.append({
            "text": task["text"],
            "type": task["type"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_history()
        self.update_history_display()

    # ===== ДОБАВЛЕНИЕ (с валидацией) =====
    def add_custom_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка", "Описание задачи не может быть пустым!")
            return

        self.custom_tasks.append({"text": text, "type": self.type_var.get()})
        self.save_custom_tasks()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена!")

    # ===== ФИЛЬТРАЦИЯ =====
    def apply_filter(self):
        self.update_history_display()

    def update_history_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_type = self.filter_var.get()
        filtered = self.history.copy()
        if filter_type != "все":
            filtered = [h for h in filtered if h["type"] == filter_type]

        filtered.reverse()

        for idx, record in enumerate(filtered, 1):
            icon = "📚" if record["type"] == "учёба" else "🏃" if record["type"] == "спорт" else "💼"
            self.tree.insert("", "end", values=(idx, record["timestamp"], record["text"], f"{icon} {record['type']}"))

    def clear_history(self):
        if not self.history:
            messagebox.showinfo("Инфо", "История уже пуста")
            return
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history.clear()
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
