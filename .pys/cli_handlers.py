from utils import clear_screen, show_tasks, get_validated_date_input
from task_service import TaskService

def handle_add_task(task_service: TaskService):
    """Handles the logic for adding a new task."""
    while True:
        clear_screen()
        print('\n--- ADD NEW TASK ---')
        select_title = input('Enter the task title: ')
        select_description = input('Enter the task description: ')

        formatted_deadline = get_validated_date_input('Enter the deadline: (yyyy/mm/dd or yyyymmdd)')

        while True:
            select_priority = input('Enter the task priority (low, medium, high): ').lower()
            if select_priority in ['low', 'medium', 'high']:
                break
            else:
                print('Error: Invalid priority. Please enter low, medium or high.')

        task_service.add_task(select_title, select_description, formatted_deadline, select_priority)

        proceed = input('Want to register another task? (Y/N) ').upper()
        if proceed != "Y":
            break

        input('\nPress Enter to return to the main menu...')

def handle_list_tasks(task_service: TaskService):
    """Handles the task listing sub-menu logic and dispatches to sub-functions."""

    #sub-menu action handlers
    def show_all(service):
        tasks = service.get_all_tasks()
        show_tasks(tasks)
    
    def show_pending(service):
        tasks = service.get_all_tasks()
        show_tasks(tasks, status='pending')

    def show_completed(service):
        tasks = service.get_all_tasks()
        show_tasks(tasks, status='completed')

    def show_overdue(service):
        overdue_tasks = service.get_overdue_tasks()
        show_tasks(overdue_tasks)

    listing_options = {
        '1': show_all,
        '2': show_pending,
        '3': show_completed,
        '4': show_overdue,
    }

    while True: #sub-menu loop
        clear_screen()
        print('\n--- TASKS LIST ---')
        print('1. Show all tasks')
        print('2. Show only pending tasks')
        print('3. Show only completed tasks')
        print('4. Show only overdue tasks')
        print('5. Back to main menu')

        list_choice = input('\nChoose an option: ')

        if list_choice == '5':
            break
        elif list_choice in listing_options:
            listing_options[list_choice](task_service)
        else:
            print('Error: Invalid option. Please enter a number between 1 and 5.')

        input('\nPress Enter to return to the list menu...')

def handle_edit_task(task_service: TaskService):
    """Handles the logic for editing an existing task."""
    clear_screen()
    all_tasks = task_service.get_all_tasks()
    if not all_tasks:
        print('\nNo tasks to edit.')
    else:
        show_tasks(all_tasks)
        try:
            task_id_to_edit = int(input('\nEnter the ID of the task to edit: '))

            existing_task = None
            for task in all_tasks:
                if task.id == task_id_to_edit:
                    existing_task = task
                    break
            
            if not existing_task:
                print('\nError: Task not found.')
            else:
                print(f'\nEditing Task ID: {existing_task.id} - "{existing_task.title}"')
                new_title = input(f'Enter new title (current: "{existing_task.title}"): ') or existing_task.title
                new_description = input(f'Enter new description (current: "{existing_task.description}"): ') or existing_task.description

                new_deadline_str = get_validated_date_input(f'Enter the new deadline (current: "{existing_task.deadline}"): ', existing_task.deadline)

                while True:
                    new_priority = input(f'Enter new priority (current: "{existing_task.priority}"): ').lower() or existing_task.priority
                    if new_priority in ['low', 'medium', 'high']:
                        break
                    else:
                        print('Error: Invalid priority. Please enter low, medium or high.')

                task_service.update_task(task_id_to_edit, new_title, new_description, new_deadline_str, new_priority)
        except ValueError:
            print('Error: Invalid input. Please enter a valid number.')

    input('\nPress Enter to return to the menu...')

def handle_mark_completed(task_service: TaskService):
    """Handles the logic for making a task as completed."""
    clear_screen()
    all_tasks = task_service.get_all_tasks()
    if not all_tasks:
        print('\nNo tasks to update.')
    else:
        show_tasks(all_tasks)
        try:
            task_id_to_update = int(input('\nEnter the ID of the task to mar as completed: '))
            task_service.update_task_status(task_id_to_update)
        except ValueError:
            print('Error: Invalid input. Please enter a valid number.')
    
    input('\nPress Enter to return to the menu...')

def handle_delete_task(task_service: TaskService):
    """Handles the logic for deleting a task."""
    clear_screen()
    all_tasks = task_service.get_all_tasks()
    if not all_tasks:
        print('\nNo tasks to delete.')
    else:
        show_tasks(all_tasks)
        try:
            task_id_to_delete = int(input('\nEnter the ID of task to delete: '))
            task_service.delete_task(task_id_to_delete)
        except ValueError:
            print('Error: Invalid input. Please enter a valid number.')
        
    input('\nPress Enter to return to the menu...')