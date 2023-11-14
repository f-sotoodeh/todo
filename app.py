from datetime import datetime, timedelta
import json
import os

tasks = []
STATES = dict(
	pending='⠐',
	done='✓',
	canceled='✗',
	postponed='➜',
)

def is_unique(text):
    for task in tasks:
        if task['text'] == text:
            return False
    return True

def add(text):
    text = text or input('Task title ("cancel" to cancel): ') or 'Untitled task!'
    if text.lower() == 'cancel':
        return
    if is_unique(text):
        tasks.append(dict(
            text=text,
            state='pending',
            date=datetime.now().date().isoformat(),
        ))
        save()
    else:
        return f'Task "{text}" already exists!'

def find(arg):
    for task in tasks:
        if task['text'] == arg:
            return task
    for task in tasks:
        if task['text'].startswith(arg):
            return task

def edit(text):
    task = find(text)
    if task:
        text = input('New task title (Leave blank to keep it unchanged): ') or task['text']
        if is_unique(text) or text == task['text']:
            task.update(text=text)
            save()
        else:
            return f'Task "{text}" already exists!'
    else:
        return f'There is no task "{text}"!'

def postpone(text):
    task = find(text)
    if task:
        task.update(
            date=(datetime.now()+timedelta(days=1)).date().isoformat(),
            state='postponed',
        )
        save()
    else:
        return f'There is no task "{text}"!'

def mark(text, state):
    task = find(text)
    if task:
        task.update(state=state)
        save()
    else:
        return f'There is no task "{text}"!'

def transfer():
    global tasks
    date = lambda task: datetime.strptime(task['date'], '%Y-%m-%d').date()
    today = datetime.now().date()
    for task in tasks:
        if date(task) < today:
            if task['state'] in ['pending', 'postponed']:
                task.update(
                    date=today.isoformat(),
                    state='pending',
                )
            elif task['state'] in ['done', 'canceled']:
                task.update(state='delete')
    tasks = [task for task in tasks if task['state']!='delete']
    save()

def show(message):
    os.system('cls||clear')
    print('    '+datetime.now().date().isoformat()+'\n')
    tasks.sort(key=lambda t: t['text'].lower())
    taskslist  = [t for t in tasks if t['state']=='pending']
    taskslist += [t for t in tasks if t['state']=='done']
    taskslist += [t for t in tasks if t['state']=='canceled']
    taskslist += [t for t in tasks if t['state']=='postponed']
    for task in taskslist:
        print(
            '',
            STATES[task['state']],
            task['text']
        )
    print()
    if message:
        print(message)

def save():
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)

def load():
    global tasks
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    except:
        pass

def quit():
    os.system('cls||clear')
    answer = input('Are you sure (y|N)? ').strip()
    match answer.lower():
        case 'y' | 'yes':
            exit()
        case 'n' | 'no' | _:
            return 'Welcome back :)'

def manual():
    os.system('cls||clear')
    print('''
    a, add                  To add a new task
    e, edit                 To edit a task
    d, done                 To mark a task as done
    c, cancel               To mark a task as canceled
    u, undone, pending      To mark a task as pending
    p, postpone             To postpone a task
    h, help, man, manual    To see the manual
    q, quit, exit           To quit the program
    ''')
    input('Press Enter to return to the menu.')

def menu():
    message = None
    while True:
        transfer()
        show(message)
        cmd, arg = [*input('> ').split(' ', 1), ''][:2]
        match cmd:
            case 'a' | 'add':
                message = add(arg)
            case 'e' | 'edit':
                message = edit(arg)
            case 'd' | 'done':
                message = mark(arg, 'done')
            case 'c' | 'cancel':
                message = mark(arg, 'canceled')
            case 'u' | 'undone' | 'pending':
                message = mark(arg, 'pending')
            case 'p' | 'postpone':
                message = postpone(arg)
            case 'h' | 'help' | 'man' | 'manual':
                message = manual()
            case 'q' | 'quit' | 'exit':
                message = quit()
            case _:
                message = 'Wrong command! Enter "h" to see the manual.'

if __name__ == '__main__':
    load()
    menu()