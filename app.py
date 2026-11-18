
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "student-management-secret"


# Connect to database
def get_db_connection():
    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create students table
def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Homepage
@app.route("/")
def home():
    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    total_courses = connection.execute(
        "SELECT COUNT(DISTINCT course) FROM students"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_courses=total_courses
    )


# Register student
@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]

    connection = get_db_connection()

    connection.execute(
        "INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)",
        (name, email, phone, course)
    )

    connection.commit()
    connection.close()

    flash("Student registered successfully!")

    return redirect(url_for("home"))

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    flash("Student deleted successfully!")

    return redirect(url_for("home"))
if __name__ == "__main__":
    create_table()
    app.run(debug=True)


