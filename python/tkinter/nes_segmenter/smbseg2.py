  

from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from scipy import ndimage

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")

def _bound_to_mousewheel(self, event):
    canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

def _unbound_to_mousewheel(self, event):
    canvas.unbind_all("<MouseWheel>") 

def _on_mousewheel(self, event):
    canvas.yview_scroll(int(-1*(event.delta/300)), "units")

def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (int(x2-x1), int(y2-y1)), fill)
        images.append(ImageTk.PhotoImage(image))
        irect = canvas.create_image(x1, y1, image=images[-1], anchor='nw')
        all_rects.append(irect)
    rect = canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    all_rects.append(rect)
def callback_square(event):
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
    bx0 = (cx//img_zoom)*img_zoom
    bx1 = bx0 + img_zoom
    by0 = (cy//img_zoom)*img_zoom
    by1 = by0 + img_zoom
    if (cx//img_zoom, cy//img_zoom) not in object_pixels:
        create_rectangle(bx0, by0, bx1, by1, outline='red', fill='red', alpha=.3)
        object_pixels.add((cx//img_zoom, cy//img_zoom))
def callback_erase(event):
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
    bx0 = (cx//img_zoom)*img_zoom
    bx1 = bx0 + img_zoom
    by0 = (cy//img_zoom)*img_zoom
    by1 = by0 + img_zoom
    if (cx//img_zoom, cy//img_zoom) in object_pixels:
        create_rectangle(bx0, by0, bx1, by1, outline='black', fill='black', alpha=.3)
        object_pixels.remove((cx//img_zoom, cy//img_zoom))
    # subobject pixels
def outline_found_mask(mask, color='green'):
    zz = list(zip(*np.where(mask==1)))
    # print(list(zip(*np.where(mask==1))))
    for x in zz:
        bx0 = x[0]*img_zoom
        bx1 = bx0 + img_zoom
        by0 = x[1]*img_zoom
        by1 = by0 + img_zoom
        # print(x, bx0, bx1, by0, by1)
        create_rectangle(bx0, by0, bx1, by1, outline=color, fill=color, alpha=.3)
def clear_all_rects():
    for x in all_rects:
        canvas.delete(x)
    for x in all_rects:
        del(x)
    # maybe necessary if memory leaks

def find_template_in_image(image, template, mask):
    res = cv2.matchTemplate(image.astype(np.uint8), 
                            template.astype(np.uint8), 
                            cv2.TM_CCORR_NORMED, 
                            mask=mask)
    return res == 1

def add_template(mask,):
    img = array
    brect = cv2.boundingRect(mask.astype(np.uint8))
    r = brect
    mask = mask[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    b = img[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    templates.append(np.stack[b,mask])
    object_pixels.clear()

def mask_from_coords(coords):
    img = array
    shape_mask = (img.shape[1], img.shape[0])
    new_mask = np.zeros(shape_mask)
    coords = [[int(c) for c in x] for x in coords]
    for x in coords:
        new_mask[x[0], x[1]] = 1
    return new_mask

def print_obj():
    print(object_pixels)

def create_mask():
    clear_all_rects()
    mask = mask_from_coords(object_pixels)
    add_template(mask)
    outline_found_mask(mask)
    print(all_rects)

def create_submask():
    mask = mask_from_coords(object_pixels)
    add_template(mask)
    outline_found_mask(mask, 'blue')
    print(all_rects)

def save_templates():
    for i in range(len(templates)):
        np.save("template" + str(i), templates[i])

def load_templates():
    templates = []
    for i in list(os.walk("./templates"))[0][2]:
        templates.append(np.load(i))

def show_found_objects():    
    # matching the object to the larger image
    reses = []
    for i in templates:
        tmask = np.zeros((240,224))
        founds = find_template_in_image(image, i[:3], i[3])
        mshape = i[3].shape
        #need to make big mask out of small mask + coordinates
        coords = list(zip(*np.where(founds==1)))
        for x in coords:
            tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = i[3]
        outline_found_mask(tmask, color='yellow')

root = Tk()
object_pixels = set()
subobjects = []
subobject_pixels = set()
all_rects = []
# load + zoom image
array = np.load("2small.npy")[0]
print(array.dtype)
img_zoom = 4
img_size = (240*img_zoom, 224*img_zoom)
img = ImageTk.PhotoImage(image=Image.fromarray(array).resize(img_size))

# add scroll bar

canvas_width = img_size[0]
canvas_height = img_size[1]
canvas = Canvas(root, 
           width=canvas_width,
           height=canvas_height)

images = []  # to hold the newly created image


canvas.bind_all("<MouseWheel>", _on_mousewheel)

scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, rowspan=4)
canvas.configure(yscrollcommand = scrollbar.set)
canvas.grid(row=0,column=0, rowspan=4, sticky='ns')
canvas.create_image(0, 0, anchor='nw', image=img)
checkered(canvas,4)
button_start_big_object = Button(root, text='Start Big Object', command=create_mask)
button_end_big_object = Button(root, text='Hilite Found Objects', command=show_found_objects)
button_start_sub_object = Button(root, text='Start Sub Object', command=create_submask)
button_save_sub_object = Button(root, text='Save Obj + Sub Objects', command=save_templates)
button_load_sub_object = Button(root, text='Load Obj + Sub Objects', command=load_templates)
button_start_big_object.grid(row=0, column=2)
button_end_big_object.grid(row=0, column=3)
button_start_sub_object.grid(row=1, column=2)
button_save_sub_object.grid(row=1, column=3)
button_save_sub_object.grid(row=1, column=4)


canvas.bind("<B1-Motion>", callback_square)
canvas.bind("<B3-Motion>", callback_erase)
canvas.bind("<Button-1>", callback_square)
canvas.bind("<Button-3>", callback_erase)

templates = []
# np_array_index_dict = {}
# mask_array_index_dict = {}

mainloop()


# The result of the previous script looks like this: 

# Checkered canvas
