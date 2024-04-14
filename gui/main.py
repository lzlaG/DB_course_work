import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
from config import host, user, password, db_name, port

class PostgreSQLApp:
    def __init__(self, root):

        self.root = root
        self.root.title("PostgreSQL GUI App")

        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cursor = self.connection.cursor()

        self.selected_code = None

        self.create_choice_buttons()

    def create_choice_buttons(self):
        self.code1_button = tk.Button(self.root, text="Код 1", command=self.load_code_1)
        self.code1_button.pack()

        self.code2_button = tk.Button(self.root, text="Код 2", command=self.load_code_2)
        self.code2_button.pack()

    def load_code_1(self):
        self.selected_code = 1
        self.clear_root()
        self.load_code1_widgets()

    def load_code_2(self):
        self.selected_code = 2
        self.clear_root()
        self.load_code2_widgets()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_code1_widgets(self):
        self.tables_label = ttk.Label(self.root, text="Существующие таблицы:")
        self.tables_label.pack()
        self.tables_label.pack()

        self.tables_combobox = ttk.Combobox(root, state="readonly", width=47)
        self.tables_combobox.pack()

        self.show_tables_button = tk.Button(root, text="Показать таблицы", command=self.populate_tables_combobox)
        self.show_tables_button.pack()

        self.show_table_button = tk.Button(root, text="Показать содержимое таблицы", command=self.show_table)
        self.show_table_button.pack()

        self.table_data_text = tk.Text(root, height=10, width=50)
        self.table_data_text.pack()

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_choice_buttons)
        self.back_button.pack()

    def load_code2_widgets(self):
        self.query_label = ttk.Label(self.root, text="Введите SQL-запрос:")
        self.query_label.pack()
        self.query_label = tk.Label(root, text="Введите SQL-запрос:")
        self.query_label.pack()

        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        self.execute_button = tk.Button(root, text="Выполнить запрос", command=self.execute_query)
        self.execute_button.pack()

        self.result_label = tk.Label(root, text="Результат:")
        self.result_label.pack()

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack()

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_choice_buttons)
        self.back_button.pack()

    def populate_tables_combobox(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
                self.tables_combobox["values"] = [table[0] for table in tables]
        except Exception as ex:
            tk.messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {ex}")

    def execute_query(self):
        sql = self.query_entry.get()
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, results)
        except Exception as ex:
            tk.messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {ex}")
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
app = PostgreSQLApp(root)

# Запуск главного цикла программы
root.mainloop()