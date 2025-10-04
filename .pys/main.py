from task_service import TaskService
from utils import clear_screen
from cli_handlers import (
    handle_add_task,
    handle_list_tasks,
    handle_edit_task,
    handle_mark_completed,
    handle_delete_task
)

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

    menu_actions = {
        '1': handle_add_task,
        '2': handle_list_tasks,
        '3': handle_edit_task,
        '4': handle_mark_completed,
        '5': handle_delete_task,
    }
    
    while True:
        clear_screen()
        print('\n--- PySQLedule ---')
        print("1. Add new task")
        print("2. List tasks")
        print("3. Edit a task")
        print("4. Mark task as completed")
        print("5. Delete task")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == '6':
            print('\nLeaving...')
            break

        if choice in menu_actions:
            menu_actions[choice](task_service)
        else:
            print('Error: Invalid option. Please enter a number between 1 and 6.')
            input('Press Enter to continue...')

if __name__ == '__main__':
    main_menu()