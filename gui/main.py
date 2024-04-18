import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
from config import host, db_name, port #Убираем логин и пароль, для ввода его пользователем 


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

class PostgreSQLApp(tk.Frame):
    def __init__(self, root):

        self.root = root
        self.root.title("GUI Panel")
        self.root.geometry("500x500")
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=20)
        self.title_label = ttk.Label(self.main_frame, text="PostgreSQL GUI App", font=("Helvetica", 18))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
         # виджет для ввода имени пользователя и пароля
        self.user_label = tk.Label(self.root, text="User:")
        self.user_label.pack()
        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")  # чтобы скрыть введенные символы
        self.password_entry.pack()

        # Кнопка для подключения к базе данных
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_database)
        self.connect_button.pack()
        self.selected_code = None

    def connect_to_database(self):
        # Получаем значения из виджетов Entry
        user = self.user_entry.get()
        password = self.password_entry.get()

        # Здесь используем user и password для подключения к базе данных
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database!")
            self.user_label.pack_forget()
            self.user_entry.pack_forget()
            self.password_label.pack_forget()
            self.password_entry.pack_forget()
            self.connect_button.pack_forget()
            self.connect_button.destroy()

        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

        self.selected_code = None
        self.create_choice_buttons()

    def create_choice_buttons(self):
        # Уничтожаем предыдущие кнопки, если они существуют
        if hasattr(self, "code1_button"):
            self.code1_button.destroy()
        if hasattr(self, "code2_button"):
            self.code2_button.destroy()
        if hasattr(self, "code3_button"):
            self.code3_button.destroy()

        # Создаем новые кнопки
        self.code1_button = tk.Button(self.root, text="Существующие таблицы", command=self.load_code_1)
        self.code1_button.pack()

        self.code2_button = tk.Button(self.root, text="Запросы", command=self.load_code_2)
        self.code2_button.pack()

        self.code3_button = tk.Button(self.root, text="Номер телефона", command=self.load_code_3)
        self.code3_button.pack()

    def load_code_1(self):
        self.selected_code = 1
        self.clear_root()
        self.load_code1_widgets()

    def load_code_2(self):
        self.selected_code = 2
        self.clear_root()
        self.load_code2_widgets()

    def load_code_3(self):
        self.selected_code = 3
        self.clear_root()
        self.load_code3_widgets()

    #УНИЧТОЖЕНИЕ
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_code3_widgets(self):
        self.label = tk.Label(root, text="Выберите число:")
        self.label.pack(pady=10)

        # Создание ползунка
        self.scale = tk.Scale(root, from_=1_000_000_0000, to=9_999_999_9999, orient=tk.HORIZONTAL)
        self.scale.pack(fill=tk.X, padx=20)

        # Кнопка для отображения выбранного числа. Сомнительное предназначенние 
        self.button = tk.Button(root, text="Показать число", command=self.show_number)
        self.button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Назад", command=self.create_choice_buttons)
        self.back_button.pack(pady=10) 

    def show_number(self):
        selected_number = self.scale.get()
        messagebox.showinfo("Выбранное число", f"Выбранное число: {selected_number}")
 

    def load_code1_widgets(self):
        # Создание виджета с названием таблиц
        self.tables_label = ttk.Label(self.root, text="Существующие таблицы:", font=("Helvetica", 12, "bold"))
        self.tables_label.pack(pady=(10, 5))  # Добавляем немного отступа между виджетами

        # Выпадающий список для выбора таблиц
        self.tables_combobox = ttk.Combobox(self.root, state="readonly", width=40)
        self.tables_combobox.pack(pady=5)

        # Кнопка для отображения списка таблиц
        self.show_tables_button = tk.Button(self.root, text="Показать таблицы", command=self.populate_tables_combobox)
        self.show_tables_button.pack(pady=5)

        # Кнопка для отображения содержимого выбранной таблицы
        self.show_table_button = tk.Button(self.root, text="Показать содержимое таблицы", command=self.show_table)
        self.show_table_button.pack(pady=5)

        # Текстовое поле для отображения данных таблицы
        #self.table_data_text = tk.Text(self.root, height=20, width=100)
        #self.table_data_text.pack(pady=5)

        # Кнопка "Назад" для возвращения к предыдущему экрану
        self.back_button = tk.Button(self.root, text="Назад", command=self.create_choice_buttons)
        self.back_button.pack(pady=10)

    def load_code2_widgets(self):
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

    def show_table(self):
        selected_table = self.tables_combobox.get()
        if not selected_table:
            tk.messagebox.showwarning("Предупреждение", "Выберите таблицу для просмотра.")
            return
        try:
            self.clear_root()
            data = ()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {selected_table} LIMIT 0;")
            column_names = [desc[0] for desc in cursor.description]
            new_cur = self.connection.cursor()
            new_cur.execute (f"SELECT * FROM {selected_table};")
            data = (row for row in new_cur.fetchall())
            table = Table(self.root, headings = column_names, rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            self.back_button = tk.Button(self.root, text="Назад", command=self.create_choice_buttons)
            self.back_button.pack()
        except Exception as ex:
            tk.messagebox.showerror("Ошибка", f"Ошибка при получении данных таблицы: {ex}")
# Создание экземпляра основного окна
if __name__ == "__main__":
    root = tk.Tk()
    app = PostgreSQLApp(root)

    # Запуск главного цикла программы
    root.mainloop()
