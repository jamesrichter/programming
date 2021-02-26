from tkinter import Tk, Label, Button, Canvas

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.C = Canvas(master, 
                   width=100,
                   height=100)
        self.C.pack()
        self.rect = self.C.create_rectangle(1,1,4,4, fill="green", stipple='gray50')

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()  





# from tkinter import Tk, Label, Button, StringVar

# class MyFirstGUI:
#     LABEL_TEXT = [
#         "This is our first GUI!",
#         "Actually, this is our second GUI.",
#         "We made it more interesting...",
#         "...by making this label interactive.",
#         "Go on, click on it again.",
#     ]
#     def __init__(self, master):
#         self.master = master
#         master.title("A simple GUI")

#         self.label_index = 0
#         self.label_text = StringVar()
#         self.label_text.set(self.LABEL_TEXT[self.label_index])
#         self.label = Label(master, textvariable=self.label_text)
#         self.label.bind("<Button-1>", self.cycle_label_text)
#         self.label.pack()

#         self.greet_button = Button(master, text="Greet", command=self.greet)
#         self.greet_button.pack()

#         self.close_button = Button(master, text="Close", command=master.quit)
#         self.close_button.pack()

#     def greet(self):
#         print("Greetings!")

#     def cycle_label_text(self, event):
#         self.label_index += 1
#         self.label_index %= len(self.LABEL_TEXT) # wrap around
#         self.label_text.set(self.LABEL_TEXT[self.label_index])

# root = Tk()
# my_gui = MyFirstGUI(root)
# root.mainloop()


# ~~~~~~~~~~

# from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E

# class Calculator:

#     def __init__(self, master):
#         self.master = master
#         master.title("Calculator")

#         self.total = 0
#         self.entered_number = 0

#         self.total_label_text = IntVar()
#         self.total_label_text.set(self.total)
#         self.total_label = Label(master, textvariable=self.total_label_text)

#         self.label = Label(master, text="Total:")

#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         self.add_button = Button(master, text="+", command=lambda: self.update("add"))
#         self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
#         self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

#         # LAYOUT

#         self.label.grid(row=0, column=0, sticky=W)
#         self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

#         self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

#         self.add_button.grid(row=2, column=0)
#         self.subtract_button.grid(row=2, column=1)
#         self.reset_button.grid(row=2, column=2, sticky=W+E)

#     def validate(self, new_text):
#         if not new_text: # the field is being cleared
#             self.entered_number = 0
#             return True

#         try:
#             self.entered_number = int(new_text)
#             return True
#         except ValueError:
#             return False

#     def update(self, method):
#         if method == "add":
#             self.total += self.entered_number
#         elif method == "subtract":
#             self.total -= self.entered_number
#         else: # reset
#             self.total = 0

#         self.total_label_text.set(self.total)
#         self.entry.delete(0, END)

# root = Tk()
# my_gui = Calculator(root)
# root.mainloop()

# ~~~~~~~~~

# import random
# from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E

# class GuessingGame:
#     def __init__(self, master):
#         self.master = master
#         master.title("Guessing Game")

#         self.secret_number = random.randint(1, 100)
#         self.guess = None
#         self.num_guesses = 0

#         self.message = "Guess a number from 1 to 100"
#         self.label_text = StringVar()
#         self.label_text.set(self.message)
#         self.label = Label(master, textvariable=self.label_text)

#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         self.guess_button = Button(master, text="Guess", command=self.guess_number)
#         self.reset_button = Button(master, text="Play again", command=self.reset, state=DISABLED)

#         self.label.grid(row=0, column=0, columnspan=2, sticky=W+E)
#         self.entry.grid(row=1, column=0, columnspan=2, sticky=W+E)
#         self.guess_button.grid(row=2, column=0)
#         self.reset_button.grid(row=2, column=1)

#     def validate(self, new_text):
#         if not new_text: # the field is being cleared
#             self.guess = None
#             return True

#         try:
#             guess = int(new_text)
#             if 1 <= guess <= 100:
#                 self.guess = guess
#                 return True
#             else:
#                 return False
#         except ValueError:
#             return False

#     def guess_number(self):
#         self.num_guesses += 1

#         if self.guess is None:
#             self.message = "Guess a number from 1 to 100"

#         elif self.guess == self.secret_number:
#             suffix = '' if self.num_guesses == 1 else 'es'
#             self.message = "Congratulations! You guessed the number after %d guess%s." % (self.num_guesses, suffix)
#             self.guess_button.configure(state=DISABLED)
#             self.reset_button.configure(state=NORMAL)

#         elif self.guess < self.secret_number:
#             self.message = "Too low! Guess again!"
#         else:
#             self.message = "Too high! Guess again!"

#         self.label_text.set(self.message)

#     def reset(self):
#         self.entry.delete(0, END)
#         self.secret_number = random.randint(1, 100)
#         self.guess = 0
#         self.num_guesses = 0

#         self.message = "Guess a number from 1 to 100"
#         self.label_text.set(self.message)

#         self.guess_button.configure(state=NORMAL)
#         self.reset_button.configure(state=DISABLED)

# root = Tk()
# my_gui = GuessingGame(root)
# root.mainloop()
