from tkinter import ttk


class Scroller(ttk.Scrollbar):  # tk.Scrollbar undesirably responds to touch scrolling, so ttk.Scrollbar
    # automatically hide when not needed
    def set(self, lo, hi):
        if float(lo) <= 0 and 1 <= float(hi):
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)
