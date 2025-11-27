import os
import random
from datetime import datetime

students = {}
current_user = ""
logged_in = False

# **FILE HANDLING **
def load_data():
    if not os.path.exists("students.txt"):
        return
    with open("students.txt", "r") as f:
        for line in f:
            data = line.strip().split("|")
            if len(data) == 10:
                u, p, n, r, b, y, e, ph, a, d = data
                students[u] = {
                    "password": p, "name": n, "roll_no": r, "branch": b, "year": y,
                    "email": e, "phone": ph, "address": a, "dob": d
                }

def save_data():
    with open("students.txt", "w") as f:
        for u, info in students.items():
            f.write(f"{u}|{info['password']}|{info['name']}|{info['roll_no']}|{info['branch']}|{info['year']}|{info['email']}|{info['phone']}|{info['address']}|{info['dob']}\n")

# **STUDENT FUNCTIONS**
def register():
    print(" Registration ")
    user = input("Username: ").strip()
    if user in students:
        print("Already registered, try another username.")
        return
    pwd = input("Password: ").strip()
    name = input("Full name: ")
    roll = input("Roll no: ")
    branch = input("Branch: ")
    year = input("Year: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    dob = input("Date of birth: ")

    students[user] = {
        "password": pwd, "name": name, "roll_no": roll, "branch": branch,
        "year": year, "email": email, "phone": phone, "address": address, "dob": dob
    }
    save_data()
    print("Registration done successfully!")

def login():
    global logged_in, current_user
    if logged_in:
        print("Already logged in.")
        return
    print("Login ")
    user = input("Username: ").strip()
    pwd = input("Password: ").strip()
    if user in students and students[user]["password"] == pwd:
        logged_in = True
        current_user = user
        print("Login Successful. Welcome", students[user]["name"])
    else:
        print("Invalid credentials.")

def show_profile():
    if not logged_in:
        print("Login first (only for student).")
        return
    data = students[current_user]
    print("--- Profile ---")
    for k, v in data.items():
        if k != "password":
            print(k, ":", v)

def update_profile():
    if not logged_in:
        print("Login first (only for student).")
        return
    print("--- Update Profile ---")
    info = students[current_user]
    for k in info:
        if k == "password":
            continue
        new_val = input(f"{k} ({info[k]}): ").strip()
        if new_val:
            info[k] = new_val
    save_data()
    print("Profile updated!")

def logout():
    global logged_in, current_user
    if not logged_in:
        print("No user logged in.")
        return
    print(current_user, "logged out.")
    logged_in = False
    current_user = ""

# ** QUIZ FUNCTIONS ** 
def setup_questions():
    data = {
        "os.txt": [
            "Which scheduling algorithm is preemptive?|FCFS|Round Robin|SJF|Priority|2",
            "What is a page fault?|Page in memory|Page not in memory|Page deleted|Page locked|2",
            "Main function of an OS is?|File sharing|Program execution|Network setup|All|2",
            "Which is not part of process state?|Running|Waiting|Blocked|Linking|4",
            "What is thrashing in OS?|Too many context switches|Too many I/O|Too many page faults|Too many threads|3"
        ],
        "dbms.txt": [
            "What is normalization?|Minimize redundancy|Maximize redundancy|Add columns|Delete keys|1",
            "Which key uniquely identifies a record?|Foreign key|Primary key|Candidate key|Super key|2",
            "Which join gives all matching rows?|Inner join|Left join|Full join|Cross join|3",
            "Which SQL clause filters rows?|WHERE|ORDER BY|GROUP BY|HAVING|1",
            "Transaction means?|Single query|Single logical unit of work|Backup|Shutdown|2"
        ],
        "python.txt": [
            "What is output of type([])?|list|tuple|dict|set|1",
            "Which keyword handles exceptions?|try|throw|catch|except|1",
            "Which function gives length?|count()|length()|len()|size()|3",
            "Which data type is mutable?|tuple|str|list|int|3",
            "What symbol starts a comment?|#|//|--|/*|1"
        ]
    }

    for file, questions in data.items():
        if not os.path.exists(file):
            with open(file, "w") as f:
                for q in questions:
                    f.write(q + "\n")

def load_questions(cat):
    fname = cat.lower() + ".txt"
    if not os.path.exists(fname):
        print("Question file missing:", fname)
        return []
    qlist = []
    with open(fname, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 6:
                q, a, b, c, d, ans = parts
                qlist.append({"q": q, "opt": [a, b, c, d], "ans": ans})
    return qlist

def quiz():
    if not logged_in:
        print("Only students can attempt quiz.")
        return
    print("--- Quiz Categories ---")
    print("1. OS")
    print("2. DBMS")
    print("3. PYTHON")
    ch = input("Choose category: ").strip()
    if ch == "1":
        cat = "OS"
    elif ch == "2":
        cat = "DBMS"
    elif ch == "3":
        cat = "PYTHON"
    else:
        print("Invalid choice.")
        return
    questions = load_questions(cat)
    if not questions:
        print("No questions found.")
        return
    random.shuffle(questions)
    questions = questions[:5]
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q['q']}")
        for j, opt in enumerate(q["opt"], 1):
            print(f"{j}. {opt}")
        ans = input("Your answer (1-4): ").strip()
        if ans.isdigit() and 1 <= int(ans) <= 4:
            if q["opt"][int(ans) - 1].lower() == q["opt"][int(q["ans"]) - 1].lower():
                score += 1
    print("Quiz completed! Your Score:", score, "/", len(questions))
    with open("scores.txt", "a") as f:
        f.write(f"{current_user}|{cat}|{score}/{len(questions)}|{datetime.now()}")

def view_scores():
    if not os.path.exists("scores.txt"):
        print("No scores yet.")
        return
    print("# All Scores ")
    with open("scores.txt", "r") as f:
        for line in f:
            u, c, s, d = line.strip().split("|")
            print(f"{u} | {c} | {s} | {d}" " -""Submited to Lilesh sir have a nice day.")

#**MAIN **
def main():
    load_data()
    setup_questions()
    while True:
        print("===== STUDENT QUIZ SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Show Profile")
        print("4. Update Profile")
        print("5. Attempt Quiz")
        print("6. View Scores")
        print("7. Logout")
        print("8. Exit")
        ch = input("Enter choice: ").strip()
        if ch == "1":
            register()
        elif ch == "2":
            login()
        elif ch == "3":
            show_profile()
        elif ch == "4":
            update_profile()
        elif ch == "5":
            quiz()
        elif ch == "6":
            view_scores()
        elif ch == "7":
            logout()
        elif ch == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

main()
