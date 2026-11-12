import sqlite3

DATABASE = "university.db"


def connect():
    return sqlite3.connect(DATABASE)


def create_table():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                department TEXT NOT NULL,
                level INTEGER NOT NULL,
                email TEXT UNIQUE
            )
        """)


def add_sample_records():
    samples = [
        (1001, "Ada Johnson", "Computer Science", 200, "ada@example.com"),
        (1002, "Tunde Bello", "Accounting", 300, "tunde@example.com"),
        (1003, "Mira Okafor", "Computer Science", 100, "mira@example.com"),
        (1004, "David James", "Mass Communication", 400, "david@example.com"),
        (1005, "Zainab Musa", "Accounting", 200, "zainab@example.com"),
    ]
    with connect() as conn:
        conn.executemany("""
            INSERT OR IGNORE INTO students
            (student_id, full_name, department, level, email)
            VALUES (?, ?, ?, ?, ?)
        """, samples)


def add_student():
    try:
        student_id = int(input("Student ID: "))
        name = input("Full name: ").strip()
        department = input("Department: ").strip()
        level = int(input("Level (e.g. 100, 200): "))
        email = input("Email: ").strip()
        with connect() as conn:
            conn.execute("""
                INSERT INTO students VALUES (?, ?, ?, ?, ?)
            """, (student_id, name, department, level, email or None))
        print("Student added successfully.")
    except ValueError:
        print("ID and level must be numbers.")
    except sqlite3.IntegrityError as error:
        print("Could not add student:", error)


def display_students(rows):
    if not rows:
        print("No student records found.")
        return
    print("\nID | Name | Department | Level | Email")
    print("-" * 75)
    for row in rows:
        print(" | ".join(str(value) for value in row))


def view_all():
    with connect() as conn:
        rows = conn.execute("""
            SELECT student_id, full_name, department, level, email
            FROM students ORDER BY student_id
        """).fetchall()
    display_students(rows)


def view_department():
    department = input("Enter department: ").strip()
    with connect() as conn:
        rows = conn.execute("""
            SELECT student_id, full_name, department, level, email
            FROM students WHERE department = ? ORDER BY full_name
        """, (department,)).fetchall()
    display_students(rows)


def update_level():
    try:
        student_id = int(input("Student ID to update: "))
        new_level = int(input("New level: "))
        with connect() as conn:
            cursor = conn.execute(
                "UPDATE students SET level = ? WHERE student_id = ?",
                (new_level, student_id)
            )
        print("Level updated." if cursor.rowcount else "Student ID not found.")
    except ValueError:
        print("Student ID and level must be numbers.")


def delete_student():
    try:
        student_id = int(input("Student ID to delete: "))
        with connect() as conn:
            cursor = conn.execute(
                "DELETE FROM students WHERE student_id = ?", (student_id,)
            )
        print("Student deleted." if cursor.rowcount else "Student ID not found.")
    except ValueError:
        print("Student ID must be a number.")


def main():
    create_table()
    add_sample_records()
    actions = {
        "1": add_student,
        "2": view_all,
        "3": view_department,
        "4": update_level,
        "5": delete_student,
    }
    while True:
        print("""
STUDENT RECORD MANAGEMENT
1. Add student
2. View all students
3. Find students by department
4. Update a student's level
5. Delete a student
0. Exit
""")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
