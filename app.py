
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
    return render_template("index.html")


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


if __name__ == "__main__":
    create_table()
    app.run(debug=True)


