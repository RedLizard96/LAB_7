import psycopg2

def truncate_tables():
    try:
        # Підключення до БД
        conn = psycopg2.connect(
            dbname="university",
            user="admin",
            password="admin",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Відключення обмежень на зовнішні ключі
        cursor.execute("SET session_replication_role = 'replica';")

        # Очистка таблиць
        tables = ["Exams", "Subjects", "Students"]
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
            print(f"Таблиця {table} очищена.")

        # Відновлення обмежень на зовнішні ключі
        cursor.execute("SET session_replication_role = 'origin';")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    truncate_tables()
