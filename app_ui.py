import tkinter as tk
import task_logic as logic

#ERRORS
#can't delete tasks after selecting
root = tk.Tk()
root.geometry("500x450")

def refresh_ui():
    listbox.delete(0, tk.END)

    current_tasks = logic.load_from_file()

    for task in current_tasks:
        listbox.insert(tk.END, task.title)
    


def add():
    if entry_task.get() != "":
        logic.add_task(entry_task.get())

        listbox.insert("end", entry_task.get())
        entry_task.delete(0, tk.END)
        listbox.config(height=listbox.size())

def delete():
    for index in reversed(listbox.curselection()):
        logic.delete_task(index)
        listbox.delete(index)
        
    listbox.config(height=listbox.size())

entry_task = tk.Entry(root, width=30)
entry_task.pack()

add_button = tk.Button(text="Add a task", command=add)
add_button.pack(pady=10)

del_button = tk.Button(root, text="Delete task", command=delete)
del_button.pack()

listbox = tk.Listbox(root, width=50, selectmode='multiple', font=35)
listbox.pack(pady=20)
refresh_ui()

listbox.config(height=listbox.size())



root.mainloop()