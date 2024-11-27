import psycopg2

# Параметри підключення до БД
conn = psycopg2.connect(
    dbname="university",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    address TEXT,
    phone VARCHAR(15) NOT NULL,
    course INT CHECK (course BETWEEN 1 AND 4),
    faculty VARCHAR(50) CHECK (faculty IN ('Аграрного менеджменту', 'Економіки', 'Інформаційних технологій')),
    group_name VARCHAR(10),
    is_headman BOOLEAN DEFAULT FALSE
);

CREATE TABLE Subjects (
    subject_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hours_per_semester INT NOT NULL,
    semesters INT NOT NULL
);

CREATE TABLE Exams (
    exam_id SERIAL PRIMARY KEY,
    exam_date DATE NOT NULL,
    student_id INT REFERENCES Students(student_id) ON DELETE CASCADE,
    subject_id INT REFERENCES Subjects(subject_id) ON DELETE CASCADE,
    grade INT CHECK (grade BETWEEN 2 AND 5)
);
""")

conn.commit()
print("Таблиці створено успішно.")
cursor.close()
conn.close()
