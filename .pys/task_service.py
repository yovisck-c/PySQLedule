import sqlite3
from models import Task
from datetime import datetime
from contextlib import contextmanager

class TaskService:
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        self.create_table()

    @contextmanager
    def get_db_connection(self):
        """creates a database connection and yields the connection object.
        this function now acts as a context manager."""
        conn = sqlite3.connect(self.db_name)
        conn.isolation_level = None
        try:
            yield conn
        finally:
            conn.close()
    
    def create_table(self):
        """creates the tasks table if it doesn't exist."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                priority TEXT NOT NULL DEFAULT 'medium'
            );
            """)
    
    def add_task(self, title, description, deadline, priority):
        """adds a new task to the database."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO tasks (title, description, deadline, priority)
            VALUES (?, ?, ?, ?);
            """, (title, description, deadline, priority))

            last_id = cursor.lastrowid
        
        print(f'Task "{title}" added with ID: {last_id}.')

    def get_all_tasks(self):
        """retrieves all tasks from the database and returns them as a list of Task objects."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, description, status, deadline, priority FROM tasks")
            tasks_data = cursor.fetchall()

        tasks = []
        for task_tuple in tasks_data:
            task_obj = Task(*task_tuple)
            tasks.append(task_obj)

        return tasks
    
    def update_task_status(self, task_id):
        """updates a task's status to 'completed' based on its ID."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
            if cursor.rowcount > 0:
                print(f'Task with ID {task_id} updated successfully.')
            else:
                print(f'Error: No task found with ID {task_id}.')

    def update_task(self, task_id, new_title, new_description, new_deadline, new_priority):
        """updates a task's title, description, deadline, and priority based on its ID."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE tasks
                    SET title = ?, description = ?, deadline = ?, priority = ?
                    WHERE id = ?;
                """, (new_title, new_description, new_deadline, new_priority, task_id))
                
                if cursor.rowcount > 0:
                    print(f'\nTask with ID {task_id} updated successfully.')
                else:
                    print(f'\nError: No task found with ID {task_id}.')
            except sqlite3.Error as e:
                print(f'\nDatabase error: {e}')

    def delete_task(self, task_id):
        """deletes a task from the database based on its ID."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount > 0:
                print(f'Task with ID {task_id} deleted successfully.')
            else:
                print(f'Error: No task found with ID {task_id}.')

    def get_overdue_tasks(self):
        """retrieves all overdue tasks from the database and returns them as a list of Task objects.
        a task is considered overdue if its deadline has passed."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            today_date = datetime.now().strftime('%Y/%m/%d')
            cursor.execute("""
                SELECT id, title, description, status, deadline, priority
                FROM tasks
                WHERE deadline < ? AND status = 'pending'
            """, (today_date,))
            tasks_data = cursor.fetchall()

        tasks = []
        for task_tuple in tasks_data:
            task_obj = Task(*task_tuple)
            tasks.append(task_obj)
        
        return tasks