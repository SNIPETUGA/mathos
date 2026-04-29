# Mathos - favour tracker

from datetime import date

favours = []

def log_favour():
    person = input("Who did you do it for? ")
    description = input("What did you do? ")
    favour = {
        "person": person,
        "description": description,
        "date": date.today()
    }
    favours.append(favour)
    print(f"\nLogged: {description} for {person} on {favour['date']}\n")

def show_favours():
    if len(favours) == 0:
        print("\nNo favours logged yet.\n")
    else:
        print("\nAll favours:")
        for favour in favours:
            print(f"- {favour['date']} | {favour['person']}: {favour['description']}")
        print()

def show_by_person():
    person = input("Which person? ")
    results = [f for f in favours if f["person"].lower() == person.lower()]
    if len(results) == 0:
        print(f"\nNo favours found for {person}.\n")
    else:
        print(f"\nFavours for {person}:")
        for favour in results:
            print(f"- {favour['date']}: {favour['description']}")
        print()

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