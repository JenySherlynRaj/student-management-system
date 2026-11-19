
from flask import Flask, render_template, request, redirect, url_for, flash
import re
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

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()
    course = request.form["course"].strip()

    # Check for empty fields
    if not all([name, email, phone, course]):
        flash("All fields are required!")
        return redirect(url_for("home"))

    # Validate email
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        flash("Please enter a valid email address!")
        return redirect(url_for("home"))

    # Validate Indian mobile number
    if not re.fullmatch(r"[6-9]\d{9}", phone):
        flash("Please enter a valid 10-digit mobile number!")
        return redirect(url_for("home"))

    connection = get_db_connection()

    # Check for duplicate email
    existing_student = connection.execute(
        "SELECT id FROM students WHERE LOWER(email) = LOWER(?)",
        (email,)
    ).fetchone()

    if existing_student:
        connection.close()
        flash("This email is already registered!")
        return redirect(url_for("home"))

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

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        course = request.form["course"].strip()

        # Check for empty fields
        if not all([name, email, phone, course]):
            connection.close()
            flash("All fields are required!")
            return redirect(url_for("home"))

        # Validate email
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            connection.close()
            flash("Please enter a valid email address!")
            return redirect(url_for("home"))

        # Validate Indian mobile number
        if not re.fullmatch(r"[6-9]\d{9}", phone):
            connection.close()
            flash("Please enter a valid 10-digit mobile number!")
            return redirect(url_for("home"))

        # Check whether another student uses this email
        existing_student = connection.execute(
            "SELECT id FROM students WHERE LOWER(email) = LOWER(?) AND id != ?",
            (email, student_id)
        ).fetchone()

        if existing_student:
            connection.close()
            flash("This email is already registered!")
            return redirect(url_for("home"))

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


