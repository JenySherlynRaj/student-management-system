
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Student Management System</h1>
    <p>Welcome to our application!</p>
    <p>Our student management system is running.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
