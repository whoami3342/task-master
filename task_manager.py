from datetime import datetime

# Класс задачи
class Task:
    def __init__(self, description, priority, due_date, status=False):
        self.description = description  # Описание задачи
        self.priority = priority  # Приоритет задачи
        self.due_date = due_date  # Дата выполнения
        self.status = status  # Статус задачи (по умолчанию не выполнено)

# Класс для работы с задачами
class TaskManager:
    def __init__(self):
        self.tasks = []  # Список задач

    # Метод для добавления новой задачи
    def add_task(self, description, priority, due_date):
        task = Task(description, priority, due_date)  # Создание задачи
        self.tasks.append(task)  # Добавление задачи в список

    # Метод для вывода всех задач
    def view_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            status = "Выполнено" if task.status else "Не выполнено"
            print(f"{i}. {task.description} (Приоритет: {task.priority}, Дата: {task.due_date}, Статус: {status})")

    # Метод для обновления статуса задачи
    def update_task_status(self, task_index):
        if task_index < len(self.tasks) and task_index >= 0:
            task = self.tasks[task_index]
            task.status = not task.status  # Меняем статус
            print("Статус задачи обновлен.")
        else:
            print("Неверный индекс задачи.")

    # Метод для удаления задачи
    def delete_task(self, task_index):
        if task_index < len(self.tasks) and task_index >= 0:
            del self.tasks[task_index]  # Удаляем задачу из списка
            print("Задача удалена.")
        else:
            print("Неверный индекс задачи.")
