from datetime import datetime
import json
import os

tasks = []
STATES = dict(
	pending='⠐',
	done='✓',
	canceled='✗',
	postponed='➜',
)

def add(text):
    tasks.append(dict(
        text=text or input('Task: ') or 'Untitled task!',
        state='pending',
        date=datetime.now().date().isoformat(),
    ))
    save()

def find(arg):
    for task in tasks:
        if task['text'].startswith(arg):
            return task

def edit():
    pass

def postpone():
    pass

def mark(text, state):
    task = find(text)
    if task:
        task.update(state=state)
        save()

def show():
    os.system('cls||clear')
    print()
    for task in tasks:
        print(
            '',
            STATES[task['state']],
            task['text']
        )
    print()

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

def manual():
    pass

def menu():
    while True:
        show()
        cmd, arg = [*input('> ').split(' ', 1), ''][:2]
        match cmd:
            case 'a':
                add(arg)
            case 'e':
                edit()
            case 'd':
                mark(arg, 'done')
            case 'c':
                mark(arg, 'canceled')
            case 'p':
                postpone()
            case 'h':
                manual()
            case 'q':
                exit()
            case _:
                print('Wring command!')

if __name__ == '__main__':
    load()
    menu()