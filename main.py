import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from task_manager import TaskManager
from storage import Storage

# Класс для окна ввода даты
class DateDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Введите дату (ДД.ММ.ГГГГ):").grid(row=0)
        self.entry = tk.Entry(master)  # Поле для ввода
        self.entry.grid(row=0, column=1)
        return self.entry  # Фокус на поле ввода

    def apply(self):
        self.result = self.entry.get()  # Сохраняем результат

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Отмена", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Сегодня", width=10, command=self.set_today)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)  # При нажатии Enter
        self.bind("<Escape>", self.cancel)  # При нажатии Esc

        box.pack()

    def set_today(self):
        today = datetime.today().strftime('%d.%m.%Y')  # Устанавливаем текущую дату в формате ДД.ММ.ГГГГ
        self.entry.delete(0, tk.END)
        self.entry.insert(0, today)

# Основной класс приложения
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.task_manager = TaskManager()
        self.task_manager.tasks = Storage.load_tasks()  # Загружаем задачи

        self.create_widgets()  # Создаем интерфейс

    # Метод для создания виджетов
    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=60, height=15)  # Список задач
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame)  # Полоса прокрутки
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.load_tasks()  # Загружаем задачи

        # Кнопки управления задачами
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Добавить задачу", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Обновить статус", command=self.update_task_status)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.button_frame, text="Сохранить и выйти", command=self.save_and_exit)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Фильтрация задач
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(pady=10)

        self.filter_label = tk.Label(self.filter_frame, text="Фильтр:")
        self.filter_label.pack(side=tk.LEFT, padx=5)

        self.filter_var = tk.StringVar(value="Все")
        self.filter_menu = ttk.Combobox(self.filter_frame, textvariable=self.filter_var, values=["Все", "Выполнено", "Не выполнено", "Приоритет", "Срок выполнения"])
        self.filter_menu.pack(side=tk.LEFT, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.filter_tasks)

    # Метод для загрузки задач
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.task_manager.tasks, 1):
            status = "Выполнено" if task.status else "Не выполнено"
            due_date_str = task.due_date.strftime('%d.%m.%Y')  # Форматируем дату в формат ДД.ММ.ГГГГ
            self.task_listbox.insert(tk.END, f"{idx}. {task.description} (Приоритет: {task.priority}, Дата: {due_date_str}, Статус: {status})")

    # Метод для добавления задачи
    def add_task(self):
        description = simpledialog.askstring("Ввод", "Введите описание задачи:")
        if description:
            priority = simpledialog.askinteger("Ввод", "Введите приоритет (1-5):", minvalue=1, maxvalue=5)
            date_dialog = DateDialog(self.root, "Введите дату")
            due_date = date_dialog.result
            if due_date:
                due_date = datetime.strptime(due_date, '%d.%m.%Y')  # Преобразуем строку в дату
                self.task_manager.add_task(description, priority, due_date)
                self.filter_tasks()

    # Метод для обновления статуса задачи
    def update_task_status(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_index = selected_task[0]
            self.task_manager.update_task_status(task_index)
            self.filter_tasks()

    # Метод для удаления задачи
    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_index = selected_task[0]
            self.task_manager.delete_task(task_index)
            self.filter_tasks()

    # Метод для сохранения задач в базе данных и выхода
    def save_and_exit(self):
        Storage.save_tasks(self.task_manager.tasks)
        self.root.destroy()

    # Метод для фильтрации задач
    def filter_tasks(self, event=None):
        filter_by = self.filter_var.get()
        self.task_listbox.delete(0, tk.END)
        if filter_by == "Все":
            tasks = self.task_manager.tasks
        elif filter_by == "Выполнено":
            tasks = [task for task in self.task_manager.tasks if task.status]
        elif filter_by == "Не выполнено":
            tasks = [task for task in self.task_manager.tasks if not task.status]
        elif filter_by == "Приоритет":
            tasks = sorted(self.task_manager.tasks, key=lambda x: x.priority)
        elif filter_by == "Срок выполнения":
            tasks = sorted(self.task_manager.tasks, key=lambda x: x.due_date)
        else:
            tasks = self.task_manager.tasks

        for idx, task in enumerate(tasks, 1):
            status = "Выполнено" if task.status else "Не выполнено"
            due_date_str = task.due_date.strftime('%d.%m.%Y')  # Форматируем дату в формат ДД.ММ.ГГГГ
            self.task_listbox.insert(tk.END, f"{idx}. {task.description} (Приоритет: {task.priority}, Дата: {due_date_str}, Статус: {status})")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()