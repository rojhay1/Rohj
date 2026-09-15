import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL)
""")

conn.commit()

# Add student
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )

    clear_fields()
    display_students()

# Read students
def display_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:
        tree.insert("", tk.END, values=student)

# Update student
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )

    clear_fields()
    display_students()

# Delete student
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )

        clear_fields()
        display_students()

# Clear inputs
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

# Select student
def select_student(event):
    selected = tree.selection()

    if selected:
        student = tree.item(selected[0])["values"]

        clear_fields()
        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")
root.configure(bg="#0D1B2A")

# Colors
dark_blue = "#0D1B2A"
navy_blue = "#1B263B"
pink = "#FFB6C1"
light_pink = "#FFE4E9"
red = "#E63946"
dark_red = "#B71C1C"
white = "#FFFFFF"
dark_text = "#1B1B1B"

# Title
title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 18, "bold"),
    bg=dark_blue,
    fg=pink
)

title_label.pack(pady=15)

# Input frame
input_frame = tk.Frame(
    root,
    bg=light_pink,
    bd=2,
    relief="groove"
)

input_frame.pack(pady=10, padx=20)

# Name
tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 11, "bold"),
    bg=light_pink,
    fg=dark_blue
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)

name_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11),
    bg=white,
    fg=dark_text,
    relief="solid",
    bd=1
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)

# Age
tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11, "bold"),
    bg=light_pink,
    fg=dark_blue
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)

age_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11),
    bg=white,
    fg=dark_text,
    relief="solid",
    bd=1
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)

# Course
tk.Label(
    input_frame,
    text="Course:",
    font=("Arial", 11, "bold"),
    bg=light_pink,
    fg=dark_blue
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8
)

course_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11),
    bg=white,
    fg=dark_text,
    relief="solid",
    bd=1
)

course_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)

# Buttons
button_frame = tk.Frame(
    root,
    bg=dark_blue
)

button_frame.pack(pady=10)

# Add button
tk.Button(
    button_frame,
    text="Add",
    width=10,
    font=("Arial", 10, "bold"),
    bg=red,
    fg=white,
    activebackground=dark_red,
    activeforeground=white,
    command=add_student
).grid(
    row=0,
    column=0,
    padx=5
)

# Update button
tk.Button(
    button_frame,
    text="Update",
    width=10,
    font=("Arial", 10, "bold"),
    bg=navy_blue,
    fg=white,
    activebackground=dark_blue,
    activeforeground=white,
    command=update_student
).grid(
    row=0,
    column=1,
    padx=5
)

# Delete button
tk.Button(
    button_frame,
    text="Delete",
    width=10,
    font=("Arial", 10, "bold"),
    bg=dark_red,
    fg=white,
    activebackground="#8B0000",
    activeforeground=white,
    command=delete_student
).grid(
    row=0,
    column=2,
    padx=5
)

# Clear button
tk.Button(
    button_frame,
    text="Clear",
    width=10,
    font=("Arial", 10, "bold"),
    bg=pink,
    fg=dark_blue,
    activebackground="#FF91A4",
    activeforeground=dark_blue,
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)

# Table style
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background=dark_blue,
    foreground=white,
    font=("Arial", 10, "bold")
)

style.configure(
    "Treeview",
    background=white,
    foreground=dark_text,
    fieldbackground=white,
    font=("Arial", 10),
    rowheight=28
)

style.map(
    "Treeview",
    background=[
        ("selected", pink)
    ],
    foreground=[
        ("selected", dark_blue)
    ]
)

# Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Course"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column(
    "ID",
    width=50,
    anchor="center"
)

tree.column(
    "Name",
    width=200
)

tree.column(
    "Age",
    width=80,
    anchor="center"
)

tree.column(
    "Course",
    width=200
)

tree.pack(
    padx=20,
    pady=10
)

tree.bind(
    "<<TreeviewSelect>>",
    select_student
)

display_students()

root.mainloop()
