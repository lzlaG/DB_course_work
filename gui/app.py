import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
from config import *
  
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)
  
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
  
        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)
  
        for row in rows:
            table.insert('', tk.END, values=tuple(row))
  
        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)
  
  
data = ()
with psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port
            ) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Заявки")
    data = (row for row in cursor.fetchall())

root = tk.Tk()
table = Table(root, headings=('id_заявки', 'Наименование', 'Дата', 'Тип_работы', 'Статус'), rows=data)
table.pack(expand=tk.YES, fill=tk.BOTH)
root.mainloop()