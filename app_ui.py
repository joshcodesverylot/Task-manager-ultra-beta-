import tkinter as tk
import task_logic as logic
from tkinter import ttk
import threading

#AUDIT
#implement load on boot - Done
#implement update - Done
#implement delete - Done
#implement save - Done
#check if deleting data.json crashes the code or creates a new json file - done
# check if " " - done
root = tk.Tk()
root.geometry("1000x450")

def on_closing():
    logic.save_to_file()

    root.destroy()

def refresh_ui():
    listbox.delete(0, tk.END)

    current_tasks = logic.load_from_file()

    for task in current_tasks:
        listbox.insert(tk.END, task.title)
    
def refresh_ui_tree():
    for item in tree.get_children():
        tree.delete(item)

    current_tasks = logic.load_from_file()

    for task in current_tasks:

        if task.completed:
            status_symbol = "☑"
        else:
            status_symbol = "☐"

        tree.insert('', tk.END, values=(task.title, task.category, status_symbol))


def add():
    if entry_task.get() != "":
        category = logic.add_task(entry_task.get())

        listbox.insert("end", entry_task.get() + "  " + category)
        entry_task.delete(0, tk.END)
        listbox.config(height=listbox.size())


def add_tree():

    task_text1 = entry_task.get()

    task_text = task_text1.strip()

    if task_text != '':
        
        row_id = tree.insert('', 'end', values=(task_text, "Thinking...", '☐'))

        entry_task.delete(0, tk.END)

        threading.Thread(target=process_ai_task, args=(task_text, row_id), daemon=True).start()


def process_ai_task(task_text, row_id):
    try:
        category = logic.add_task(task_text)
        tree.after(0, update_row, row_id, task_text, category, '☐')
    except Exception as e:
        tree.after(0, update_row, row_id, task_text, "Error", '☐')

def update_row(row_id, task_text, category, status):
    tree.item(row_id, values=(task_text, category, status))


def on_double(event):
    region = tree.identify('region', event.x, event.y)
    if region != "cell":
        print("not cell")
    item_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    print(item_id, column)

    

    column_index = int(column.replace('#', '')) - 1

    if column_index == 2:
        return
    
    column_box = tree.bbox(item_id, column)
    
    entry_edit = ttk.Entry(tree, width=column_box[2])

    current_values = tree.item(item_id, 'values')
    current_text = current_values[column_index]

    entry_edit.insert(0, current_text)
    entry_edit.select_range(0, tk.END)


    entry_edit.place(x=column_box[0],
                     y=column_box[1],
                     w=column_box[2],
                     h=column_box[3])
    

    def save_edit(event):
        new_text = entry_edit.get()


        current_values_list = list(current_values)

        current_values_list[column_index] = new_text

        tree.item(item_id, values=current_values_list)


        task_index = tree.index(item_id)
        if column_index == 1:
            logic.update_task_title(task_index, new_text)
        elif column_index == 2:
            logic.update_task_category(task_index, new_text)
        entry_edit.destroy()
    
    def cancel_edit(event):
        entry_edit.destroy()

    entry_edit.bind('<Return>', save_edit)
    entry_edit.bind('<Escape>', cancel_edit)
    entry_edit.bind('<FocusOut>', cancel_edit)

    entry_edit.focus()


def toggle_check(event):
    item_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if item_id and column == "#3":
        current_values = tree.item(item_id, 'values')

        status_symbol = current_values[2]
        task = current_values[0]
        category = current_values[1]

        task_index = tree.index(item_id)

        if status_symbol == "☐":
            new_status = "☑"
            is_done = True
        else:
            new_status = "☐"
            is_done = False
        
        tree.item(item_id, values=(task, category, new_status))


        logic.tasks[task_index].completed = is_done

        logic.save_to_file()



def delete_tree():
    selected_item = tree.selection()

    if not selected_item:
        return
    print(selected_item)

    row_id = selected_item[0]

    index = tree.index(row_id)

    success = logic.delete_task(index)

    if success:
        tree.delete(row_id)

def delete():
    for index in reversed(listbox.curselection()):
        logic.delete_task(index)
        listbox.delete(index)
        
    listbox.config(height=listbox.size())

entry_task = tk.Entry(root, width=30)
entry_task.pack()

add_button = tk.Button(text="Add a task", command=add_tree)
add_button.pack(pady=10)

del_button = tk.Button(root, text="Delete task", command=delete_tree, bg="red", fg="white")
del_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, selectmode='multiple', font=35)
listbox.pack(pady=20)

columns = ('task', 'category', 'completed')
tree = ttk.Treeview(root, columns=columns, show='headings', height=10, )

tree.heading('task', text="Task Name")
tree.heading('category', text='Category')
tree.heading('completed', text='Status')

tree.column('task', width=200)
tree.column('category', width=100)
tree.column('completed', width=40)
tree.pack(pady=10)
refresh_ui_tree()

listbox.config(height=listbox.size())
tree.bind('<Button-1>', toggle_check)
tree.bind('<Double-1>', on_double)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()