import calendar
import tkinter as tk
from tkinter import ttk
import datetime as dt


def generate_minute():
    return [f'{i:>02}' for i in range(0, 60)]


def generate_day():
    """Generate a list of date values for the next 30 days."""
    return [f'{i}' for i in range(1, 31)]


def generate_month():
    """Generate a list of date values for the next 30 days."""
    return list(calendar.month_name[1:])


def generate_year():
    """Generate a list of date values for the next 30 days."""
    return [f'{i}' for i in range(1990, 2032)]


def generate_hour():
    return [f'{i:>02}' for i in range(0, 24)]


class DateTimePickerRange(tk.Toplevel):
    start_date = dt.datetime.now()
    end_date = start_date + dt.timedelta(days=30)

    def __init__(self, parent, start_date, end_date):
        super().__init__(parent)
        self.result = None
        self.start_date = start_date
        self.end_date = end_date
        self.title("Date and Time Filter")
        self.geometry("540x240")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        start_box_frame = tk.LabelFrame(self.main_frame, text="Start Date & Time",
                                        bd=2, relief="solid")
        start_box_frame.pack(fill="x", pady=5)

        # Start date and time (aligned horizontally)
        start_frame = tk.Frame(start_box_frame)
        start_frame.pack(fill="x", pady=15)

        self.start_day_combo = ttk.Combobox(start_frame, values=generate_day(), state="readonly", width=3)
        self.start_day_combo.pack(side="left", padx=5)
        self.start_day_combo.set(self.start_date.date().day)

        self.start_month_combo = ttk.Combobox(start_frame, values=generate_month(), state="readonly", width=8)
        self.start_month_combo.pack(side="left", padx=5)
        self.start_month_combo.set(calendar.month_name[self.start_date.month])

        self.start_year_combo = ttk.Combobox(start_frame, values=generate_year(), state="readonly", width=4)
        self.start_year_combo.pack(side="left", padx=5)
        self.start_year_combo.set(self.start_date.year)

        tk.Frame(start_frame, width=30).pack(side="left")

        tk.Label(start_frame, text="Start Time:").pack(side="left", padx=5)

        self.start_hour_combo = ttk.Combobox(start_frame, values=generate_hour(), state="readonly", width=4)
        self.start_hour_combo.pack(side="left", padx=5)
        self.start_hour_combo.set(f'{self.start_date.hour:>02}')

        self.start_minute_combo = ttk.Combobox(start_frame, values=generate_minute(), state="readonly", width=4)
        self.start_minute_combo.pack(side="left", padx=5)
        self.start_minute_combo.set(f'{self.start_date.minute:>02}')

        end_box_frame = tk.LabelFrame(self.main_frame, text="End Date & Time",
                                      borderwidth=2, relief="solid",
                                      highlightbackground="lightgrey",
                                      highlightcolor="lightgrey")
        end_box_frame.pack(fill="x", pady=5)

        # Start date and time (aligned horizontally)
        end_frame = tk.Frame(end_box_frame)
        end_frame.pack(fill="x", pady=15)

        self.end_day_combo = ttk.Combobox(end_frame, values=generate_day(), state="readonly", width=3)
        self.end_day_combo.pack(side="left", padx=5)
        self.end_day_combo.set(self.end_date.date().day)

        self.end_month_combo = ttk.Combobox(end_frame, values=generate_month(), state="readonly", width=8)
        self.end_month_combo.pack(side="left", padx=5)
        self.end_month_combo.set(calendar.month_name[self.end_date.month])

        self.end_year_combo = ttk.Combobox(end_frame, values=generate_year(), state="readonly", width=4)
        self.end_year_combo.pack(side="left", padx=5)
        self.end_year_combo.set(self.end_date.year)

        tk.Frame(end_frame, width=30).pack(side="left")

        tk.Label(end_frame, text="End Time:").pack(side="left", padx=5)

        self.end_hour_combo = ttk.Combobox(end_frame, values=generate_hour(), state="readonly", width=4)
        self.end_hour_combo.pack(side="left", padx=5)
        self.end_hour_combo.set(f'{self.end_date.hour:>02}')

        self.end_minute_combo = ttk.Combobox(end_frame, values=generate_minute(), state="readonly", width=4)
        self.end_minute_combo.pack(side="left", padx=5)
        self.end_minute_combo.set(f'{self.end_date.minute:>02}')

        # Submit button (aligned to bottom-right)
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10, anchor="se")

        submit_button = tk.Button(self.button_frame, text="Apply",
                                  command=self.on_ok)

        submit_button.pack(side="right")

        cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="right")

    def on_ok(self):
        s_day = self.start_day_combo.current() + 1
        s_month = self.start_month_combo.current() + 1
        s_year = self.start_year_combo.get()
        s_hour = self.start_hour_combo.current()
        s_minute = self.start_minute_combo.current()

        e_day = self.end_day_combo.current() + 1
        e_month = self.end_month_combo.current() + 1
        e_year = self.end_year_combo.get()
        e_hour = self.end_hour_combo.current()
        e_minute = self.end_minute_combo.current()

        self.start_date = dt.datetime(int(s_year), s_month, s_day, s_hour, s_minute, 0, 0)
        self.end_date = dt.datetime(int(e_year), e_month, e_day, e_hour, e_minute, 0, 0)

        self.result = (self.start_date, self.end_date)  # Capture the input
        self.destroy()  # Close the window

    def on_cancel(self):
        self.result = None  # No result (canceled)
        self.destroy()  # Close the window
