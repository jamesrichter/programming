import tkinter as tk


class Menu(tk.Menu):
    def __init__(self, parent, commands):
        super().__init__(parent)
        self.commands = commands
        self.cascades = {}
        for (key, value) in commands.items():
            if value[0] not in self.cascades:
                self.cascades[value[0]] = tk.Menu(self)
                self.add_cascade(label=value[0], menu=self.cascades[value[0]])
        for (key, value) in commands.items():
            if value[3] is not None:
                self.cascades[value[0]].add_command(label=key, command=value[3], accelerator=value[1])
            else:
                self.cascades[value[0]].add_separator()
        self.set_menu_state('all', 'disabled')

    def set_menu_state(self, menu, state):
        for (key, value) in self.commands.items():
            if (menu == 'all' or menu == value[0]) and value[4] is 'disableable':
                self.cascades[value[0]].entryconfigure(key, state=state)

    def set_item_state(self, command, state):
        for key in command:
            value = self.commands[key]
            self.cascades[value[0]].entryconfigure(key, state=state)
