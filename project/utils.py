import os
from datetime import datetime
from models import Task

def clear_screen():
    '''clears the terminal screen.'''
    os.system('cls' if os.name == 'nt' else 'clear')
        
def validate_and_format_date(date_str):
    '''validates if the date is in the format YYYYMMDD or YYYY/MM/DD and if it's not a past date.
    returns the formatted date if valid, otherwise returns None.'''
    date_str = date_str.replace('/', '')

    if len(date_str) != 8:
        print('Error: Date must be 8 digits long (YYYYMMDD).')
        return None
    
    try:
        input_date = datetime.strptime(date_str, '%Y%m%d').date()
        today = datetime.now().date()

        if input_date < today:
            print('Error: The deadline cannot be in the past. PLease enter a future date.')
            return None
        
        formatted_date = f'{date_str[0:4]}/{date_str[4:6]}/{date_str[6:8]}'
        return formatted_date
    except ValueError:
        print('Error: Invalid date format or date does not exist.\nUse YYYY/MM/DD or YYYYMMDD.')
        return None

def get_validated_date_input(prompt, default_value=None):
    '''prompts the user for a date, validates it, and returns the formatted date.
    returns the default_value if the user provides an empty input.'''
    while True:
        date_str = input(prompt)

        if not date_str and default_value is not None:
            return default_value
        
        formatted_date = validate_and_format_date(date_str)
        if formatted_date:
            return formatted_date
    
def show_tasks(tasks_list, status=None):
    '''displays tasks based on a given status filter.'''
    filtered_tasks = []
    if status:
        filtered_tasks = [task for task in tasks_list if task.status == status]
    else:
        filtered_tasks = tasks_list

    if not filtered_tasks:
        print('\nNo tasks registeres for this filter.')
    else:
        for task in filtered_tasks:
            print(f'\nID: {task.id}')
            print(f'Title: {task.title}')
            if task.description:
                print(f'Description: {task.description}')
            if task.deadline:
                print(f'Deadline: {task.deadline}')
            print(f'Status: {task.status.upper()}')
            print(f'Priority: {task.priority.upper()}')
            print('-'*20)