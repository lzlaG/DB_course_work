import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from config import host, db_name, port  # Импорт настроек подключения к базе данных


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


class PostgreSQLApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Приложение PostgreSQL")
        self.root.geometry("600x600")

        # self.scrollable_frame = ScrollableFrame(self)
        # self.scrollable_frame.pack(fill="both", expand=True)
        # self.root = self.scrollable_frame.scrollable_frame

        self.user_entry = None
        self.password_entry = None
        self.connection = None
        self.cursor = None

        self.init_ui()

    def init_ui(self):
        ttk.Label(self.root, text="Имя пользователя:").pack(pady=5)
        self.user_entry = ttk.Entry(self.root)
        self.user_entry.pack(pady=5)

        ttk.Label(self.root, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        connect_button = ttk.Button(self.root, text="Подключиться к базе данных", command=self.connect_to_database)
        connect_button.pack(pady=10)

    def connect_to_database(self):
        user = self.user_entry.get()
        password = self.password_entry.get()

        try:
            self.connection = psycopg2.connect(host=host, user=user, password=password, database=db_name, port=port)
            self.cursor = self.connection.cursor()
            messagebox.showinfo("Подключение", "Успешное подключение к базе данных")
            self.display_options()
        except Exception as e:
            messagebox.showerror("Ошибка подключения", str(e))

    def display_options(self):
        self.clear_widgets()
        ttk.Button(self.root, text="Добавить запись", command=self.add_new_record).pack(fill='x', padx=50, pady=10)
        ttk.Button(self.root, text="Просмотр таблиц", command=self.view_tables).pack(fill='x', padx=50, pady=10)
        ttk.Button(self.root, text="Выполнить SQL запрос", command=self.execute_sql_query).pack(fill='x', padx=50, pady=10)

    def view_tables(self):
        self.clear_widgets()
        try:
            # Извлечение имен таблиц из базы данных
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = [table[0] for table in self.cursor.fetchall()]

            ttk.Label(self.root, text="Выберите таблицу:").pack(pady=10)
            table_combo = ttk.Combobox(self.root, values=tables, state="readonly")
            table_combo.pack(pady=10)

            def on_table_select(event):
                selected_table = table_combo.get()
                self.show_table_data(selected_table)

            table_combo.bind('<<ComboboxSelected>>', on_table_select)
            ttk.Button(self.root, text="Назад", command=self.display_options).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Ошибка базы данных", str(e))

    def show_table_data(self, table_name):
        self.clear_widgets()
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()

            table_frame = ttk.Frame(self.root)
            table_frame.pack(expand=True, fill='both')

            table = ttk.Treeview(table_frame, columns=columns, show="headings")
            for col in columns:
                table.heading(col, text=col)
                table.column(col, anchor="center")

            for row in rows:
                table.insert('', 'end', values=row)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            table.pack(expand=True, fill='both')

            def update_record():
                selected_item = table.selection()
                if selected_item:
                    data = table.item(selected_item)['values']
                    edit_window = tk.Toplevel(self.root)
                    self.display_edit_window(edit_window, data, table_name, selected_item, columns)  # Добавлено columns
                    self.display_edit_window(edit_window, data, table_name, selected_item, columns)  # Добавлено columns

            def delete_record():
                selected_item = table.selection()
                if selected_item:
                    data = table.item(selected_item)['values']
                    try:
                        delete_query = f"DELETE FROM {table_name} WHERE {columns[0]} = %s"
                        self.cursor.execute(delete_query, (data[0],))
                        self.connection.commit()
                        table.delete(selected_item)
                        messagebox.showinfo("Success", "Запись удаленна успешно")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            ttk.Button(self.root, text="Изменение записи", command=update_record).pack(pady=10)
            ttk.Button(self.root, text="Удаление записи", command=delete_record).pack(pady=10)
            ttk.Button(self.root, text="Назад", command=lambda: self.view_tables()).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def display_edit_window(self, edit_window, data, table_name, tree_item, columns):
        edit_window.title("Изменение записи")
        entries = {}
        for index, value in enumerate(data):
            ttk.Label(edit_window, text=columns[index]).pack()
            entry = ttk.Entry(edit_window)
            entry.pack()
            entry.insert(0, value)
            entries[columns[index]] = entry

        def save_changes():
            values = [entry.get() for entry in entries.values()]
            # Подготовка SQL запроса для обновления записи
            set_clause = ', '.join([f"{col}= %s" for col in columns])
            where_clause = f"{columns[0]} = %s"  # Предполагаем, что первый столбец - это первичный ключ
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            values.append(data[0])  # Добавляем первичный ключ в конец списка значений для WHERE условия
            try:
                self.cursor.execute(update_query, values)
                self.connection.commit()
                messagebox.showinfo("Success", "Запись обновленна успешна")
                edit_window.destroy()
                self.show_table_data(table_name)  # Обновляем данные в таблице
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(edit_window, text="Сохранить изменения", command=save_changes).pack()

    def add_new_record(self):
        self.clear_widgets()

        ttk.Label(self.root, text="Выберите таблицу для добавления записи:").pack(pady=10)
        
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [table[0] for table in self.cursor.fetchall()]
        table_combo = ttk.Combobox(self.root, values=tables, state="readonly")
        table_combo.pack(pady=10)

        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=20)

        entries = {}  # Для хранения объектов Entry

        def on_table_select(event):
            table_name = table_combo.get()
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
            columns = [desc[0] for desc in self.cursor.description]
            
            # Очистка старых виджетов
            for widget in entry_frame.winfo_children():
                widget.destroy()

            # Создание новых Entry для каждого столбца
            for column in columns:
                ttk.Label(entry_frame, text=column).pack()
                entry = ttk.Entry(entry_frame)
                entry.pack()
                entries[column] = entry

        def insert_data():
            table_name = table_combo.get()
            columns = list(entries.keys())
            values = [entry.get() for entry in entries.values()]
            
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
            try:
                self.cursor.execute(query, values)
                self.connection.commit()
                messagebox.showinfo("Success", "Запись добавлена успешно!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add record: {str(e)}")

        table_combo.bind('<<ComboboxSelected>>', on_table_select)
        ttk.Button(self.root, text="Добавить запись", command=insert_data).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.display_options).pack(pady=10)

    def execute_sql_query(self):
        self.clear_widgets()
        # Создание виджетов для ввода SQL запроса
        ttk.Label(self.root, text="Введите SQL запрос:").pack(pady=10)
        query_text = tk.Text(self.root, height=10, width=50)
        query_text.pack(pady=10)

        # Функция для выполнения запроса
        def execute_query():
            query = query_text.get("1.0", "end-1c")
            try:
                # Выполнение запроса
                self.cursor.execute(query)
                # Если запрос на выборку данных, отображаем результаты
                if query.lower().startswith("select"):
                    rows = self.cursor.fetchall()
                    # Показываем результаты в новом окне или текстовом поле
                    result_window = tk.Toplevel(self.root)
                    result_window.title("Результаты запроса")
                    result_table = ttk.Treeview(result_window, columns=[f"Column {i+1}" for i in range(len(rows[0]))], show="headings")
                    for i, column in enumerate(result_table["columns"]):
                        result_table.heading(column, text=f"Column {i+1}")
                    for row in rows:
                        result_table.insert('', 'end', values=row)
                    result_table.pack(expand=True, fill='both', padx=10, pady=10)
                else:
                    # Для запросов, не возвращающих результат (например, UPDATE, DELETE), подтверждаем выполнение
                    self.connection.commit()
                    messagebox.showinfo("Выполнено", "SQL запрос успешно выполнен")
            except psycopg2.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {str(e)}")

        # Кнопка для выполнения запроса
        ttk.Button(self.root, text="Выполнить", command=execute_query).pack(pady=10)
        ttk.Button(self.root, text="Назад", command=self.display_options).pack(pady=10)

    def clear_widgets(self):
        # Функция для очистки всех виджетов на текущем окне
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PostgreSQLApp(root)
    root.mainloop()
