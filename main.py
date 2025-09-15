from database_functions import add_task, list_tasks, validate_and_format_date, update_task_status, delete_task, create_table

def main_menu():
    create_table()

    while True:
        print('\n--- PyTaskManager ---')
        print("1. Add new task")
        print("2. List tasks")
        print("3. Mark task as completed")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            while True:
                selec_title = input('Enter the task title: ')
                select_description = input('Enter the task description: ')

                while True:
                    selec_deadline = input('Enter the deadline: (yyyy/mm/dd or yyyymmdd)')
                    formatted_deadline = validate_and_format_date(selec_deadline)
                    if formatted_deadline:
                        break

                add_task(selec_title, select_description, formatted_deadline)

                proceed = input('Want to register another task?? (Y/N)').upper()
                if proceed != 'Y':
                    break

        elif choice == '2':
            tasks_list = list_tasks()
            if not tasks_list:
                print("\nThere are no tasks registered.")
            else:
                print('\n--- Tasks List ---')
                for task in tasks_list:
                    task_id, title, description, status, deadline = task
                    print(f'ID: {task_id}, Title: {title}, Status: {status.upper()}')
        
        elif choice == '3':
            tasks_list = list_tasks()
            if not tasks_list:
                print('\nThere are no tasks to update.')
            else:
                print('\n--- Tasks List ---')
                for task in tasks_list:
                    task_id, title, description, status, deadline = task
                    print(f'ID: {task_id}, Title: {title}, Status: {status.upper()}')

                try:
                    task_id_to_update = int(input('\nEnter the ID of the task to mark as completed: '))
                    update_task_status(task_id_to_update)
                except ValueError:
                    print('Error: Invalid input. Please enter a valid number.')

        elif choice == '4':
            tasks_list = list_tasks()
            if not tasks_list:
                print('\nThere are no tasks to delete.')
            else:
                print('\n--- Tasks List ---')
                for task in tasks_list:
                    task_id, title, description, status, deadline = task
                    print(f'ID: {task_id}, Title: {title}, Status: {status.upper()}')

                try:
                    task_id_to_delete = int(input('\nEnter the ID of task to delete: '))
                    delete_task(task_id_to_delete)
                except ValueError:
                    print('Error: Invalid input. Please enter a valid numer.')

        elif choice == '5':
            print('Leaving...')
            break

if __name__ == "__main__":
    main_menu()