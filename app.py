
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

    search_query = request.args.get("search", "")

    students = connection.execute(
        "SELECT * FROM students WHERE name LIKE ? ORDER BY id DESC",
        ("%" + search_query + "%",)
    ).fetchall()

    total_students = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_courses = connection.execute(
        "SELECT COUNT(DISTINCT course) FROM students"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        total_courses=total_courses,
        search_query=search_query
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
@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    connection = get_db_connection()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]

        connection.execute(
            "UPDATE students SET name = ?, email = ?, phone = ?, course = ? WHERE id = ?",
            (name, email, phone, course, student_id)
        )

        connection.commit()
        connection.close()

        flash("Student updated successfully!")

        return redirect(url_for("home"))

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    return render_template("edit_student.html", student=student)
if __name__ == "__main__":
    create_table()
    app.run(debug=True)


