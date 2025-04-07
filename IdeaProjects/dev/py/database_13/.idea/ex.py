import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection."""
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
        return None

def execute_sql(conn, sql, data=None):
    """Execute SQL command."""
    try:
        c = conn.cursor()
        if data:
            c.execute(sql, data)
        else:
            c.execute(sql)
    except Error as e:
        print(e)

def insert_student(conn, name, surname, diary_nr):
    sql = """
    INSERT INTO students (name, surname, diary_nr)
    VALUES (?, ?, ?)
    """
    execute_sql(conn, sql, (name, surname, diary_nr))

def insert_subject(conn, subject_name, grade, student_id):
    sql = """
    INSERT INTO subjects (subject_name, grade, student_id)
    VALUES (?, ?, ?)
    """
    execute_sql(conn, sql, (subject_name, grade, student_id))

def fetch_students(conn):
    sql = "SELECT * FROM students"
    c = conn.cursor()
    c.execute(sql)
    return c.fetchall()

def fetch_subjects_with_students(conn):
    sql = """
    SELECT s.subject_name, s.grade, st.name, st.surname
    FROM subjects s
    JOIN students st ON s.student_id = st.id
    """
    c = conn.cursor()
    c.execute(sql)
    return c.fetchall()

def update_grade(conn, subject_id, new_grade):
    sql = "UPDATE subjects SET grade = ? WHERE id = ?"
    execute_sql(conn, sql, (new_grade, subject_id))

def delete_subject(conn, subject_id):
    sql = "DELETE FROM subjects WHERE id = ?"
    execute_sql(conn, sql, (subject_id,))

def delete_student(conn, student_id):
    sql = "DELETE FROM students WHERE id = ?"
    execute_sql(conn, sql, (student_id,))

def create_tables(conn):
    sql_students = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        diary_nr INTEGER NOT NULL
    );
    """

    sql_subjects = """
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subject_name TEXT NOT NULL,
        grade REAL NOT NULL,
        student_id INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    );
    """

    execute_sql(conn, sql_students)
    execute_sql(conn, sql_subjects)

if __name__ == "__main__":
    db_file = "school.db"

    conn = create_connection(db_file)
    if conn:
        with conn:
            create_tables(conn)

            insert_student(conn, "Jan", "Kowalski", 5)
            insert_student(conn, "Anna", "Nowak", 8)

            insert_subject(conn, "Math", 4.5, 1)
            insert_subject(conn, "Biology", 5.0, 2)

            print("Students:")
            for st in fetch_students(conn):
                print(st)

            print("\nSubjects with students:")
            for s in fetch_subjects_with_students(conn):
                print(s)

            update_grade(conn, 1, 5.0)
