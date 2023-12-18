import tasklist 

def get_header():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Laget Sebastiaan</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
        </head>
        <body>
        <div class="container">
        '''


def get_footer():
    return '''
        </div>
        </body>
        </html>
        '''

def get_view_body():
    #get the tasks
    tasklist1 = tasklist.TaskList()
    tasklist1.read_tasks_from_file("tasklist.json")
    
    list_header = '''
    <ul class="list-group">
    '''
    
    list_lines = ""
    for task in tasklist1.get_tasks():
        list_lines = list_lines + f"  <li class='list-group-item d-flex justify-content-between align-items-center'>{task.value}\n"
        list_lines = list_lines + f"    <span class='badge badge-primary badge-pill'>task {task.key}</span>\n"
        list_lines = list_lines + f"  </li>\n"

    list_footer = '''
    </ul>
    '''
    
    buttons = ""
    buttons = buttons + f"<form action='' method='POST' role='form'>\n"
    buttons = buttons + f"<button name='button' value='edit_tasks' type='submit' class='btn btn-primary'>Edit Tasks</button>\n"
    buttons = buttons + f"<button name='button' value='delete_task' type='submit' class='btn btn-primary'>Delete Tasks</button>\n"
    buttons = buttons + f"<button name='button' value='add_task' type='submit' class='btn btn-primary'>Add Task</button>\n"
    buttons = buttons + f"</form>"
    
    
    body = list_header + list_lines + buttons + list_footer
    return body
    
def get_edit_body():
    #     FORM!!!  
    form_header = '''
    <form action="" method="POST" role="form">
    '''
    
    tasklist1 = tasklist.TaskList()
    tasklist1.read_tasks_from_file("tasklist.json")
    
    
    form_lines = ""
    for task in tasklist1.get_tasks():
    
        form_lines = form_lines + f"<div class='form-group'>\n"
        form_lines = form_lines + f"<label for='{task.key}'>task {task.key}</label>\n"
        form_lines = form_lines + f"<input name='{task.key}' type='{task.key}' class='form-control' id='{task.key}' value={task.value}>\n"
        form_lines = form_lines + f"</div>\n"

    
    #this also contains the button that was pressed!!!
    #name and value can be used to know which button was pressed. It is added to the post data.
    form_footer = '''
        <button name="button" value="save_edited_tasks" type="submit" class="btn btn-primary">Submit</button>
    </form>
    '''
    
    body = form_header + form_lines + form_footer
    return body
    
    
def get_add_body():
    #     FORM!!!  
    form_header = '''
    <form action="" method="POST" role="form">
    '''

    
    form_lines = ""

    
    form_lines = form_lines + f"<div class='form-group'>\n"
    form_lines = form_lines + f"<input name='task' value=>\n"
    form_lines = form_lines + f"</div>\n"

    
    #this also contains the button that was pressed!!!
    #name and value can be used to know which button was pressed. It is added to the post data.
    form_footer = '''
        <button name="button" value="save_added_tasks" type="submit" class="btn btn-primary">Submit</button>
    </form>
    '''
    
    body = form_header + form_lines + form_footer
    return body

def save_task(task):
    print("saving task", task)
    tasklist1 = tasklist.TaskList()
    tasklist1.read_tasks_from_file("tasklist.json")
    
    key = tasklist1.get_highest_key() + 1
    task = tasklist.Task(key, task)
    print(task)
    tasklist1.add_task(task)
    tasklist1.write_tasks_to_file("tasklist.json")
    
def save_edited_tasks(post_dict):
    tasklist1 = tasklist.TaskList()
    tasklist1.read_tasks_from_file("tasklist.json")
    for key in post_dict:
        if str(key) != "button":
            print(key,post_dict[key])
            tasklist1.update_task(int(key),post_dict[key])
    tasklist1.write_tasks_to_file("tasklist.json")
    pass
    
def delete_task(post_dict):
    print(deleting task)


def index(method="GET", url="/", post_dict=None):
    print(method, url, post_dict)

    if method == "GET":
        print("in Get")
        page = get_header() + get_view_body() + get_footer()
        return page
    
    
    if method == "POST":
        route = post_dict["button"]
        body = ""
        
        #reate the "body" of the page
        if route == "view_tasks":
            print("view")
            body = get_view_body()
        
        if route == "add_task":
            body =  get_add_body()
            
        if route == "delete_task":
            body = get_delete_body()
            print("delete")
            
        if route == "edit_tasks":
            body = get_edit_body()
            
        if route == "save_edited_tasks":
            print("saving multiple tasks and redirecting to view")
            save_edited_tasks(post_dict)
            body =  get_view_body()

        if route == "save_added_tasks":           
            print("saving task and redirecting to view")
            save_task(post_dict["task"])
            body =  get_view_body()
            
        if route == "save_deleted_task":
            print("saving deleted task")
            save_deleted_task()
            body = get_view_body()
            
        
        page = get_header() + body + get_footer()
        return page
    
    




        
