class Task:
    def __init__(self, id, title, description, status, deadline, priority):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.priority = priority

    def __repr__(self):
        '''this method provides a string representations of the Task object.
        it's useful for debugging and printing.'''
        return f'Task(id={self.id}, title="{self.title}", status="{self.status}", priority="{self.priority}")'
    
#* Just a test
'''
if __name__ == '__main__':
    #create a new Task object
    my_task = Task(
        id=1,
        title='Learn Python',
        description='Study object-oriented programming.',
        status='pending',
        deadline='2025/12/31',
        priority='high' 
    )

    #print the Task object
    print(my_task)
    print(f'Task title: {my_task.title}')
    print(f'Task status: {my_task.status}')
'''