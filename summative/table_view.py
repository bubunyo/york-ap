import tkinter as tk

_cell_width = 100
_cell_height = 30
_border_color = "dimgray"
_scrollbar_width = 16
_header_color = "grey"


class TableViewWithBorders:
    def __init__(self, root):

        self.container = tk.Canvas(root, highlightthickness=0)
        self.container.pack(fill="both", expand=True)

        self.header_canvas = tk.Canvas(self.container, highlightthickness=0, background="black")
        self.header_canvas.configure(height=_cell_height)
        self.header_canvas.pack(fill="x")

        self.body_canvas = tk.Canvas(self.container, highlightthickness=0)
        self.body_canvas.pack(fill="both", expand=True)

        # Scrollbars
        self.v_scroll = tk.Scrollbar(self.body_canvas, orient="vertical", command=self.body_canvas.yview)
        self.h_scroll = tk.Scrollbar(self.body_canvas, orient="horizontal", command=self.sync_scroll)

        self.body_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.header_canvas.configure(xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        # Create table
        rows = 500
        cols = 50
        self._create_header(cols)
        self._create_table(rows, cols)
        self._set_scroll_padding(rows, cols)

        self._set_scroll_region()

    def _set_scroll_region(self):
        self.body_canvas.bind('<Configure>', self.update)
        self.bind_mouse_scroll(self.body_canvas, self.y_scroll)
        self.bind_mouse_scroll(self.h_scroll, self.x_scroll)
        self.bind_mouse_scroll(self.v_scroll, self.y_scroll)

        self.body_canvas.focus_set()

    def bind_mouse_scroll(self, parent, mode):
        # ~~ Windows only
        parent.bind("<MouseWheel>", mode)
        # ~~ Mac Horizontal Scroll
        parent.bind("<Shift-MouseWheel>", mode)
        # ~~ Unix only
        parent.bind("<Button-4>", mode)
        parent.bind("<Button-5>", mode)

    def y_scroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.body_canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.body_canvas.yview_scroll(-1, "unit")

    def x_scroll(self, event):
        if event.num == 5 or event.delta < 0:
            self.body_canvas.xview_scroll(1, "unit")
            self.header_canvas.xview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.body_canvas.xview_scroll(-1, "unit")
            self.header_canvas.xview_scroll(-1, "unit")

    def update(self, event):
        self.body_canvas.config(scrollregion=self.body_canvas.bbox('all'))
        self.header_canvas.config(scrollregion=self.header_canvas.bbox('all'))

    def sync_scroll(self, *args):
        """Sync scroll position for both canvases."""
        self.body_canvas.xview(*args)
        self.header_canvas.xview(*args)

    def _create_header(self, cols):
        for j in range(cols):
            # Draw cell border
            x1 = j * _cell_width
            y1 = 0
            x2 = x1 + _cell_width
            y2 = y1 + _cell_height

            self.header_canvas.create_rectangle(x1, y1, x2, y2, outline=_border_color, width=1, fill=_header_color)

            # Add cell text
            self.header_canvas.create_text(
                x1 + 10, y1 + _cell_height // 2,
                text=f"Header {j}", anchor="w",
                fill="black",
            )

        # Adjust scroll region to fit content
        self.header_canvas.configure(scrollregion=self.header_canvas.bbox("all"))

    def _create_table(self, rows, cols):

        def on_enter(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="lightblue", outline="black", width=3)

        def on_leave_even(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="white", outline="black", width=1)

        def on_leave_odd(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="gainsboro", outline="black", width=1)

        for i in range(rows):
            for j in range(cols):
                # Draw cell border
                x1 = j * _cell_width
                y1 = i * _cell_height
                x2 = x1 + _cell_width
                y2 = y1 + _cell_height

                color = "white" if i % 2 == 0 else "gainsboro"
                tag = "h_even" if i % 2 == 0 else "h_odd"

                self.body_canvas.create_rectangle(x1, y1, x2, y2, outline=_border_color,
                                                  width=1, fill=color, tags=tag)

                # Add cell text
                self.body_canvas.create_text(
                    x1 + 10, y1 + _cell_height // 2,
                    text=f"R{i}C{j}", anchor="w",
                    fill="black",
                    # tags=tag
                )

        # Adjust scroll region to fit content
        self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all"))
        self.body_canvas.tag_bind("h_odd", "<Enter>", on_enter)  # Hover starts
        self.body_canvas.tag_bind("h_even", "<Enter>", on_enter)  # Hover starts
        self.body_canvas.tag_bind("h_odd", "<Leave>", on_leave_odd)
        self.body_canvas.tag_bind("h_even", "<Leave>", on_leave_even)

    def _set_scroll_padding(self, rows, cols):

        x1 = cols * _cell_width
        y1 = 0
        x2 = x1 + _scrollbar_width
        y2 = _cell_height

        self.header_canvas.create_rectangle(x1, y1, x2, y2, width=0, fill=_header_color)

        # add padding for scroll bars
        x1 = 0
        y1 = rows * _cell_height
        x2 = (cols * _cell_width) + _scrollbar_width
        y2 = y1 + _scrollbar_width
        self.body_canvas.create_rectangle(x1, y1, x2, y2, width=0)
