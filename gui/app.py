import tkinter as tk
from tkinter import ttk
import psycopg2
from config import host, user, password, db_name, port

class PostgreSQLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PostgreSQL GUI App")

        # Подключение к базе данных PostgreSQL
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cursor = self.connection.cursor()

        # Создание и настройка виджетов для таблиц
        self.tables_label = tk.Label(root, text="Существующие таблицы:")
        self.tables_label.pack()

        self.tables_combobox = ttk.Combobox(root, state="readonly", width=47)
        self.tables_combobox.pack()

        self.show_tables_button = tk.Button(root, text="Показать таблицы", command=self.populate_tables_combobox)
        self.show_tables_button.pack()

        # Создание и настройка виджетов для выполнения SQL-запросов
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

# Создание экземпляра основного окна
root = tk.Tk()
app = PostgreSQLApp(root)

# Запуск главного цикла программы
root.mainloop()