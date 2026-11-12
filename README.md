# Student Record Management System

A simple Python command-line application using SQLite to manage university student records.

## Features
- Creates `university.db` and a `students` table automatically.
- Inserts five sample student records the first time it runs.
- Adds and displays students.
- Searches for students by department.
- Updates a student's level.
- Deletes a student record.

## Requirements
- Python 3
- SQLite (included with Python's `sqlite3` module)

## Run
```bash
python main.py
```

The database file is created automatically in the same folder. Sample records are inserted only when their student IDs do not already exist.
