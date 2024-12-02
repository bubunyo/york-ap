import tkinter as tk
from tkinter import filedialog, ttk
import datetime as dt

from date_picker import DateTimePickerRange
from table_view import TableViewWithBorders


class Gui(tk.Tk):
    def __init__(self, import_hook):
        super().__init__()

        self.import_hook = import_hook

        self.start = dt.datetime.now()
        self.end = self.start + dt.timedelta(days=30)

        self.title("Student Activity Log Analysis")
        self.minsize(1200, 500)
        self.geometry("1200x500")

        # Configure the root window grid
        self.grid_rowconfigure(1, weight=1)  # Middle row expands
        self.grid_columnconfigure(0, weight=1)

        # Top row
        self.top_frame = tk.Frame(self, height=40)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_propagate(False)

        # tabs
        notebook = ttk.Notebook(self)
        # notebook.pack(expand=True, fill="both")
        notebook.grid(row=1, column=0, sticky="nsew")

        # Create frames for tabs
        tab_merge_data = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab_merge_data, text="Tab 1")
        notebook.add(tab2, text="Tab 2")

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

        self._set_top_bar()
        self._set_bottom_bar()

        TableViewWithBorders(tab_merge_data)

    def _set_top_bar(self):
        tk.Label(self.top_frame, text="Filter by Date:").pack(side=tk.LEFT, padx=(10, 0))
        self.filter_label = tk.Label(self.top_frame)
        self.filter_label.pack(side=tk.LEFT, padx=(10, 0))

        self.filter_button = tk.Button(self.top_frame, text="Set Date Range", command=self.filter_data)
        self.filter_button.pack(padx=4, pady=2, side=tk.LEFT)
        self._set_filter_text()

        self.load_csv_button = tk.Button(self.top_frame, text="Load CSV Files", command=self.import_files)
        self.load_csv_button.pack(padx=4, pady=2, side=tk.RIGHT)

        ttk.Separator(self.top_frame, orient="vertical").pack(fill="y", padx=10, pady=8, side=tk.LEFT)

        tk.Label(self.top_frame, text="Generate Action:").pack(side=tk.LEFT)
        self.action = ttk.Combobox(self.top_frame, values=["OUTPUT STATISTICS", "GRAPHS", "CORRELATION analysis"], state="readonly", width=18)
        self.action.current(0)
        self.action.pack(side="left", padx=0, pady=0)

        self.apply_action_button = tk.Button(self.top_frame, text="Go!")
        self.apply_action_button.pack(padx=4, side=tk.LEFT, anchor=tk.N)

    def _set_bottom_bar(self):
        # Bottom row
        self.bottom_frame = tk.Frame(self, bg="white", height=50)
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")
        self.bottom_frame.grid_propagate(False)

        # Create a status bar
        frame = tk.Frame(self.bottom_frame, bg="white")
        frame.pack(fill="x")

        self.status_bar = tk.Label(frame, text="Status: Ready", bg="white", fg="black", anchor=tk.W)
        self.status_bar.grid(row=0, column=0, sticky="ew", padx=10)

        self.log_button = tk.Button(frame, text="Show Logs", highlightbackground="white")
        self.log_button.grid(row=0, column=1, pady=(0, 5), padx=5)
        frame.grid_columnconfigure(0, weight=1)

    def _set_filter_text(self):
        txt = f'{self.start.strftime("%d %b, %Y, %H:%M")} → {self.end.strftime("%d %b, %Y, %H:%M")}'
        self.filter_label.config(text=txt)

    def set_status(self, status: str):
        self.status_bar.config(text=f"Status: {status}")

    def import_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if self.import_hook is not None:
            self.import_hook(files)

    def filter_data(self):
        picker = DateTimePickerRange(self, self.start, self.end)
        picker.grab_set()
        self.wait_window(picker)
        if picker.result is not None:
            self.start, self.end = picker.result
        self._set_filter_text()

    def show_table_data(self, headers, data):
        if not isinstance(headers, tuple):
            self.set_status("improper header format")
        pass


if __name__ == "__main__":
    Gui(None).mainloop()
