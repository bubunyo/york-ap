import tkinter as tk
from tkinter import filedialog, ttk
import datetime as dt

from date_picker import DateTimePickerRange
from table_view import TableViewWithBorders


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.start = dt.datetime.now()
        self.end = self.start + dt.timedelta(days=30)

        self.title("Log Activity Analysis")
        self.geometry("1200x500")

        # Configure the root window grid
        self.grid_rowconfigure(1, weight=1)  # Middle row expands
        self.grid_columnconfigure(0, weight=1)

        # Top row
        self.top_frame = tk.Frame(self, height=40)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_propagate(False)

        # Middle row
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        # Bottom row
        self.bottom_frame = tk.Frame(self, bg="white", height=50)
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")
        self.bottom_frame.grid_propagate(False)

        self.filter_button = tk.Button(self.top_frame,
                                       highlightthickness=2,
                                       command=self.filter_data)
        self.filter_button.pack(padx=4, pady=2, side=tk.LEFT)

        self._set_filter_text()

        # Create a status bar
        frame = tk.Frame(self.bottom_frame)
        self.status_bar = tk.Label(frame, text="Status: Ready", anchor=tk.W, bg="white", fg="black")
        self.status_bar.pack(fill=tk.X)
        frame.pack(fill=tk.X, padx=5, pady=5)

        TableViewWithBorders(self.main_frame)

    def _set_filter_text(self):
        txt = f'{self.start.strftime("%d %b, %Y, %H:%M")} → {self.end.strftime("%d %b, %Y, %H:%M")}'
        self.filter_button.config(text=txt)

    def set_status(self, status: str):
        self.status_bar.config(text=f"Status: {status}")

    @staticmethod
    def import_files():
        return filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

    def filter_data(self):
        picker = DateTimePickerRange(self, self.start, self.end)
        picker.grab_set()
        self.wait_window(picker)
        if picker.result is not None:
            self.start, self.end = picker.result
        self._set_filter_text()


if __name__ == "__main__":
    a = App()
    a.mainloop()
