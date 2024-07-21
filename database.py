from tinydb import TinyDB, Query

file_verdb = TinyDB('file_verdb.json')
task_queue = []

def filever_add(ver_id):
    file_verdb.insert({'veriv_id': str(ver_id)})

def filever_verif(ver_id):
    User = Query()
    result = file_verdb.search(User.veriv_id == str(ver_id))
    if not result:
        return False
    else:
        return True

def expire_verif(ver_id):
    User = Query()
    file_verdb.remove(User.veriv_id == str(ver_id))


def new_task(base64img1, base64img2, ver_id):
    percentage = 0
    status = 0
    result = 0
    task_queue.append([base64img1, base64img2, percentage, status, result, ver_id])

def percent_task(ver_id):
    for i in range(len(task_queue)):
        if task_queue[i][5] == ver_id:
            return task_queue[i][2]
    return "Error, task ver_id not found"