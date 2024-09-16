import tkinter as tk
from tkinter import ttk

class ProcessTable:
    def __init__(self, master):
        self.tree = ttk.Treeview(master, columns=('PID', 'Name', 'Memory Usage', 'CPU Usage', 'Ports'), show='headings')
        self.tree.heading('PID', text='PID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Memory Usage', text='Memory Usage (bytes)')
        self.tree.heading('CPU Usage', text='CPU Usage (%)')
        self.tree.heading('Ports', text='Ports')
        self.tree.pack(fill=tk.BOTH, expand=True)

    def update_table(self, processes):
        self.clear_table()
        for process in processes:
            self.tree.insert('', 'end', values=(process['pid'], process['name'], process['memory_usage'], process['cpu_usage'], ', '.join(map(str, process['ports']))))

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)