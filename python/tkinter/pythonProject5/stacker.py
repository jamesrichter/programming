import tkinter as tk
from PIL import Image, ImageTk
import warnings

from utility import *


class Stacker(tk.Frame):
    def __init__(self, parent):
        bg = 'lightgray'
        super().__init__(bg=bg)
        self.uid_cnt = 0
        self.uids = []
        self.width = 80
        self.margin = 4
        self.marker_width = 10
        self.highlighted = 0
        self.gallery = tk.Canvas(self, highlightthickness=0, bg=bg, width=self.width)
        self.marker = tk.Canvas(self, highlightthickness=0, bg=bg, width=self.marker_width, height=self.marker_width)
        self.parent = parent
        self.thumbnail_size = (self.width - 2 * self.margin, self.width - 2 * self.margin)
        self.npimage = None
        self.tops = None
        self.scale = tk.Scale(self, to=0, showvalue=0,
                              command=lambda x: self.parent.goto_page(int(x)) if self.npimage is not None else None)
        self.marker.grid(row=0, column=0)
        self.gallery.grid(row=0, column=1, sticky=tk.NS)
        self.scale.grid(row=0, column=2, sticky=tk.NS)
        self.grid_rowconfigure(0, weight=1)
        # self.scale.grid_remove()
        # self.update()
        self.bind('<Configure>', lambda x: self.highlight(self.highlighted))

    def uid(self):
        self.uid_cnt += 1
        return uid + str(self.uid_cnt)

    def show(self, npimage1):
        self.npimage = []
        self.uids = []
        self.tops = [0]
        self.marker.create_oval((1, 1, self.marker_width - 2, self.marker_width - 2),
                                outline='', fill='green', tag=tag_marker)
        for idx, path in enumerate(images):
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                image = Image.open(path)
            image.thumbnail(self.thumbnail_size)
            self.npimage.append(ImageTk.PhotoImage(Image.fromarray(np.uint8(npimage1))))
            self.uids.append(self.uid())
            self.tops.append(self.tops[-1] + self.npimage[-1].height() + 2 * self.margin)
            self.gallery.create_rectangle((0, self.tops[-2], self.width, self.tops[-1]),
                                          outline='', fill='', tags=(self.uids[-1], tag_highlighter))
            self.gallery.create_image((self.margin, self.tops[-2] + self.margin), anchor='nw', image=self.npimage[-1],
                                      tags=(self.uids[-1], tag_thumbnail))
            self.gallery.tag_bind(self.uids[-1] + '&&' + tag_thumbnail, '<1>',
                                  lambda x, the_idx=idx: self.parent.goto_page(the_idx))
        self.gallery.configure(height=self.tops[-1] + self.margin, scrollregion=(0, 0, 0, self.tops[-1]))
        self.scale.config(to=len(self.npimage) - 1)
        # self.canvas.update()

    def close(self):
        self.gallery.delete('all')
        self.marker.delete('all')
        self.npimage = None
        self.scale.config(to=0)
        # self.scale.grid_remove()

    def highlight(self, page):
        if self.npimage is not None and page is not None:
            self.highlighted = page
            self.scale.set(self.highlighted)
            _, t, _, b = self.marker.bbox(tag_marker)
            m = (self.marker.canvasy(t) + self.marker.canvasy(b)) / 2
            ym = int(self.marker.winfo_y() + m)
            _, t, _, b = self.gallery.bbox(self.uids[page] + '&&' + tag_thumbnail)
            g = (self.gallery.canvasy(t) + self.gallery.canvasy(b)) / 2
            yg = int(self.gallery.winfo_y() + g)
            self.gallery.move('all', 0, ym - yg)
