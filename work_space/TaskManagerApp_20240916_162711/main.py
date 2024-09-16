import tkinter as tk
from tkinter import ttk, messagebox
from process_utils import get_running_processes, terminate_process
from gui_components import ProcessTable
from config import DEFAULT_REFRESH_INTERVAL

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Task Manager')
        self.refresh_interval = DEFAULT_REFRESH_INTERVAL
        self.process_table = ProcessTable(master)
        self.create_widgets()
        self.start_refresh()

    def create_widgets(self):
        self.end_task_button = tk.Button(self.master, text='End Task', command=self.end_task)
        self.end_task_button.pack(pady=10)

    def start_refresh(self):
        self.refresh_tasks()
        self.master.after(self.refresh_interval * 1000, self.start_refresh)

    def refresh_tasks(self):
        processes = get_running_processes()
        self.process_table.update_table(processes)

    def end_task(self):
        selected_item = self.process_table.tree.selection()
        if not selected_item:
            messagebox.showwarning('Warning', 'No process selected!')
            return
        process_id = self.process_table.tree.item(selected_item, 'values')[0]
        try:
            terminate_process(int(process_id))
            self.refresh_tasks()
        except ValueError:
            messagebox.showerror('Error', 'Invalid Process ID selected!')

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()