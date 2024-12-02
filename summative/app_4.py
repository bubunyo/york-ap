import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Table View Example")
root.geometry("400x300")

# Create Treeview

notebook = ttk.Notebook(root)

# Create frames for tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

notebook.pack(expand=True, fill="both")

# Add content to tabs
tk.Label(tab1, text="Content of Tab 1").pack(pady=20)

columns = ("ID", "Name", "Age")
table = ttk.Treeview(tab2, columns=columns, show="headings", height=10)
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