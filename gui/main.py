import tkinter as tk
from tkinter import ttk
import psycopg2
from config import host, user, password, db_name, port

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PostgreSQL GUI")

        # Подключение к базе данных PostgreSQL
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.connection.autocommit = True

        # Создание и настройка виджетов
        self.tables_label = tk.Label(root, text="Существующие таблицы:")
        self.tables_label.pack()

        self.tables_combobox = ttk.Combobox(root, state="readonly", width=47)
        self.tables_combobox.pack()

        self.show_tables_button = tk.Button(root, text="Показать таблицы", command=self.populate_tables_combobox)
        self.show_tables_button.pack()

        self.show_table_button = tk.Button(root, text="Показать содержимое таблицы", command=self.show_table)
        self.show_table_button.pack()

        self.table_data_text = tk.Text(root, height=10, width=50)
        self.table_data_text.pack()

    def populate_tables_combobox(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
                )
                tables = cursor.fetchall()
                self.tables_combobox["values"] = [table[0] for table in tables]
        except Exception as ex:
            tk.messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {ex}")

    def show_table(self):
        selected_table = self.tables_combobox.get()
        if not selected_table:
            tk.messagebox.showwarning("Предупреждение", "Выберите таблицу для просмотра.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {selected_table};")
                table_data = cursor.fetchall()

                self.table_data_text.delete(1.0, tk.END)

                if table_data:
                    for row in table_data:
                        self.table_data_text.insert(tk.END, str(row) + "\n")
                else:
                    self.table_data_text.insert(tk.END, "Таблица пуста.")
        except Exception as ex:
            tk.messagebox.showerror("Ошибка", f"Ошибка при получении данных таблицы: {ex}")

# Создание экземпляра основного окна
root = tk.Tk()
app = DatabaseGUI(root)
root.mainloop()