import sqlite3
from datetime import datetime

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

# Function to create the tasks table
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        deadline TEXT,
        status TEXT NOT NULL DEFAULT 'pending'
    );
    """)
    conn.commit()
    conn.close()

# Function to add a new task
def add_task(title, description, deadline):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (title, description, deadline)
    VALUES (?, ?, ?);
    """, (title, description, deadline))
    conn.commit()
    conn.close()

# Function to list all tasks
def list_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, status, deadline FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Function to validate and format the date
def validate_and_format_date(date_str):
    """
    Validates if the date is in the format YYYYMMDD or YYYY/MM/DD and formats it to YYYY/MM/DD.
    Returns the formatted date if it is valid, otherwise returns None.
    """
    date_str = date_str.replace('/', '')
    
    if len(date_str) != 8:
        print('Error: Date must be 8 digits long (YYYYMMDD).')
        return None
    
    try:
        datetime.strptime(date_str, '%Y%m%d')
        formatted_date = f'{date_str[0:4]}/{date_str[4:6]}/{date_str[6:8]}'
        return formatted_date
    except ValueError:
        print('Error: Invalid date format or date does not exist. Use YYYY/MM/DD or YYYYMMDD.')
        return None

# Function to update a task's status
def update_task_status(task_id):
    """
    Updates the status of a task to 'completed' based on its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Task with ID {task_id} updated successfully.')
        else:
            print(f'Error: No task found with ID {task_id}.')
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    finally:
        conn.close()

# Function to delete a task
def delete_task(task_id):
    """
    Deletes a task from the database based on its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Task with ID {task_id} deleted successfully.')
        else:
            print(f'Error: No task found with ID {task_id}.')
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    finally:
        conn.close()