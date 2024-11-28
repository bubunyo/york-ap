import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Table View Example")
root.geometry("400x300")

# Create Treeview
columns = ("ID", "Name", "Age")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
table.pack(fill="both", expand=True)

# Set column headings
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100)

# Add data to the table
data = [
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Charlie", 22)
]

for row in data:
    table.insert("", "end", values=row)


root.mainloop()