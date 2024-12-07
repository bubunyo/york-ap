import tkinter as tk

_cell_width = 20
_cell_height = 30
_border_color = "dimgray"
_scrollbar_width = 16
_header_color = "grey"


class TableView:
    def __init__(self, root, header, data):

        self.container = tk.Canvas(root, highlightthickness=0)
        self.container.pack(fill="both", expand=True)

        self.header_canvas = tk.Canvas(self.container, highlightthickness=0)
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
        total_width = self._create_header(header)
        total_height = self._create_table(header, data)
        self._set_scroll_padding(total_width, total_height)

        self._set_scroll_region()

    def _create_header(self, header):
        total = 0
        x1 = 0
        for header_text, cell_width in header:
            # Draw cell border
            x2 = x1 + (cell_width * _cell_width)  # Calculate the end x-coordinate
            y1, y2 = 0, _cell_height  # Fixed height for all headers

            self.header_canvas.create_rectangle(x1, y1, x2, y2,
                                                outline=_border_color, width=1, fill=_header_color)

            # Add cell text
            self.header_canvas.create_text(
                x1 + 10, y1 + _cell_height // 2,
                text=header_text, anchor="w",
                font=("Arial", 14, "bold"),
                # fill="black",
            )

            # Update x1 for the next cell
            x1 = x2
            total += (cell_width * _cell_width)

        # Adjust scroll region to fit content
        self.header_canvas.configure(scrollregion=self.header_canvas.bbox("all"))
        return total

    def _create_table(self, header, data):

        def on_enter(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="lightblue", outline="black", width=3)

        def on_leave_even(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="white", outline="black", width=1)

        def on_leave_odd(event):
            self.body_canvas.itemconfig(event.widget.find_withtag("current"), fill="gainsboro", outline="black", width=1)

        y1 = 0  # Starting y-coordinate (below the header)
        i = 0
        total = 0

        for row in data:
            x1 = 0  # Reset x1 for each row
            for cell, (_, cell_width) in zip(row, header):
                # Calculate cell boundaries
                x2 = x1 + (cell_width * _cell_width)
                y2 = y1 + _cell_height

                color = "white" if i % 2 == 0 else "gainsboro"
                tag = "h_even" if i % 2 == 0 else "h_odd"

                self.body_canvas.create_rectangle(x1, y1, x2, y2,
                                                  outline=_border_color,
                                                  width=1, fill=color, tags=tag)

                # Add cell text
                self.body_canvas.create_text(
                    x1 + 10, y1 + _cell_height // 2,
                    text=str(cell), anchor="w",
                    fill="black",
                    # tags=tag
                )

                # Update x1 for the next cell
                x1 = x2

            # Update y1 for the next row
            y1 += _cell_height
            i += 1

        # Adjust scroll region to fit content
        self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all"))
        self.body_canvas.tag_bind("h_odd", "<Enter>", on_enter)  # Hover starts
        self.body_canvas.tag_bind("h_even", "<Enter>", on_enter)  # Hover starts
        self.body_canvas.tag_bind("h_odd", "<Leave>", on_leave_odd)
        self.body_canvas.tag_bind("h_even", "<Leave>", on_leave_even)

        return _cell_height * len(data)

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

    def _set_scroll_padding(self, width, height):

        x1 = width
        y1 = 0
        x2 = x1 + _scrollbar_width
        y2 = _cell_height

        self.header_canvas.create_rectangle(x1, y1, x2, y2, width=0)

        # add padding for scroll bars
        x1 = 0
        y1 = height
        x2 = (width) + _scrollbar_width
        y2 = y1 + _scrollbar_width
        self.body_canvas.create_rectangle(x1, y1, x2, y2, width=0)
