import sqlite3
from datetime import datetime
from task_manager import Task

# Класс для работы с базой данных
class Storage:
    # Метод для создания таблицы в базе данных
    @staticmethod
    def create_table(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                priority INTEGER NOT NULL,
                due_date TEXT NOT NULL,
                status BOOLEAN NOT NULL
            )
        ''')

    # Метод для сохранения задач в базу данных
    @staticmethod
    def save_tasks(tasks, db_name='tasks.db'):
        conn = sqlite3.connect(db_name)  # Подключение к базе
        cursor = conn.cursor()
        Storage.create_table(cursor)  # Создание таблицы, если она не существует

        cursor.execute('DELETE FROM tasks')  # Очищаем таблицу перед добавлением
        for task in tasks:
            cursor.execute('''
                INSERT INTO tasks (description, priority, due_date, status)
                VALUES (?, ?, ?, ?)
            ''', (task.description, task.priority, task.due_date.strftime('%Y-%m-%d'), task.status))

        conn.commit()  # Сохраняем изменения
        conn.close()  # Закрываем соединение

    # Метод для загрузки задач из базы данных
    @staticmethod
    def load_tasks(db_name='tasks.db'):
        conn = sqlite3.connect(db_name)  # Подключение к базе данных
        cursor = conn.cursor()
        Storage.create_table(cursor)  # Создание таблицы, если нет

        cursor.execute('SELECT description, priority, due_date, status FROM tasks')  # Запрос на выборку всех задач
        rows = cursor.fetchall()  # Получаем все строки
        tasks = []

        for row in rows:
            description, priority, due_date, status = row
            # Убираем временную часть, если она есть
            due_date = due_date.split('T')[0]
            task = Task(description, priority, datetime.strptime(due_date, '%Y-%m-%d'), status)
            tasks.append(task)  # Добавляем задачу в список

        conn.close()  # Закрываем соединение
        return tasks  # Возвращаем список задач