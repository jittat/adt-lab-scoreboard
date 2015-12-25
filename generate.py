from jinja2 import Template
import json

USER_FILE_NAME = 'users.txt'
TASK_FILE_NAME = 'tasks.json'
TEMPLATE_FILE_NAME = 'index-template.html'

NO_SUBMISSION = 0
INCORRECT_SUBMISSION = -1
CORRECT_SUBMISSION = 1

def read_users(file_name):
    lines = open(file_name).readlines()

    users = []
    for l in lines:
        items = l.strip().split("\t")
        if len(items) >= 3:
            name = items[1]
            uva_id = items[2].strip()
            users.append({ 'name': name,
                           'uva_id': uva_id })

    return users

def extract_tasks(problem_list):
    tasks = []
    for pset in problem_list:
        for s in pset['sections']:
            tasks += s['problems']
    return tasks
        
def generate_table(users, tasks, display_tasks, task_status):
    template = Template(open(TEMPLATE_FILE_NAME).read())
    print(template.render(users=users,
                          tasks=tasks,
                          display_tasks=display_tasks,
                          task_status=task_status))

def main():
    users = read_users(USER_FILE_NAME)
    problem_data = json.loads(open(TASK_FILE_NAME).read())
    problem_list = problem_data['problemList']
    problems = problem_data['problems']

    tasks = extract_tasks(problem_list)
    display_tasks = [problems[str(p)] for p in tasks]

    task_status = {}
    for u in users:
        task_status[u['uva_id']] = {}
        for t in tasks:
            task_status[u['uva_id']][t] = NO_SUBMISSION

    generate_table(users,
                   tasks,
                   display_tasks,
                   task_status)
            

if __name__ == '__main__':
    main()
