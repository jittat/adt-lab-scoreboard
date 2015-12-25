from jinja2 import Template
import json
import requests
import time

USER_FILE_NAME = 'users.txt'
TASK_FILE_NAME = 'tasks.json'
TEMPLATE_FILE_NAME = 'index-template.html'

NO_SUBMISSION = 0
INCORRECT_SUBMISSION = -1
CORRECT_SUBMISSION = 1

REQUEST_WAIT = 0.1

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

def fetch_user_submissions(uva_id):
    url = 'http://uhunt.felix-halim.net/api/subs-user/' + uva_id
    result = requests.get(url)
    data = json.loads(result.text)
    submissions = [{'problem_id': s[1],
                    'verdict_id': s[2]} for s in data['subs']]
    return submissions

def fetch_task_statuses(users, tasks, problems):
    task_status = {}
    for u in users:
        uva_id = u['uva_id']
        task_status[uva_id] = {}
        for t in tasks:
            task_status[uva_id][t] = NO_SUBMISSION

        if uva_id == '':
            continue
        
        submissions = fetch_user_submissions(u['uva_id'])
        time.sleep(REQUEST_WAIT)

        for s in submissions:
            if s['problem_id'] in task_status[uva_id]:
                t = s['problem_id']
                if s['verdict_id'] == 90:
                    task_status[uva_id][t] = CORRECT_SUBMISSION
                elif task_status[uva_id][t] == NO_SUBMISSION:
                    task_status[uva_id][t] = INCORRECT_SUBMISSION
    return task_status
            
def main():
    users = read_users(USER_FILE_NAME)
    problem_data = json.loads(open(TASK_FILE_NAME).read())
    problem_list = problem_data['problemList']
    problems = problem_data['problems']

    tasks = extract_tasks(problem_list)
    display_tasks = [problems[str(p)] for p in tasks]

    task_status = fetch_task_statuses(users, tasks, problems)
            
    generate_table(users,
                   tasks,
                   display_tasks,
                   task_status)
            

if __name__ == '__main__':
    main()
