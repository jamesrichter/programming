import csv
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import warnings

from scroller import Scroller
from utility import *


# todo: place the image in the middle when it is smaller
# base class for drawer
# load the images
class Container(tk.Frame):
    def __init__(self, parent, width=None, height=None):
        super().__init__()
        self.parent = parent
        if width==None:
            self.canvas = tk.Canvas(self, highlightthickness=0, width=96, height=896, bg='blue')  # , scrollregion=(0,0,1000,1500))
        else:
            self.canvas = tk.Canvas(self,
                                    highlightthickness=0, width=width, height=height, bg='black')
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.canvas.config()
        self.uid_cnt = 0
        self.page = None
        self.npimages = None
        self.stack = None
        self.image = None
        self.has_edf = None
        self.bind('<Configure>', lambda x: self.canvas.update())  # for smooth resize when maximized

    def uid(self):
        self.uid_cnt += 1
        return uid + str(self.uid_cnt)

    def has_images(self):
        return self.npimages is not None

    def has_page(self):
        return self.page is not None

    def get_file(self):
        if self.has_page() and not self.close():
            return None
        path = tk.filedialog.askopenfilename(title='Select a Stack', parent=self.parent)
        return path if path != '' else None

    def open(self):
        path = self.get_file()
        if path is None:
            return False
        # path = '/Users/adrian/PycharmProjects/Images/frame000_stack'
        if is_numpy_file(path):
            self.npimages = np.load(path)
        if len(self.npimages) == 0:
            tk.messagebox.showwarning('No Image', 'There are no compatible images in the folder', parent=self.parent)
            return False
        self.parent.goto_page(0)
        return True

    def close(self):
        self.canvas.delete(tag_image)
        self.canvas.delete(tag_marker)
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        self.npimages = None
        self.image = None
        self.page = None
        self.parent.set_title(app_name)
        return True

    def goto(self, page):
        # load the image
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self.image = ImageTk.PhotoImage(Image.fromarray(np.uint8(self.npimages[page])).resize((960,896), Image.NEAREST))
        # show the image
        self.canvas.delete(tag_image)
        self.canvas.create_image((0, 0), anchor='nw', image=self.image, tags=(self.uid(), tag_image, tag_background))
        self.canvas.tag_lower(tag_image)
        self.page = page
        self.canvas.config(scrollregion=(0, 0, self.image.width(), self.image.height()))

    def show_csv(self, path):
        if path != '':
            with open(path, newline='') as f:
                reader = csv.reader(f)
                for e in reader:
                    x, y = int(e[0]), int(e[1])
                    x, y = y, x  # todo: check this
                    self.canvas.create_oval(x - marker_radius, y - marker_radius, x + marker_radius, y + marker_radius,
                                            tags=(self.uid(), tag_marker, tag_back), width=0, fill=color_fill_marker)

    def on_image(self, point):
        return (self.has_page() and
                0 <= point[0] < self.image.width() and
                0 <= point[1] < self.image.height())

    def next_page(self, event):
        if self.page + 1 < len(self.npimages):
            self.parent.goto_page(self.page + 1)

    def previous_page(self, event):
        if self.page - 1 >= 0:
            self.parent.goto_page(self.page - 1)
