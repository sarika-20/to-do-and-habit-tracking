import streamlit as st
import datetime
import json
import os

# -------------------------- Helper Functions --------------------------

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_data(username):
    path = f"data_{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"todo": [], "habits": {}}

def save_data(username, data):
    with open(f"data_{username}.json", "w") as f:
        json.dump(data, f, indent=2)

# -------------------------- Page Layout --------------------------
st.set_page_config(page_title="To-Do + Habit Tracker", layout="centered")

st.title("📘 To-Do & Habit Tracker")

# -------------------------- User Login/Register --------------------------
users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with tab2:
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        if st.button("Register"):
            if new_username in users:
                st.warning("Username already exists.")
            else:
                users[new_username] = new_password
                save_users(users)
                st.success("User registered! Now login.")
else:
    username = st.session_state.username
    st.success(f"Welcome, {username}!")
    data = load_data(username)

    # -------------------------- To-Do Section --------------------------
    st.subheader("📅 To-Do List")
    with st.form("todo_form"):
        todo_date = st.date_input("Date", value=datetime.date.today())
        todo_task = st.text_input("Task")
        todo_type = st.radio("Type", ["Academic", "Personal"])
        submitted = st.form_submit_button("Add Task")
        if submitted and todo_task:
            data["todo"].append({"date": str(todo_date), "task": todo_task, "type": todo_type})
            save_data(username, data)
            st.success("Task added!")

    for t in data["todo"]:
        st.write(f"📌 **{t['task']}** ({t['type']}) - {t['date']}")

    # -------------------------- Habit Tracker --------------------------
    st.subheader("📈 Weekly Habit Tracker")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if "habits" not in data:
        data["habits"] = {}

    with st.form("habit_form"):
        habit_name = st.text_input("Add a Habit")
        add_habit = st.form_submit_button("Add Habit")
        if add_habit and habit_name:
            if habit_name not in data["habits"]:
                data["habits"][habit_name] = {day: False for day in days}
                save_data(username, data)

    for habit, record in data["habits"].items():
        st.markdown(f"### {habit}")
        cols = st.columns(7)
        for i, day in enumerate(days):
            checked = cols[i].checkbox(day, value=record[day], key=f"{habit}_{day}")
            data["habits"][habit][day] = checked
        save_data(username, data)

    # -------------------------- Weekly Summary --------------------------
    st.subheader("🏆 Most Completed Habits This Week")
    scores = {
        habit: sum(1 for done in record.values() if done)
        for habit, record in data["habits"].items()
    }
    sorted_habits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for habit, count in sorted_habits:
        st.write(f"✅ {habit}: {count}/7 days")

    # -------------------------- Logout --------------------------
    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()