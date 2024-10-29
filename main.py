import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db import Database

# Initialize database
db = Database("Employee.db")

# Manually set the TCL_LIBRARY path (adjust if needed)
os.environ['TCL_LIBRARY'] = r"C:\Users\admin\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"

# Create the main Tkinter window
root = tk.Tk()
root.title("EMPLOYEE MANAGEMENT SYSTEM")
root.geometry("1366x768+0+0")
root.config(bg="#2c3e50")
root.state("zoomed")  # Start in maximized mode

# Variables
name, age, doj, gender, email, contact = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

# Entries Frame
entries_frame = tk.Frame(root, bg="#535c68")
entries_frame.pack(side=tk.TOP, fill=tk.X)

# Title
title = tk.Label(entries_frame, text="EMPLOYEE MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=4, padx=10, pady=20, sticky="ew")

# Entry Labels and Fields
labels = ["NAME", "AGE", "D.O.J", "EMAIL", "GENDER", "CONTACT NO", "ADDRESS"]
variables = [name, age, doj, email, gender, contact]
columns = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]

# Create Labels and Fields in a Loop
for (i, j), text, var in zip(columns, labels[:6], variables):
    lbl = tk.Label(entries_frame, text=text, font=("Arial", 15), bg="#535c68", fg="white")
    lbl.grid(row=i + 1, column=j, padx=5, pady=5, sticky="w")
    if text == "GENDER":
        field = ttk.Combobox(entries_frame, textvariable=var, font=("Arial", 15), width=28, state="readonly")
        field['values'] = ("Male", "Female")
    else:
        field = tk.Entry(entries_frame, textvariable=var, font=("Arial", 15), width=30)
    field.grid(row=i + 1, column=j + 1, padx=5, pady=5, sticky="w")

# Address Field
lblAddress = tk.Label(entries_frame, text="ADDRESS", font=("Arial", 15), bg="#535c68", fg="white")
lblAddress.grid(row=4, column=0, padx=5, pady=5, sticky="w")

txtAddress = tk.Text(entries_frame, width=89, height=3, font=("Arial", 15))
txtAddress.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="w")



def getData(event):
    selected_row=tv.focus()
    data=tv.item(selected_row)
    global row
    row =data["values"]
    name.set(row[1])
    age.set(row[2])
    doj.set(row[3])
    email.set(row[4])
    gender.set(row[5])
    contact.set(row[6])
    txtAddress.delete(1.0,tk.END)
    txtAddress.insert(tk.END,row[7])



def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", tk.END, values=row)


def add_employee():
    if (
            name.get().strip() == "" or
            age.get().strip() == "" or
            doj.get().strip() == "" or
            email.get().strip() == "" or
            gender.get().strip() == "" or
            contact.get().strip() == "" or
            txtAddress.get(1.0, tk.END).strip() == ""
    ):
        messagebox.showerror("Error in input", "Please fill all the details")
        return

    # Insert employee data into the database (assuming a method exists for this)
    db.insert(name.get(), age.get(), doj.get(), email.get(), gender.get(), contact.get(),
              txtAddress.get(1.0, tk.END).strip())

    messagebox.showinfo("Success", "Employee added successfully!")
    clearall()
    displayAll()


def update_employee():
    if (
            name.get().strip() == "" or
            age.get().strip() == "" or
            doj.get().strip() == "" or
            email.get().strip() == "" or
            gender.get().strip() == "" or
            contact.get().strip() == "" or
            txtAddress.get(1.0, tk.END).strip() == ""
    ):
        messagebox.showerror("Error in input", "Please fill all the details")
        return

    # Insert employee data into the database (assuming a method exists for this)
    db.update(row[0],name.get(), age.get(), doj.get(), email.get(), gender.get(), contact.get(),
              txtAddress.get(1.0, tk.END).strip())

    messagebox.showinfo("Success", "Employee updated successfully!")
    clearall()
    displayAll()

def delete_employee():
    db.remove(row[0])
    clearall()
    displayAll()


def clearall():
    name.set("")
    age.set("")
    doj.set("")
    gender.set("")
    email.set("")
    contact.set("")
    txtAddress.delete(1.0, tk.END)


# Button Frame
btn_frame = tk.Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

# Configure Button Frame Columns
btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Buttons
buttons = [
    ("Add Details", "#16a885", add_employee),
    ("Update Details", "#2980b9", update_employee),
    ("Delete Details", "#c0392b", delete_employee),
    ("Clear Details", "#f39c12", clearall)
]
for i, (text, color, cmd) in enumerate(buttons):
    tk.Button(btn_frame, text=text, font=("Arial", 15, "bold"), bg=color, fg="white", bd=0, command=cmd).grid(
        row=0, column=i, padx=5, pady=5, sticky="ew"
    )

# Treeview Frame with Scrollbars
tree_frame = tk.Frame(root, bg="#ecf0f1", relief=tk.RIDGE)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

style = ttk.Style()
style.configure("mystyle.Treeview", font=('calibri', 13), rowheight=30)
style.configure("mystyle.Treeview.Heading", font=('calibri', 15))

tv = ttk.Treeview(
    tree_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8"),
    style="mystyle.Treeview", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
)

# Treeview Headings
columns = ["ID", "NAME", "AGE", "D.O.J", "EMAIL", "GENDER", "CONTACT", "ADDRESS"]
for i, col in enumerate(columns, 1):
    tv.heading(str(i), text=col)
    tv.column(str(i), width=150, anchor="center")

tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)

tv.pack(fill=tk.BOTH, expand=True)

# Configure Scrollbars
scroll_y.config(command=tv.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

scroll_x.config(command=tv.xview)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

displayAll()

# Run the Application
root.mainloop()
