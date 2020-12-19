import tkinter as tk

from drawer import Drawer
from stacker import Stacker
from menu import Menu
from utility import app_name


# todo: type-hints
class Annotator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.drawer = Drawer(self)
        self.stacker = Stacker(self)
        self.template_drawer = Drawer(self)
        self.commands = None
        self.bind_events()
        self.menu = Menu(self, self.commands)
        self.set_title(app_name)
        self.geometry('1200x920')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.stacker.grid(row=0, column=1, sticky=tk.NS)
        self.drawer.grid(row=0, column=0, sticky=tk.NSEW)
        self.template_drawer.grid(row=0, column=2, sticky=tk.NSEW)
        self.configure(menu=self.menu)

        self.filename = None
        self.update()
        self.open()

    def bind_events(self):
        commands = {'Open': ['File', 'Ctrl+O', '<Control-o>', self.open, ''],
                    'Close': ['File', 'Ctrl+W', '<Control-w>', self.close, 'disableable'],
                    'Divider1': ['File', '', '', None, None],
                    'Save': ['File', 'Ctrl+S', '<Control-s>', self.save, 'disableable'],
                    'Divider2': ['File', '', '', None, None],
                    'Quit': ['File', 'Ctrl+Q', '<Control-q>', self.quit, ''],
                    'Toggle Draw Type': ['Draw', 'Ctrl+T', '<Control-t>', self.toggle_draw, 'disableable'],
                    'Divider3': ['Draw', '', '', None, None],
                    'Clear Mask': ['Draw', 'Ctrl+X', '<Control-x>', self.clear_mask, 'disableable'],
                    'Delete Last': ['Draw', 'Ctrl+Z', '<Control-z>', self.delete_last, 'disableable'],
                    'Divider4': ['Draw', '', '', None, None],
                    'Up': ['Draw', '', '<Up>', self.previous_page, 'disableable'],  # previous page of stack
                    'Down': ['Draw', '', '<Down>', self.next_page, 'disableable'],  # next page of stack
                    }
        for (key, value) in commands.items():
            if value[3] is not None:
                self.bind(value[2], value[3])
        self.commands = commands

    def open(self, event=None):
        if self.drawer.open():
            self.menu.set_menu_state('all', 'normal')
            # self.stacker.show(self.drawer.npimages)
            self.goto_page(0)

    def close(self, event=None):
        if not self.drawer.close():
            return False
        self.menu.set_menu_state('all', 'disable')
        self.stacker.close()
        return True

    def clear_mask(self, event=None):
        self.drawer.clear_mask()

    def save(self, event=None):
        self.drawer.save_mask()

    def quit(self, event=None):
        if self.close():
            super().quit()

    def delete_last(self, event=None):
        self.drawer.delete_last()

    def toggle_draw(self, event=None):
        self.drawer.toggle_draw()

    def set_title(self, title):
        self.title(title)

    def next_page(self, event=None):
        self.drawer.next_page(event)

    def previous_page(self, event=None):
        self.drawer.previous_page(event)

    def goto_page(self, page):
        if self.drawer.has_images():
            self.drawer.goto(page)
            # self.stacker.highlight(page)


annotator = Annotator()
annotator.mainloop()
# a = tk.Tk()
# Drawer(a).pack()
# a.mainloop()
