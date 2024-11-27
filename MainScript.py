import psycopg2
from prettytable import PrettyTable


# Функція для підключення до бази даних
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="university",
            user="admin",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Не вдалося підключитися до бази даних: {e}")
        return None

# Функція для виводу структури таблиці
def show_table_structure(cursor, table_name):
    cursor.execute(f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
    """)
    columns = cursor.fetchall()
    table = PrettyTable(["Column Name", "Data Type", "Nullable", "Default"])
    for col in columns:
        table.add_row(col)
    print(f"Структура таблиці `{table_name}`:")
    print(table)

# Функція для виводу даних таблиці
def show_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    table = PrettyTable(colnames)
    for row in rows:
        table.add_row(row)
    print(f"Дані таблиці `{table_name}`:")
    print(table)


# Функція для виконання та виводу запитів
def execute_query(cursor, query, description):
    cursor.execute(query)
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    table = PrettyTable(colnames)
    for row in rows:
        table.add_row(row)
    print(description)
    print(table)


# Основна функція
def main():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()

    # Список таблиць
    tables = ["students", "subjects", "exams"]

    # Вивід структури та даних таблиць
    for table in tables:
        show_table_structure(cursor, table)
        show_table_data(cursor, table)
        print("\n" + "=" * 50 + "\n")

    # Виконання запитів
    queries = [
        {
            "query": "SELECT last_name, first_name FROM Students WHERE is_headman = TRUE ORDER BY last_name",
            "description": "Студенти-старости (відсортовано за прізвищем):"
        },
        {
            "query": "SELECT student_id, AVG(grade) AS average_grade FROM Exams GROUP BY student_id",
            "description": "Середній бал кожного студента:"
        },
        {
            "query": "SELECT name, SUM(hours_per_semester * semesters) AS total_hours FROM Subjects GROUP BY name",
            "description": "Загальна кількість годин для кожного предмета:"
        },
        {
            "query": """
                SELECT s.last_name, s.first_name, e.grade 
                FROM Students s
                JOIN Exams e ON s.student_id = e.student_id
                JOIN Subjects sub ON e.subject_id = sub.subject_id
                WHERE sub.name = 'Математика'
            """,
            "description": "Успішність студентів по предмету 'Математика':"
        },
        {
            "query": "SELECT faculty, COUNT(*) FROM Students GROUP BY faculty",
            "description": "Кількість студентів на кожному факультеті:"
        },
        {
            "query": """
                SELECT s.last_name, sub.name, e.grade 
                FROM Students s
                JOIN Exams e ON s.student_id = e.student_id
                JOIN Subjects sub ON e.subject_id = sub.subject_id
                ORDER BY s.last_name, sub.name
            """,
            "description": "Оцінки кожного студента по кожному предмету:"
        }
    ]

    for q in queries:
        execute_query(cursor, q["query"], q["description"])
        print("\n" + "=" * 50 + "\n")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
