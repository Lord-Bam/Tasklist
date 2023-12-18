import json

class Task():
    def __init__(self, key=None, value=None):
        self.__key = int(key)
        self.__value = value
        
        
    @property
    def key(self):
        return self.__key
    
    
    @key.setter
    def key(self, key):
        self.__key = key
        return key
    
    
    @property
    def value(self):
        return self.__value
    
    
    @value.setter
    def value(self, value):
        self.__value = value
        return value
    
    
    #overwrite so print returns something nice.
    def __str__(self):
        return f"{self.__key}, {self.__value}"
    
    
    #Function used to return a dict so the object can be converted to json.
    def as_dict(self):
        task = {}
        task["key"] = self.__key
        task["value"] = self.__value       
        return task
    
    

class TaskList():
    
    def __init__(self):
        self.__tasks = []
        pass
    
    
    def add_task(self, new_task):
        key_found = False
        for task in self.__tasks:
            if task.key == new_task.key:
                key_found = True
        
        if not key_found:
            self.__tasks.append(new_task)
            
        return self.__tasks
            
        
        
    def update_task(self, key, value):
        for task in self.__tasks:
            if task.key == int(key):
                task.value = value
                        
        return self.__tasks
    
    
    def get_tasks(self):
        return self.__tasks
    
    
    def get_task(self, key):
        for task in self.__tasks:
            if task.key == key:
                return task
            
        return None
    
    
    def delete_task(self, key):
        for task in self.__tasks:
            if task.key == key:
                self.__tasks.remove(task)
            
        return None
    
    
    def read_tasks_from_file(self, file):     
        with open(file) as f:
            data = json.loads(f.read())
            for task in data:
                task = Task(**task)
                self.__tasks.append(task)
        return self.__tasks
    
    
    def get_json(self):
        tasks = []
        for task in self.get_tasks():
            tasks.append(task.as_dict())
        
        return json.dumps(tasks)
    
    
    def write_tasks_to_file(self, file):
        with open(file, "w+") as f:
            f.write(self.get_json())
            
            
    def get_highest_key(self):
        highest_key = -1
        for task in self.__tasks:
            if int(task.key) > highest_key:
                highest_key = int(task.key)
        
        return int(highest_key)
        