from task_service import TaskService
from utils import clear_screen, show_tasks, get_validated_date_input

#        |\___/|     /\___/\
#        )     (     )    ~(
#       =\     /=   =\~    /=
#         )===(       ) ~ (
#        /     \     /     \
#        |     |     ) ~   (
#       /       \   /     ~ \
#       \       /   \~     ~/
#========\__ __/=====\__~__/==============================================
#           (( !Kitties! ))          Welcome to my project!       
#===========))=========//=================================================
#          ((         ((                                        @piromali_
#           \)         \)

def main_menu():
    task_service = TaskService()
    
    overdue_tasks = task_service.get_overdue_tasks()
    if overdue_tasks:
        print(f"\nALERT: You have {len(overdue_tasks)} overdue tasks!")
        print("---------------------------------")
        for task in overdue_tasks:
            print(f"- ID: {task.id} | Title: {task.title}")
        print("---------------------------------")
        input("Press Enter to continue to the main menu...")

    while True:
        clear_screen()
        print('\n--- PyTaskManager ---')
        print("1. Add new task")
        print("2. List tasks")
        print("3. Edit a task")
        print("4. Mark task as completed")
        print("5. Delete task")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice not in ['1', '2', '3', '4', '5', '6']:
            print("Error: Invalid option. Please enter a number between 1 and 6.")
            input("Press Enter to continue...")
            continue

        if choice == '1':
            while True:
                selec_title = input('Enter the task title: ')
                select_description = input('Enter the task description: ')

                formatted_deadline = get_validated_date_input('Enter the deadline: (yyyy/mm/dd or yyyymmdd)')

                while True:
                    select_priority = input('Enter the task priority (low, medium, high): ').lower()
                    if select_priority in ['low', 'medium', 'high']:
                        break
                    else:
                        print('Error: Invalid priority. Please enter low, medium or high.')
                
                task_service.add_task(selec_title, select_description, formatted_deadline, select_priority)

                proceed = input('Want to register another task? (Y/N) ').upper()
                if proceed != 'Y':
                    break

        elif choice == '2':
            while True: #sub-menu
                clear_screen()
                print('\n---TASKS LIST ---')
                print('1. Show all tasks')
                print('2. Show only pending tasks')
                print('3. Show only completed tasks')
                print('4. Show only overdue tasks')
                print('5. Back to main menu')

                list_choice = input('\nChoose an option: ')
                
                all_tasks = task_service.get_all_tasks()

                if list_choice == '1':
                    show_tasks(all_tasks)
                elif list_choice == '2':
                    show_tasks(all_tasks, status='pending')
                elif list_choice == '3':
                    show_tasks(all_tasks, status='completed')
                elif list_choice == '4':
                    overdue_tasks = task_service.get_overdue_tasks()
                    show_tasks(overdue_tasks)
                elif list_choice == '5':
                    break
                else:
                    print('Error: Invalid option. Please enter a number between 1 and 5.')

                input("\nPress Enter to return to the list menu...")
            
            continue 

        elif choice == '3':
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
                                print('Error: Invalid priority. Please enter low, medium, or high.')
                        
                        task_service.update_task(task_id_to_edit, new_title, new_description, new_deadline_str, new_priority)
                        
                except ValueError:
                    print('Error: Invalid input. Please enter a valid number.')
            input("\nPress Enter to return to the menu...")

        elif choice == '4':
            clear_screen()
            all_tasks = task_service.get_all_tasks()
            if not all_tasks:
                print('\nNo tasks to update.')
            else:
                show_tasks(all_tasks)
                try:
                    task_id_to_update = int(input('\nEnter the ID of the task to mark as completed: '))
                    task_service.update_task_status(task_id_to_update)
                except ValueError:
                    print('Error: Invalid input. Please enter a valid number.')
            input("\nPress Enter to return to the menu...")

        elif choice == '5':
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
            input("\nPress Enter to return to the menu...")

        elif choice == '6':
            print('\nLeaving...')
            break

if __name__ == '__main__':
    main_menu()