# Создание базы данных и таблицы
import sqlite3

conn = sqlite3.connect("Employees.db")  # Подключение к базе данных
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary REAL)""")
conn.commit()  # Сохранение базы данных
