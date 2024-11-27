import psycopg2

conn = psycopg2.connect(
    dbname="university",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# 1. Студенти-старости
cursor.execute("""
SELECT last_name, first_name FROM Students WHERE is_headman = TRUE ORDER BY last_name
""")
print(cursor.fetchall())

# 2. Середній бал кожного студента
cursor.execute("""
SELECT student_id, AVG(grade) AS average_grade FROM Exams GROUP BY student_id
""")
print(cursor.fetchall())

# 3. Загальна кількість годин для кожного предмета
cursor.execute("""
SELECT name, SUM(hours_per_semester * semesters) AS total_hours FROM Subjects GROUP BY name
""")
print(cursor.fetchall())

# 4. Успішність студентів по предмету
selected_subject = "Математика"
cursor.execute("""
SELECT s.last_name, s.first_name, e.grade FROM Students s
JOIN Exams e ON s.student_id = e.student_id
JOIN Subjects sub ON e.subject_id = sub.subject_id
WHERE sub.name = %s
""", (selected_subject,))
print(cursor.fetchall())

# 5. Кількість студентів на кожному факультеті
cursor.execute("""
SELECT faculty, COUNT(*) FROM Students GROUP BY faculty
""")
print(cursor.fetchall())

# 6. Оцінки кожного студента по кожному предмету
cursor.execute("""
SELECT s.last_name, sub.name, e.grade FROM Students s
JOIN Exams e ON s.student_id = e.student_id
JOIN Subjects sub ON e.subject_id = sub.subject_id
ORDER BY s.last_name, sub.name
""")
print(cursor.fetchall())

cursor.close()
conn.close()
