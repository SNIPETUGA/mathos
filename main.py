# Mathos - favour tracker

import sqlite3
from datetime import date

def connect():
    conn = sqlite3.connect("mathos.db")
    return conn

def setup():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS favours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_favour():
    person = input("Who did you do it for? ")
    description = input("What did you do? ")
    today = str(date.today())
    conn = connect()
    conn.execute(
        "INSERT INTO favours (person, description, date) VALUES (?, ?, ?)",
        (person, description, today)
    )
    conn.commit()
    conn.close()
    print(f"\nLogged: {description} for {person} on {today}\n")

def show_favours():
    conn = connect()
    rows = conn.execute("SELECT person, description, date FROM favours").fetchall()
    conn.close()
    if len(rows) == 0:
        print("\nNo favours logged yet.\n")
    else:
        print("\nAll favours:")
        for row in rows:
            print(f"- {row[2]} | {row[0]}: {row[1]}")
        print()

def show_by_person():
    person = input("Which person? ")
    conn = connect()
    rows = conn.execute(
        "SELECT person, description, date FROM favours WHERE LOWER(person) = LOWER(?)",
        (person,)
    ).fetchall()
    conn.close()
    if len(rows) == 0:
        print(f"\nNo favours found for {person}.\n")
    else:
        print(f"\nFavours for {person}:")
        for row in rows:
            print(f"- {row[2]}: {row[1]}")
        print()

setup()

while True:
    print("1. Log a favour")
    print("2. See all favours")
    print("3. Search by person")
    print("4. Quit")
    choice = input("Choose: ")

    if choice == "1":
        log_favour()
    elif choice == "2":
        show_favours()
    elif choice == "3":
        show_by_person()
    elif choice == "4":
        break
    else:
        print("Please choose 1, 2, 3 or 4\n")