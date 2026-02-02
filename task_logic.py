import json
tasks = []
priority_map = {
    "H": 1,
    "M": 2,
    "L": 3,
    "U": 4,
}



#ERRORS
# 

class Task:
    def __init__(self, title, completed=False, priority="U"):
        self.title = title
        self.completed = completed
        self.priority = priority
    
    def change_title(self, title):
        self.title = title
    
    def change_completed(self, completed):
        self.completed = completed
    
    def change_priority(self, priority):
        self.priority = priority
    
    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority
        }


#Converts dictionary to list
def to_list(data):
    temp_title = None
    temp_priority = None
    temp_completed = None
    temp_task = None
    for task in data:
        for index , (key, item) in enumerate(task.items()):
            if key == "title":
                temp_title = item
            elif key == "completed":
                temp_completed = item
            elif key == "priority":
                temp_priority = item
        temp_task = Task(temp_title, temp_completed, temp_priority)
        tasks.append(temp_task)


#Overwrites current task list with tasks from data.json
def load_from_file():
    try:
        filepath = "data.json"
        tasks.clear()
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        to_list(data)
        print("Loading file back")
    except FileNotFoundError:
        print("No Saves Found")
        return []
    except json.JSONDecodeError:
        return []


#Saves file to data.json
def save_to_file():
    file_path = "data.json"
    tasks_json = [task.to_dict() for task in tasks]
    with open(file_path, 'w') as file:
        json.dump(tasks_json, file, indent=4)

    print(f"Tasks saved to {file_path}")

def sort_tasks(order):
    if order == "ascending":
        tasks.sort(key=lambda x: priority_map[x.priority])
        print("sorted tasks from high priority")
        view_tasks(tasks)
    elif order == "descending":
        tasks.sort(key=lambda x: priority_map[x.priority], reverse=order)
        print("sorted tasks from lowest priority")
        view_tasks(tasks)

def search_task(keyword):
    keyword_list = []
    for task in tasks:
        if keyword.lower() in task.title.lower():
            keyword_list.append(task)
    view_tasks(keyword_list)
    

#Adds task objects to the tasks list
def add_task(title):
    temp_task = Task(title)
    tasks.append(temp_task)
    print("Task:", temp_task.title, "added!")


#Edits the task
def edit_task(index):
    #Editting the task
    task_edit = input("[T] Change Title | [C] Change Completed | [P] Change Priority(HIGH, MEDIUM, LOW, UNKNOWN)")
    task_edit = task_edit.lower().strip()
    
    #change title
    if task_edit == 't':
        new_title = input("New title: ")
        tasks[index].change_title(new_title)
    
    #Change status of task to True or False
    elif task_edit == 'c':
        ask_completed = input("Finished task? (Y/N)")
        ask_completed = ask_completed.lower().strip()
        if ask_completed == 'y':
            tasks[index].change_completed(True)
        elif ask_completed == 'n':
            tasks[index].change_completed(False)

    #change the Priority of the task
    elif task_edit == 'p':
        ask_priority = input("[H] HIGH,[M] MEDIUM,[L] LOW,[U] UNKNOWN?")
        ask_priority = ask_priority.lower().strip()
        while ask_priority not in "hmlu":
            ask_priority = input("[H] HIGH,[M] MEDIUM,[L] LOW,[U] UNKNOWN?")
            ask_priority = ask_priority.lower().strip()
        ask_priority = ask_priority.upper()
        tasks[index].priority = ask_priority


#Displays all tasks along with index options, checkbox showing its state and its priority
def view_tasks(tasks):
    print("These are your Tasks:")
    for i in range(len(tasks)):
        mark_checkbox = "[X]" if tasks[i].completed else "[ ]"
        priority_label = "Unknown" if tasks[i].priority == 'U' else \
                          "High" if tasks[i].priority == 'H' else \
                          "Medium" if tasks[i].priority == 'M' else \
                          "Low" 
        print(i,f": {mark_checkbox} :",tasks[i].title, "-", priority_label)


#Catches Index errors after selecting tasks
def delete_task(index):
    try:
        removed = tasks.pop(index)
        print(f"Deleting {removed.title}")
        view_tasks()
    except IndexError:
        print("Error: That task Number does not exist")

def main():
    print("Welcome back Joshua")
    print("---TASK MANAGER---")
    while True:

        choice = input("[A] Add a task | [E] Edit a task | [L] Load back up | [R] Remove a task | [S] Save tasks | [SE] Search tasks | [SA/SD] Show tasks ascending/descending in priority | [V] View tasks | [Q] Quit \n")
        choice = choice.lower().strip()

        #Adding a task
        if choice == 'a':
            task_input = input("Please enter your task: ")
            add_task(task_input)

        #Removing a task
        elif choice == 'r':
            task_remove = int(input("Please specify the numbered task to remove: "))
            delete_task(task_remove)

        #Viewing a task
        elif choice == 'v':
            view_tasks(tasks)

        #Editting a task
        elif choice == 'e':
            print("Editting task")
            view_tasks(tasks)
            edit_index = int(input("please pick the task you want to edit: "))
            while True:
                if 0 <= edit_index < len(tasks):
                    break
                else:
                    edit_index = int(input("please pick the task you want to edit: "))
            edit_task(edit_index)



        elif choice == 'l':
            print("Loading saved tasks")
            load_from_file()
            

        #Exitting
        elif choice == 'q':
            print("Goodbye Joshua")
            break
        
        #Saving
        elif choice == 's':
            save_to_file()

        
        elif choice == "se":
            search_input = input("Please enter your keyword:")
            search_task(search_input)
        
        elif choice == "sa":
            sort_tasks("ascending")
        elif choice == "sd":
            sort_tasks("descending")
        #Please enter a valid option
        else:
            print("Please enter an appropiate option...")
        


        

if __name__ == "__main__":
    main()