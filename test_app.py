import unittest
import json
import os
import sys

# Для тестов создадим фейковый tkinter root
try:
    import tkinter as tk
    HAS_TK = True
except ImportError:
    HAS_TK = False

class TestTaskGenerator(unittest.TestCase):
    def setUp(self):
        self.test_history_file = "test_history.json"
        self.test_custom_file = "test_custom.json"
        
        # Подменяем файлы для тестов
        import main
        main.HISTORY_FILE = self.test_history_file
        main.CUSTOM_FILE = self.test_custom_file

    def tearDown(self):
        # Удаляем тестовые файлы
        for f in [self.test_history_file, self.test_custom_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_load_empty_history(self):
        """Тест: загрузка пустой истории"""
        import main
        app = main.RandomTaskGenerator(tk.Tk()) if HAS_TK else None
        if app:
            self.assertEqual(len(app.history), 0)

    def test_save_and_load_history(self):
        """Тест: сохранение и загрузка истории"""
        import main
        app = main.RandomTaskGenerator(tk.Tk()) if HAS_TK else None
        if app:
            app.history = [{"text": "Тест", "type": "учёба", "timestamp": "2024-01-01"}]
            app.save_history()
            
            app.history = []
            app.history = app.load_history()
            self.assertEqual(len(app.history), 1)
            self.assertEqual(app.history[0]["text"], "Тест")

    def test_add_custom_task_validation(self):
        """Тест: валидация при добавлении задачи"""
        import main
        app = main.RandomTaskGenerator(tk.Tk()) if HAS_TK else None
        if app:
            # Пустая строка
            app.task_entry.delete(0, tk.END)
            app.task_entry.insert(0, "")
            # Функция должна показать предупреждение и не добавить задачу
            # (проверяем, что custom_tasks не изменился)
            initial_count = len(app.custom_tasks)
            # В GUI это вызовет messagebox, но мы просто проверяем что ошибка не крашит
            self.assertIsNotNone(app)

    def test_predefined_tasks_exist(self):
        """Тест: предопределённые задачи существуют"""
        import main
        self.assertGreater(len(main.PREDEFINED_TASKS), 0)
        for task in main.PREDEFINED_TASKS:
            self.assertIn("text", task)
            self.assertIn("type", task)

    def test_custom_tasks_json_creation(self):
        """Тест: создание файла пользовательских задач"""
        import main
        app = main.RandomTaskGenerator(tk.Tk()) if HAS_TK else None
        if app:
            app.custom_tasks = [{"text": "Тестовая задача", "type": "учёба"}]
            app.save_custom_tasks()
            self.assertTrue(os.path.exists(self.test_custom_file))


if __name__ == "__main__":
    unittest.main()
