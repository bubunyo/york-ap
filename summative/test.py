import tkinter as tk
from tkinter import messagebox, simpledialog

# Create the main window
root = tk.Tk()
root.title("Dialogs Example")
root.geometry("300x200")

# Function to show different dialogs
def show_info():
    messagebox.showinfo("Information", "This is an info dialog!")

def show_warning():
    messagebox.showwarning("Warning", "This is a warning dialog!")

def show_error():
    messagebox.showerror("Error", "This is an error dialog!")

def ask_question():
    response = messagebox.askquestion("Question", "Do you like Python?")
    print("Response:", response)  # Prints 'yes' or 'no'

def ask_ok_cancel():
    response = messagebox.askokcancel("Confirmation", "Do you want to proceed?")
    print("Response:", response)  # Prints True or False

def ask_input():
    user_input = simpledialog.askstring("Input", "What is your name?")
    print("User Input:", user_input)

# Buttons to trigger dialogs
tk.Button(root, text="Show Info", command=show_info).pack(pady=5)
tk.Button(root, text="Show Warning", command=show_warning).pack(pady=5)
tk.Button(root, text="Show Error", command=show_error).pack(pady=5)
tk.Button(root, text="Ask Question", command=ask_question).pack(pady=5)
tk.Button(root, text="Ask OK/Cancel", command=ask_ok_cancel).pack(pady=5)
tk.Button(root, text="Ask Input", command=ask_input).pack(pady=5)

root.mainloop()