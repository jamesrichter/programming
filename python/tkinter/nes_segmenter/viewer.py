from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from scipy import ndimage
import cv2
import os
import itertools
# idea corner
# /////
# maybe a structure that keeps track of guides/objs hierarchically
# like, the ability to scroll between different guides, drill down,
# then scroll between different objs within those guides
# ////
# ////
# the gradient space is like a deep, dark forest...
# and it's your job to make sure there is a path from every random place in the forest
# ////

class Viewer():
    def __init__(self, root):
        self.root = root
        self.loaded_templates = []
        self.load_templates()

        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.selected_pixels = set()
        self.object_mask = []
        self.object_pixels = set()
        self.guide_mask = []
        self.guide_pixels = set()
        self.all_rects = []
        self.current_object_index = 0
        # load + zoom image
        self.array = np.load("2small.npy")[0]
        self.img_zoom = 2
        self.img_size = (240*self.img_zoom, 224*self.img_zoom)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.array).resize(self.img_size))

        # add scroll bar

        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = Canvas(self.frame1, 
                   width=self.canvas_width,
                   height=self.canvas_height)

        # print the image of smb

        self.images = []  # to hold the newly created image



        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.grid(row=0,column=0, sticky='ns')
        self.canvas.create_image(0, 0, anchor='nw', image=self.img)
        self.button_start_big_object = Button(self.frame2, text='scroll_through_objects', command=self.scroll_through_objects)
        self.button_end_big_object = Button(self.frame2, text='Hilite Found Objects', command=self.show_found_objects)
        self.button_start_sub_object = Button(self.frame2, text='show_single_found_object', command=self.show_single_found_object)
        self.button_start_big_object.grid(row=0, column=0)
        self.button_end_big_object.grid(row=1, column=0)
        self.button_start_sub_object.grid(row=2, column=0)
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)

    def step_image():
        global array
        global img
        global array_ind
        global canvas
        global img_zoom
        clear_all_rects()
        array_ind += 1
        array = np.load("2small.npy")[array_ind]
        img = ImageTk.PhotoImage(image=Image.fromarray(array).resize(img_size))
        checkered(canvas,img_zoom)
        canvas.create_image(0, 0, anchor='nw', image=img)
    def scroll_through_objects(self):
        self.clear_all_rects()
        self.current_object_index += 1
        self.show_single_found_object()

    def create_guide(self, ):
        pass
    def show_single_found_object(self):    
        # matching the object to the larger image
        reses = []
        i = self.loaded_templates[self.current_object_index]
        tmask = np.zeros((224,240))
        gmask = np.zeros((224,240))
        b = i[:,:,3]
        # b is the guide mask
        obj = i[:,:,4]
        # obj is the object mask
        jmask = b.copy()
        b = np.stack([b,b,b], axis=-1)
        founds = self.find_template_in_image(self.array, i[:,:,:3], b)
        # returns image-sized mask
        print("fsum", founds.sum(),)
        mshape = jmask.shape
        #need to make big mask out of small mask + coordinates
        coords = list(zip(*np.where(founds==1)))
        for x in coords:
            print(obj.shape)
            print(np.zeros((mshape[0], mshape[1])).shape)
            print(tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]].shape)
            tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = obj
            gmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = jmask
        self.outline_found_mask(gmask.T, color='yellow')
        self.outline_found_mask(tmask.T, color='#55dd88')
    def show_found_objects(self):    
        # matching the object to the larger image
        reses = []
        for i in self.loaded_templates:
            tmask = np.zeros((224,240))
            b = i[:,:,3]
            # b is the guide mask
            obj = i[:,:,4]
            # obj is the object mask
            jmask = b.copy()
            b = np.stack([b,b,b], axis=-1)
            founds = self.find_template_in_image(self.array, i[:,:,:3], b)
            # returns image-sized mask
            print("fsum", founds.sum(),)
            mshape = jmask.shape
            #need to make big mask out of small mask + coordinates
            coords = list(zip(*np.where(founds==1)))
            for x in coords:
                print(obj.shape)
                print(np.zeros((mshape[0], mshape[1])).shape)
                print(tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]].shape)
                tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = obj
            self.outline_found_mask(tmask.T, color='yellow')

    def find_template_in_image(self, image, template, mask):
        res = cv2.matchTemplate(image.astype(np.uint8), 
                                template.astype(np.uint8), 
                                cv2.TM_CCORR_NORMED, 
                                mask=mask)
        return res >= .999
    def outline_found_mask(self, mask, color="#ff7788"):
        zz = list(zip(*np.where(mask==1)))
        print(list(zip(*np.where(mask==1))))
        for x in zz:
            bx0 = x[0]*self.img_zoom
            bx1 = bx0 + self.img_zoom
            by0 = x[1]*self.img_zoom
            by1 = by0 + self.img_zoom
            # print(x, bx0, bx1, by0, by1)
            self.all_rects.append(self.canvas.create_rectangle(bx0, by0, bx1, by1, outline="", 
                fill=color, stipple='gray50'))
    def clear_all_rects(self):
        for x in self.all_rects:
            self.canvas.delete(x)
        for x in self.all_rects:
            del(x)
        self.selected_pixels.clear()

    def load_templates(self):
        for i in list(os.walk("./templates"))[0][2]:
            self.loaded_templates.append(np.load("./templates/"+i))

root = Tk()
viewer = Viewer(root)
print(viewer.loaded_templates)
mainloop()

np.set_printoptions(threshold=sys.maxsize)

def hotkey_menu(event):
    print("pressed", repr(event.char))
    p = event.char
    if p == 'g':
        create_guide()
    if p == 'o':
        create_object()
    if p == 'q':
        remove_guide()
    if p == 'f':
        fill_object()


def mask_from_coords(coords):
    img = array
    shape_mask = (img.shape[1], img.shape[0])
    new_mask = np.zeros(shape_mask)
    coords = [[int(c) for c in x] for x in coords]
    for x in coords:
        new_mask[x[0], x[1]] = 1
    return new_mask


def print_diagnostic_info():
    print("Templates", templates)
    print(diagonal_fill_flag.get())



canvas.bind("<B1-Motion>", callback_square)
canvas.bind("<B3-Motion>", callback_erase)
canvas.bind("<Button-1>", callback_square)
canvas.bind("<Button-3>", callback_erase)
canvas.bind("<Motion>", callback_hover)
root.bind("<Key>", hotkey_menu)
