import tasklist
import os
import json


#task tests
task1 = tasklist.Task("1","task1")

assert task1.key == 1
assert task1.value == "task1"

task1.key = "new_key"
assert task1.key == "new_key"

task1.value = "new_value"
assert task1.value == "new_value"

assert task1.__str__() == "new_key, new_value"

#tasklist tests

task2 = tasklist.Task("2","task2")

tasklist1 = tasklist.TaskList()
tasklist1.add_task(task2)
assert len(tasklist1.get_tasks()) == 1



task3 = tasklist.Task("3","task3")
tasklist1.add_task(task3)
assert len(tasklist1.get_tasks()) == 2

assert tasklist1.get_tasks()[0].__str__() == "2, task2"
assert tasklist1.get_tasks()[1].__str__() == "3, task3"

#add task with existing key.
#task is not added and length stays 2
task4 = tasklist.Task("3","task4")
tasklist1.add_task(task4)
assert len(tasklist1.get_tasks()) == 2


#get specific task with key
assert tasklist1.get_task(3) == task3

#change value
tasklist1.update_task(3,"new_value")
assert tasklist1.get_task(3).value == "new_value"


#remove
tasklist1.delete_task(3)
assert len(tasklist1.get_tasks()) == 1

tasklist2 = tasklist.TaskList()
tasklist2.read_tasks_from_file("testtasklist.json")

assert len(tasklist2.get_tasks()) == 4
assert tasklist2.get_task(1).value == "item1"

tasklist2.add_task(tasklist.Task("5","task5"))
assert len(tasklist2.get_tasks()) == 5


try:
    os.remove("testNewTaskList.txt")
except OSError:
    pass

tasklist2.write_tasks_to_file("testNewTaskList.json")

tasklist3 = tasklist.TaskList()
tasklist3.read_tasks_from_file("testNewTaskList.json")
assert len(tasklist3.get_tasks()) == 5

print(tasklist3.get_json())

assert tasklist3.get_highest_key() == 5
print("done")
