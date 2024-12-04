import tkinter as tk
from tkinter import filedialog, ttk
import datetime as dt

from date_picker import DateTimePickerRange
from table_view import TableViewWithBorders


class Gui(tk.Tk):
    def __init__(self, import_hook, check, apply_filter):
        super().__init__()

        self.loading_dialog = None
        self.import_hook = import_hook
        self.check = check
        self.apply_filter = apply_filter

        self.start = None
        self.end = None

        self.title("Student Activity Log Analysis")
        self.minsize(1200, 200)
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
        notebook.grid(row=1, column=0, sticky="nsew")

        # Create frames for tabs
        self.tab_merge_data = ttk.Frame(notebook)
        self.tab_pivot_data_month = ttk.Frame(notebook)
        self.tab_pivot_data_total = ttk.Frame(notebook)
        self.tab_stats_month = ttk.Frame(notebook)
        self.tab_stats_year = ttk.Frame(notebook)
        self.tab_corr = ttk.Frame(notebook)
        self.tab_graphs = ttk.Frame(notebook)

        notebook.add(self.tab_merge_data, text="Merged Data")
        notebook.add(self.tab_pivot_data_month, text="Pivot Data (Monthly)")
        notebook.add(self.tab_stats_month, text="Statistics (Monthly)")
        notebook.add(self.tab_pivot_data_total, text="Pivot Data (Total)")
        notebook.add(self.tab_stats_year, text="Statistics (Total)")
        notebook.add(self.tab_corr, text="Correlation Matrix")
        notebook.add(self.tab_graphs, text="Correlation Graphs")

        self._set_top_bar()
        self.after_idle(self._on_start)

    def _on_start(self):
        if self.check():
            self.apply_filter()
            self.load_csv_button.destroy()
            self.load_csv_button = None

    @staticmethod
    def _clear_frame(frame):
        # Iterate through all widgets in the frame and destroy them
        for widget in frame.winfo_children():
            widget.destroy()

    def show_merge_data(self, header, data):
        if self.load_csv_button:
           self.load_csv_button.destroy()
        self._clear_frame(self.tab_merge_data)
        TableViewWithBorders(self.tab_merge_data, header, data)

    def show_pivot_data_month(self, header, data):
        self._clear_frame(self.tab_pivot_data_month)
        TableViewWithBorders(self.tab_pivot_data_month, header, data)

    def show_pivot_data_total(self, header, data):
        self._clear_frame(self.tab_pivot_data_total)
        TableViewWithBorders(self.tab_pivot_data_total, header, data)

    def show_stats_month(self, header, data):
        self._clear_frame(self.tab_stats_month)
        TableViewWithBorders(self.tab_stats_month, header, data)

    def show_stats_year(self, header, data):
        self._clear_frame(self.tab_stats_year)
        TableViewWithBorders(self.tab_stats_year, header, data)

    def show_corr(self, header, data):
        self._clear_frame(self.tab_corr)
        TableViewWithBorders(self.tab_corr, header, data)

    def show_graphs(self, header, data):
        # self._clear_frame(self.tab_graph)
        # TableViewWithBorders(tab_graph)
        pass

    def _set_top_bar(self):
        tk.Label(self.top_frame, text="Filter by Date:").pack(side=tk.LEFT, padx=(10, 0))
        self.filter_label = tk.Label(self.top_frame)
        self.filter_label.pack(side=tk.LEFT, padx=(10, 0))

        self.filter_button = tk.Button(self.top_frame, text="Apply Date Range", command=self.filter_data)
        self.filter_button.pack(padx=4, pady=2, side=tk.LEFT)
        self._set_filter_text()

        self.load_csv_button = tk.Button(self.top_frame, text="Load CSV Files", command=self.import_files)
        self.load_csv_button.pack(padx=4, pady=2, side=tk.RIGHT)

        ttk.Separator(self.top_frame, orient="vertical").pack(fill="y", padx=10, pady=8, side=tk.LEFT)

    def _set_filter_text(self):
        if self.start and self.end:
            txt = f'{self.start.strftime("%d %b, %Y, %H:%M")} → {self.end.strftime("%d %b, %Y, %H:%M")}'
            self.filter_label.config(text=txt)

    def set_status(self, status: str):
        self.toggle_loading_dialog(False)

        message = f"Message\n\n{status}"
        dialog = tk.Toplevel(self)
        dialog.title("Status Message")
        dialog.geometry("300x100")
        dialog.resizable(False, False)

        dialog.transient(self)
        dialog.grab_set()

        # Add a label with the loading message
        label = tk.Label(dialog, text=message, font=("Arial", 12))
        label.pack(pady=20)

        # Center the loading dialog on the screen
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 50
        dialog.geometry(f"+{x}+{y}")

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
        self.apply_filter(self.start, self.end)

    def show_table_data(self, headers, data):
        if not isinstance(headers, tuple):
            self.set_status("improper header format")

    def set_dates(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        self._set_filter_text()

    def toggle_loading_dialog(self, show=False):
        if show:
            message = "Loading and transforming data.\nPlease wait..."
            self.loading_dialog = tk.Toplevel(self)
            self.loading_dialog.title("Loading")
            self.loading_dialog.geometry("300x100")
            self.loading_dialog.resizable(False, False)

            self.loading_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

            # Disable interactions with the main window
            self.loading_dialog.transient(self)
            self.loading_dialog.grab_set()

            # Add a label with the loading message
            label = tk.Label(self.loading_dialog, text=message, font=("Arial", 12))
            label.pack(pady=20)

            # Center the loading dialog on the screen
            x = self.winfo_x() + (self.winfo_width() // 2) - 150
            y = self.winfo_y() + (self.winfo_height() // 2) - 50
            self.loading_dialog.geometry(f"+{x}+{y}")
            # self.update()
            self.update_idletasks()
        else:
            if self.loading_dialog:
                self.loading_dialog.destroy()
                self.loading_dialog = None
