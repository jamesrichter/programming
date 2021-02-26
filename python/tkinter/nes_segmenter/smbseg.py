  

from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from scipy import ndimage


class Segmenter:

    def __init__():
        self.root = Tk()
        self.object_pixels = set()
        self.subobjects = []
        self.subself.object_pixels = set()
        array = np.load("2small.npy")[0]
        print(array.dtype)
        self.img_zoom = 4
        self.img_size = (240*self.img_zoom, 224*self.img_zoom)
        img = ImageTk.PhotoImage(image=Image.fromarray(array).resize(self.img_size))
        canvas_width = self.img_size[0]
        canvas_height = self.img_size[1]
        self.canvas = Canvas(self.root, 
                        width=canvas_width,
                        height=canvas_height)

        images = []  # to hold the newly created image

        scrollbar = Scrollbar(self.root, command=canvas.yview)
        scrollbar.grid(row=0, column=1, rowspan=2)
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.grid(row=0,column=0, rowspan=2, sticky='ns')
        canvas.create_image(0, 0, anchor='nw', image=img)
        checkered(canvas,4)
        button_start_big_object = Button(self.root, text='Start Big Object')
        button_end_big_object = Button(self.root, text='End Big Object')
        button_start_sub_object = Button(self.root, text='Start Sub Object')
        button_end_sub_object = Button(self.root, text='End Sub Object')
        button_start_big_object.grid(row=0, column=2)
        button_end_big_object.grid(row=0, column=3)
        button_start_sub_object.grid(row=1, column=2)
        button_end_sub_object.grid(row=1, column=3)

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind("<B1-Motion>", callback_square)
        canvas.bind("<B3-Motion>", callback_erase)
        canvas.bind("<Button-1>", callback_square)
        canvas.bind("<Button-3>", callback_erase)    
    def checkered(canvas, line_distance):
       # vertical lines at an interval of "line_distance" pixel
       for x in range(line_distance,canvas_width,line_distance):
          canvas.create_line(x, 0, x, canvas_height, fill="#476042")
       # horizontal lines at an interval of "line_distance" pixel
       for y in range(line_distance,canvas_height,line_distance):
          canvas.create_line(0, y, canvas_width, y, fill="#476042")

    def create_rectangle(x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (int(x2-x1), int(y2-y1)), fill)
            images.append(ImageTk.PhotoImage(image))
            canvas.create_image(x1, y1, image=images[-1], anchor='nw')
        canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def _bound_to_mousewheel(self, event):
        canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        canvas.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        canvas.yview_scroll(int(-1*(event.delta/300)), "units")


    def callback_square(event):
        print("held motion at", canvas.canvasx(event.x), canvas.canvasy(event.y))
        cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
        bx0 = (cx//self.img_zoom)*self.img_zoom
        bx1 = bx0 + self.img_zoom
        by0 = (cy//self.img_zoom)*self.img_zoom
        by1 = by0 + self.img_zoom
        if (cx//self.img_zoom, cy//self.img_zoom) not in self.object_pixels:
            create_rectangle(bx0, by0, bx1, by1, outline='red', fill='red', alpha=.3)
            self.object_pixels.add((cx//self.img_zoom, cy//self.img_zoom))
        print(self.object_pixels)
    def callback_erase(event):
        print("held motion at", canvas.canvasx(event.x), canvas.canvasy(event.y))
        cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
        bx0 = (cx//self.img_zoom)*self.img_zoom
        bx1 = bx0 + self.img_zoom
        by0 = (cy//self.img_zoom)*self.img_zoom
        by1 = by0 + self.img_zoom
        if (cx//self.img_zoom, cy//self.img_zoom) in self.object_pixels:
            create_rectangle(bx0, by0, bx1, by1, outline='black', fill='black', alpha=.3)
            self.object_pixels.remove((cx//self.img_zoom, cy//self.img_zoom))
        # subobject pixels


    mainloop()

    np_array_index_dict = {}
    mask_array_index_dict = {}

    def find_template_in_image(image, template, mask):
        res = cv2.matchTemplate(image.astype(np.uint8), 
                                template.astype(np.uint8), 
                                cv2.TM_CCORR_NORMED, 
                                mask=mask)
        return res == 1

    def add_template(image, mask,):
        img = array
        index = img.tobytes()
        np_array_index_dict[index] = image
        mask_array_index_dict[index] = mask

    def mask_from_coords(coords):
        shape_mask = (image.shape[0], image.shape[1])
        new_mask = np.zeros(shape_mask)
        for x in coords:
            new_mask[coords] = 1
        return new_mask
