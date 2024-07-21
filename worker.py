from database import *
from processing import *
import time
import sys

while True:
    print(len(task_queue))
    if len(task_queue) > 0:
        for i in range(task_queue):
            print("doing work...")
            curr_task = task_queue[i]
            task_queue[i] = [curr_task[0], curr_task[1], "20", "0", None, curr_task[5]]
            compare_output = run_compare(curr_task[0], curr_task[1])
            if compare_output == "err1":
                task_queue[i] = [curr_task[0], curr_task[1], "100", "0", None, curr_task[5]]
            else:
                task_queue[i] = [curr_task[0], curr_task[1], "50", "0", None, curr_task[5]]
    else:
        time.sleep(2)
        print("waiting for tasks...")
        print(task_queue)