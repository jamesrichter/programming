import os
from PIL import Image, ImageTk
import warnings
from pathlib import Path
import numpy as np

app_name = 'Image Annotator'

ctrl = 0x0004

uid = 'uid'
type_nucleus = 0
type_cytoplasm = 1
type_names = {0: 'nucleus', 1: 'cytoplasm'}
tag_image = 'image'
tag_thumbnail = 'thumbnail'
tag_marker = 'marker'
tag_background = 'background'
tag_highlighter = 'highlighter'
tag_back = 'back'
tag_nucleus = 'nucleus'
tag_cytoplasm = 'cytoplasm'
tag_boundary = 'boundary'
tag_wrapper = 'wrapper'
tag_area = 'area'
tag_draw = (tag_nucleus, tag_cytoplasm)
tag_attach = 'attach'
# tag_selected = 'selected'
tag_highlighted = 'highlighted'
color_outline = ['red', 'blue']
# color_fill = ['tomato', 'royal blue']
color_fill = ['red', '']
color_outline_highlighted = ['gold2', 'dodger blue']
color_stipple = ['gray12', 'gray12']
line_width = 2
vertex_radius = 3
marker_radius = 2
color_fill_marker = 'maroon'
tag_marker = 'marker'
vertex_radius_squared = vertex_radius * vertex_radius

image_extensions = ['.png', '.bmp', '.jpg', '.tif', '.tiff']
mask_nucleus = '-mask-nucleus'
mask_cytoplasm = '-mask-cytoplasm'
mask_extension = '.mask'
mask_export_extension = '.png'
edit_commands = ['Clear Mask', 'Delete Last']


def is_image_file(path):
    if not os.path.isfile(path):
        return False
    if os.path.splitext(path)[1] not in image_extensions:
        return False
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            image = Image.open(path)
        ImageTk.PhotoImage(image)
        image.close()
    except Exception as e:
        return e
    return True

def is_numpy_file(path):
    if not os.path.isfile(path):
        return False
    if os.path.splitext(path)[1] not in [".np", ".npy"]:
        return False
    # try:
    #     with warnings.catch_warnings():
    #         warnings.simplefilter('ignore')
    #         z = np.load(path)
    #         image = Image.fromarray(np.uint8(z[0]))
    #     ImageTk.PhotoImage(image)
    #     image.close()
    # except Exception as e:
    #     return e
    return True


def get_sec(file):
    stack = Path(file).parent.name[: -len('_stack')]
    image_extension = os.path.splitext(file)[1]
    edf_path = Path(file).parent.parent.joinpath('EDF')
    edf_file = str(edf_path.joinpath(stack + image_extension))
    edf_file = edf_file if is_numpy_file(edf_file) else ''
    csv_file = str(edf_path.joinpath(stack + '.csv'))
    csv_file = csv_file if os.path.isfile(csv_file) else ''
    return stack, edf_file, csv_file

# gets the parent path for the file, then stores the mask
# in a Gt/Mask folder                                             
def get_m(file, make=True):
    stack = Path(file).parent.name[: -len('_stack')]
    m_path = Path(file).parent.parent.joinpath('GT/mask')
    if make:
        m_path.mkdir(parents=True, exist_ok=True)
    m_file = str(m_path.joinpath(stack))
    return m_file


def clean_c(c_file):
    c_path = Path(c_file).parent
    c_files = [f for f in os.listdir(c_path) if f.endswith('.png')]
    for f in c_files:
        os.remove(os.path.join(c_path, f))


def get_nc(file):
    stack = Path(file).parent.name[: -len('_stack')]
    n_path = Path(file).parent.parent.joinpath('GT/nucleus')
    n_path.mkdir(parents=True, exist_ok=True)
    n_file = str(n_path.joinpath(stack))
    c_path = Path(file).parent.parent.joinpath('GT/cytoplasm/' + stack)
    c_path.mkdir(parents=True, exist_ok=True)
    c_file = str(c_path.joinpath('seg'))
    return n_file, c_file


def get_clean_nc(file):
    n_file, c_file = get_nc(file)
    clean_c(c_file)
    return n_file, c_file
