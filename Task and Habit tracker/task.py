import streamlit as st
import pandas as pd
import datetime
import os
import json

# ---- Config ----
st.set_page_config(page_title="Habit & Task Tracker", layout="centered")
today = datetime.date.today()
DATA_FILE = "task_data.json"

# ---- Load or initialize data ----
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

if str(today) not in data:
    data[str(today)] = {"tasks": [], "habits": {}}

# ---- Session State for input ----
if "new_task" not in st.session_state:
    st.session_state["new_task"] = ""
if "new_habit" not in st.session_state:
    st.session_state["new_habit"] = ""

# ---- Title and date ----
st.title("🧠 Task & Habit Tracker")
st.write(f"📅 **Today:** {today.strftime('%A, %B %d, %Y')}")

# ---- Task List ----
st.subheader("✅ Daily Tasks")
for i, task in enumerate(data[str(today)]["tasks"]):
    checked = st.checkbox(task["name"], value=task["done"], key=f"task_{i}")
    data[str(today)]["tasks"][i]["done"] = checked

# Add new task
# Add new task
task_input = st.text_input("Add a new task")

if st.button("➕ Add Task"):
    if task_input:
        data[str(today)]["tasks"].append({"name": task_input, "done": False})
        st.rerun()  # Will reset the input since there's no key



# ---- Habit Tracker ----
st.subheader("🔁 Daily Habits")
habits = data[str(today)]["habits"]

# Add new habit
# Add new habit
new_habit = st.text_input("Add a new habit", key="habit_input")
if st.button("➕ Add Habit"):
    if new_habit:
        if new_habit not in habits:
            habits[new_habit] = {"done": False, "streak": 0}
        if "habit_input" in st.session_state:
            st.session_state["habit_input"] = ""
        st.rerun()


# Display habits
for habit in list(habits.keys()):
    done = st.checkbox(habit, value=habits[habit]["done"], key=f"habit_{habit}")
    if done and not habits[habit]["done"]:
        habits[habit]["streak"] += 1
    elif not done and habits[habit]["done"]:
        habits[habit]["streak"] = max(0, habits[habit]["streak"] - 1)
    habits[habit]["done"] = done
    st.write(f"🔥 Streak: {habits[habit]['streak']}")

# ---- Productivity Chart ----
st.subheader("📊 Productivity Overview")
dates = []
task_counts = []
habit_counts = []

for date_str, entry in data.items():
    dates.append(date_str)
    task_done = sum(t["done"] for t in entry["tasks"])
    habit_done = sum(1 for h in entry["habits"].values() if h["done"])
    task_counts.append(task_done)
    habit_counts.append(habit_done)

chart_df = pd.DataFrame({
    "Date": pd.to_datetime(dates),
    "Tasks Done": task_counts,
    "Habits Done": habit_counts
}).sort_values("Date")

st.line_chart(chart_df.set_index("Date"))

# ---- Save Data ----
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)
#streamlit run task.py