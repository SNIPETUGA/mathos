# Mathos - Flask API with auth

from flask import Flask, request, jsonify, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "mathos-secret-key"

def connect():
    conn = sqlite3.connect("mathos.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS favours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            person TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])
    try:
        conn = connect()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Account created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    conn = connect()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"message": f"Welcome, {username}"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@app.route("/favours", methods=["GET"])
def get_favours():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM favours WHERE user_id = ?", (session["user_id"],)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/favours", methods=["POST"])
def log_favour():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    person = data["person"]
    description = data["description"]
    today = str(date.today())
    conn = connect()
    conn.execute(
        "INSERT INTO favours (user_id, person, description, date) VALUES (?, ?, ?, ?)",
        (session["user_id"], person, description, today)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Logged favour for {person}"}), 201

@app.route("/favours/<person>", methods=["GET"])
def get_by_person(person):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM favours WHERE user_id = ? AND LOWER(person) = LOWER(?)",
        (session["user_id"], person)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

setup()

if __name__ == "__main__":
    app.run(debug=True)