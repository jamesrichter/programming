  

from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from scipy import ndimage
import cv2
import os
import itertools

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
    # if p == '':
    #     ()
    # if p == '':
    #     ()
# button_start_big_object = Button(frame2, text='create guide', command=create_guide)
# button_end_big_object = Button(frame2, text='Hilite Found Objects', command=show_found_objects)
# button_start_sub_object = Button(frame2, text='create object', command=create_object)
# button_remove_guide = Button(frame2, text='remove guide', command=remove_guide)
# button_save_sub_object = Button(frame2, text='Save Objects', command=save_templates)
# button_load_sub_object = Button(frame2, text='Load Objects', command=load_templates)
# button_print_diagnostic = Button(frame2, text='Diagnose', command=print_diagnostic_info)
# button_fill_object = Button(frame2, text='Fill', command=fill_object)

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   img_width, img_height,  = img_size
   for x in range(line_distance,img_width,line_distance):
      canvas.create_line(x, 0, x, img_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,img_height,line_distance):
      canvas.create_line(0, y, img_width, y, fill="#476042")

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
    return rect, irect
def callback_square(event):
    if diagonal_fill_flag.get():
        callback_diag_bucket(event)
    else:
        cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
        bx0 = (cx//img_zoom)*img_zoom
        bx1 = bx0 + img_zoom
        by0 = (cy//img_zoom)*img_zoom
        by1 = by0 + img_zoom
        if (cx//img_zoom, cy//img_zoom) not in selected_pixels:
            create_rectangle(bx0, by0, bx1, by1, outline='red', fill='red', alpha=.3)
            selected_pixels.add((int(cx//img_zoom), int(cy//img_zoom)))
            print(selected_pixels, "sp1")
def callback_diag_bucket(event):
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
    bx0 = (cx//img_zoom)*img_zoom
    bx1 = bx0 + img_zoom
    by0 = (cy//img_zoom)*img_zoom
    by1 = by0 + img_zoom
    selected_coord = (int(cx//img_zoom), int(cy//img_zoom))
    print(array.shape)
    print(selected_coord)
    original_color = array[selected_coord[1]][selected_coord[0]]
    used_diag_adjacencies = set()
    new_diag_adjacencies = set([selected_coord])
    temp_new_diag_adjacencies = set()
    while new_diag_adjacencies:
        newda = new_diag_adjacencies.pop()
        used_diag_adjacencies.add(newda)
        for adj in itertools.product((-1,0,1), repeat=2):
            new_coord = (newda[0]+adj[0], newda[1]+adj[1])
            if new_coord[0] >=0 and new_coord[1] >=0 and \
            new_coord[0] < 240 and new_coord[1] < 224 and \
            (array[new_coord[1]][new_coord[0]] == original_color).all() and \
            new_coord not in used_diag_adjacencies:
                new_diag_adjacencies.add(new_coord)

        used_diag_adjacencies.add(newda)
        assert not (used_diag_adjacencies & new_diag_adjacencies)
    for xx in used_diag_adjacencies:
        if xx not in selected_pixels:
            create_rectangle(xx[0]*img_zoom, xx[1]*img_zoom, (xx[0]+1)*img_zoom, 
                (xx[1]+1)*img_zoom, outline='red', fill='red', alpha=.3)
            selected_pixels.add(xx)
def callback_erase(event):
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
    bx0 = (cx//img_zoom)*img_zoom
    bx1 = bx0 + img_zoom
    by0 = (cy//img_zoom)*img_zoom
    by1 = by0 + img_zoom
    if (cx//img_zoom, cy//img_zoom) in selected_pixels:
        create_rectangle(bx0, by0, bx1, by1, outline='black', fill='black', alpha=.3)
        selected_pixels.remove((cx//img_zoom, cy//img_zoom))
    # subobject pixels
def callback_hover(event):
    global hover_rect
    if hover_rect or hover_rect == [None]:
        canvas.delete(hover_rect[0][0])
        canvas.delete(hover_rect[0][1])
        del hover_rect[0]
    hover_rect = []
    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
    bx0 = (cx//img_zoom)*img_zoom
    bx1 = bx0 + img_zoom
    by0 = (cy//img_zoom)*img_zoom
    by1 = by0 + img_zoom
    zz = create_rectangle(bx0, by0, bx1, by1, outline="#88ff77", fill="#ff11cc", alpha=.2)
    hover_rect.append(zz)

def outline_found_mask(mask, color='green'):
    zz = list(zip(*np.where(mask==1)))
    print(list(zip(*np.where(mask==1))))
    for x in zz:
        bx0 = x[0]*img_zoom
        bx1 = bx0 + img_zoom
        by0 = x[1]*img_zoom
        by1 = by0 + img_zoom
        # print(x, bx0, bx1, by0, by1)
        create_rectangle(bx0, by0, bx1, by1, outline="#ff7788", fill="#ff7788", alpha=.3)
def clear_all_rects():
    for x in all_rects:
        canvas.delete(x)
    for x in all_rects:
        del(x)
    selected_pixels.clear()
    # maybe necessary if memory leaks

def find_template_in_image(image, template, mask):
    res = cv2.matchTemplate(image.astype(np.uint8), 
                            template.astype(np.uint8), 
                            cv2.TM_CCORR_NORMED, 
                            mask=mask)
    # print("res",repr(res))
    # print("res999",repr(res>=.999))
    return res >= .999

# adds the object from the global object mask and the global guide mask
def add_template( guide_mask, object_mask,):
    print("mask/arrayshapes",object_mask.shape, guide_mask.shape, array.shape)
    img = array
    object_mask = object_mask.T # this T is important
    guide_mask = guide_mask.T # this T is important
    print(object_mask.shape, guide_mask.shape,)
    brect = cv2.boundingRect(guide_mask.astype(np.uint8))
    r = brect
    object_mask = object_mask[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    guide_mask = guide_mask[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    b = img[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
    a = np.expand_dims(guide_mask, -1)
    z = np.expand_dims(object_mask, -1)
    result = np.concatenate([b,a,z], axis=2)
    result = result.astype(np.uint8)
    print(result, result.dtype, result.shape)
    templates.append(result)
    selected_pixels.clear()

def mask_from_coords(coords):
    img = array
    shape_mask = (img.shape[1], img.shape[0])
    new_mask = np.zeros(shape_mask)
    coords = [[int(c) for c in x] for x in coords]
    for x in coords:
        new_mask[x[0], x[1]] = 1
    return new_mask

def print_obj():
    print(selected_pixels)

def create_mask():
    clear_all_rects()
    mask = mask_from_coords(selected_pixels)
    add_template(mask)
    outline_found_mask(mask)
    print(all_rects)

def create_guide():
    global guide_pixels
    global guide_mask
    print(selected_pixels)
    guide_pixels = selected_pixels.copy()
    guide_mask = mask_from_coords(selected_pixels)
    # print(guide_mask, guide_pixels)
    clear_all_rects()
    outline_found_mask(guide_mask, "#ff7788")
    # print(all_rects)

def create_object():
    global guide_pixels
    global guide_mask
    if guide_mask != []:
        object_pixels = selected_pixels.copy()
        object_mask = mask_from_coords(selected_pixels)
        clear_all_rects()
        outline_found_mask(guide_mask, "#ff7788")
        add_template(guide_mask, object_mask)
    else:
        object_pixels = selected_pixels.copy()
        object_mask = mask_from_coords(selected_pixels)
        guide_pixels = selected_pixels.copy()
        guide_mask = mask_from_coords(selected_pixels)
        clear_all_rects()
        add_template(guide_mask, object_mask)
        outline_found_mask(guide_mask, "#ff7788")
    object_pixels = set()
    object_mask = []
    print(templates)

def remove_guide():
    global guide_mask
    global guide_pixels
    clear_all_rects()
    guide_pixels = set()
    guide_mask = []

def create_submask():
    mask = mask_from_coords(selected_pixels)
    add_template(mask)
    outline_found_mask(mask, 'blue')
    print(all_rects)

def save_templates():
    global templates
    print(templates)
    a = []
    for i in list(os.walk("./templates"))[0][2]:
        a.append(int(i.strip(".npy").strip("template")))
    if a:
        print(max(a))
        z = max(a)
    else:
        z = 0
    for i in range(len(templates)):
        np.save("templates/template" + str(i+z+1), templates[i])
        print("saved template ", str(i+z+1))
    templates = []
def load_templates():
    for i in list(os.walk("./templates"))[0][2]:
        loaded_templates.append(np.load("./templates/"+i))

def show_found_objects():    
    # matching the object to the larger image
    reses = []
    for i in templates + loaded_templates:
        print("arrty",array.shape, array.dtype)
        print("sha/dty",i.shape, i.dtype)
        tmask = np.zeros((224,240))
        # print(repr(i[:,:,:3]))
        # print(repr(i[:,:,3]))
        # print(repr(i[:,:,4]))
        b = i[:,:,3]
        # b is the guide mask
        obj = i[:,:,4]
        # obj is the object mask
        jmask = b.copy()
        b = np.stack([b,b,b], axis=-1)
        founds = find_template_in_image(array, i[:,:,:3], b)
        # returns image-sized mask
        print("fsum", founds.sum(),)
        mshape = jmask.shape
        #need to make big mask out of small mask + coordinates
        coords = list(zip(*np.where(founds==1)))
        print("mshar", mshape)
        for x in coords:
            print("ohnuiiojoji", x[0], x[0]+mshape[0], x[1], x[1]+mshape[1])
            print(obj.shape)
            print(np.zeros((mshape[0], mshape[1])).shape)
            print(tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]].shape)
            tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = obj
        #           File "smbfram.py", line 158, in show_found_objects
        #     tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = i[3]
        # ValueError: could not broadcast input array from shape (4,4) into shape (5,4)
        outline_found_mask(tmask.T, color='yellow')

def print_diagnostic_info():
    print("Templates", templates)
    print(diagonal_fill_flag.get())

def diagonal_bucket():
    # coords of selection stored in fake var coords
    global selected_pixels 
    coords = list(selected_pixels)
    ncoords = coords.copy()
    # bxh = boundary_x_high, byl = boundary_y_low
    bxh = max([x[0] for x in coords])
    byh = max([x[1] for x in coords])
    bxl = min([x[0] for x in coords])
    byl = min([x[1] for x in coords])
    # left-right
    for c in coords:
        current_coord = c
        while current_coord[0] < bxh:
            current_coord = (current_coord[0]+1, current_coord[1])
            if current_coord in coords:
                current_coord = c
                while current_coord[0] < bxh:
                    current_coord = (current_coord[0]+1, current_coord[1])
                    if current_coord in coords:
                        break
                    else:
                        ncoords.append(current_coord)
                break
    # up-down
    for c in ncoords:
        current_coord = c
        while current_coord[1] < byh:
            current_coord = (current_coord[0], current_coord[1]+1)
            if current_coord in ncoords:
                current_coord = c
                while current_coord[1] < byh:
                    current_coord = (current_coord[0], current_coord[1]+1)
                    if current_coord in ncoords:
                        break
                    else:
                        ncoords.append(current_coord)
                break
    # print(soln_coords, ncoords)
    # print("Templates", templates)
    clear_all_rects()
    outline_found_mask(guide_mask, "#ff7788")
    selected_pixels = set(ncoords)
    for x in ncoords:
        bx0 = x[0]*img_zoom
        bx1 = bx0 + img_zoom
        by0 = x[1]*img_zoom
        by1 = by0 + img_zoom
        # print(x, bx0, bx1, by0, by1)
        create_rectangle(bx0, by0, bx1, by1, outline='red', fill='red', alpha=.3)
    print(selected_pixels, "sp2")
    

def fill_object():
    # coords of selection stored in fake var coords
    global selected_pixels 
    coords = list(selected_pixels)
    ncoords = coords.copy()
    # bxh = boundary_x_high, byl = boundary_y_low
    bxh = max([x[0] for x in coords])
    byh = max([x[1] for x in coords])
    bxl = min([x[0] for x in coords])
    byl = min([x[1] for x in coords])
    # left-right
    for c in coords:
        current_coord = c
        while current_coord[0] < bxh:
            current_coord = (current_coord[0]+1, current_coord[1])
            if current_coord in coords:
                current_coord = c
                while current_coord[0] < bxh:
                    current_coord = (current_coord[0]+1, current_coord[1])
                    if current_coord in coords:
                        break
                    else:
                        ncoords.append(current_coord)
                break
    # up-down
    for c in ncoords:
        current_coord = c
        while current_coord[1] < byh:
            current_coord = (current_coord[0], current_coord[1]+1)
            if current_coord in ncoords:
                current_coord = c
                while current_coord[1] < byh:
                    current_coord = (current_coord[0], current_coord[1]+1)
                    if current_coord in ncoords:
                        break
                    else:
                        ncoords.append(current_coord)
                break
    # print(soln_coords, ncoords)
    # print("Templates", templates)
    clear_all_rects()
    outline_found_mask(guide_mask, "#ff7788")
    selected_pixels = set(ncoords)
    for x in ncoords:
        bx0 = x[0]*img_zoom
        bx1 = bx0 + img_zoom
        by0 = x[1]*img_zoom
        by1 = by0 + img_zoom
        # print(x, bx0, bx1, by0, by1)
        create_rectangle(bx0, by0, bx1, by1, outline='red', fill='red', alpha=.3)
    print(selected_pixels, "sp2")

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


root = Tk()
frame1 = Frame(root)
frame2 = Frame(root)
selected_pixels = set()
object_mask = []
object_pixels = set()
guide_mask = []
guide_pixels = set()
all_rects = []
hover_rect = []
diagonal_fill_flag = IntVar()
# load + zoom image
array = np.load("2small.npy")[0]
array_ind = 0
print(array.dtype)
img_zoom = 8
img_size = (240*img_zoom, 224*img_zoom)
img = ImageTk.PhotoImage(image=Image.fromarray(array).resize(img_size))

# add scroll bar

canvas_width = 600
canvas_height = 600
canvas = Canvas(frame1, 
           width=canvas_width,
           height=canvas_height)

images = []  # to hold the newly created image


canvas.bind_all("<MouseWheel>", _on_mousewheel)

scrollbar = Scrollbar(frame1, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
scrollbarx = Scrollbar(frame1, command=canvas.xview, orient='horizontal')
scrollbarx.grid(row=1, column=0, sticky='we')
canvas.configure(xscrollcommand = scrollbarx.set)
canvas.configure(yscrollcommand = scrollbar.set)
canvas.grid(row=0,column=0, sticky='ns')
canvas.create_image(0, 0, anchor='nw', image=img)
checkered(canvas,img_zoom)
button_start_big_object = Button(frame2, text='create Guide', command=create_guide)
button_end_big_object = Button(frame2, text='Hilite Found Objects', command=show_found_objects)
button_start_sub_object = Button(frame2, text='create Object', command=create_object)
button_remove_guide = Button(frame2, text='remove guide (Q)', command=remove_guide)
button_save_sub_object = Button(frame2, text='Save Objects', command=save_templates)
button_load_sub_object = Button(frame2, text='Load Objects', command=load_templates)
button_print_diagnostic = Button(frame2, text='Diagnose', command=print_diagnostic_info)
button_fill_object = Button(frame2, text='F\u0332ill', command=fill_object)
button_clear_screen = Button(frame2, text='Clear Screen', command=remove_guide)
button_diagonal_bucket = Checkbutton(frame2, text='Diagonal Bucket', variable=diagonal_fill_flag)
button_step_image = Button(frame2, text='step to next img', command=step_image)
button_start_big_object.grid(row=0, column=0)
button_end_big_object.grid(row=1, column=0)
button_start_sub_object.grid(row=2, column=0)
button_save_sub_object.grid(row=3, column=0)
button_load_sub_object.grid(row=4, column=0)
button_print_diagnostic.grid(row=5, column=0)
button_fill_object.grid(row=6, column=0)
button_remove_guide.grid(row=7, column=0)
button_clear_screen.grid(row=8, column=0)
button_diagonal_bucket.grid(row=9, column=0)
button_step_image.grid(row=10, column=0)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)

canvas.bind("<B1-Motion>", callback_square)
canvas.bind("<B3-Motion>", callback_erase)
canvas.bind("<Button-1>", callback_square)
canvas.bind("<Button-3>", callback_erase)
canvas.bind("<Motion>", callback_hover)
root.bind("<Key>", hotkey_menu)

templates = []
loaded_templates = []
# np_array_index_dict = {}
# mask_array_index_dict = {}

mainloop()


# The result of the previous script looks like this: 

# Checkered canvas
