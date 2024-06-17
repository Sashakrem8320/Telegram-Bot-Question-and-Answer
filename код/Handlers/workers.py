import json
def new_task():
    global task
    with open('dummies.json') as json_file:
        task = json.load(json_file)
        return task

new_task()

def save_task():
    with open('dummies.json', 'w') as outfile:
        json.dump(task, outfile)

def getTask():
    return task

