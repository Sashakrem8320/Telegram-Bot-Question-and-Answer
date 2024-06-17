import json
def new_task():
    global task
    with open('task.json') as json_file:
        task = json.load(json_file)
        return task

new_task()

def save_task():
    with open('task.json', 'w') as outfile:
        json.dump(task, outfile)

def getTask():
    return task

def new_task2():
    global task2
    with open('taskcheck.json') as json_file:
        task2 = json.load(json_file)
        return task2

new_task2()

def save_task2():
    with open('taskcheck.json', 'w') as outfile:
        json.dump(task2, outfile)

def getTask2():
    return task2

def new_task3():
    global task3
    with open('taskanswers.json') as json_file:
        task3 = json.load(json_file)
        return task3

new_task3()

def save_task3():
    with open('taskanswers.json', 'w') as outfile:
        json.dump(task3, outfile)

def getTask3():
    return task3



