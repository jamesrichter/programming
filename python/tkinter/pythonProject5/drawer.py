import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox

from container import Container
from utility import *


class Drawer(Container):
    def __init__(self, parent):
        super().__init__(parent, width=960, height=896)
        self.changed = None
        self.b1_position = None
        self.draw = {}
        self.current_points = []
        self.low = -1
        self.high = 1
        self.current_id = None
        self.current_type = None
        self.draw_type = type_nucleus
        self.b1_position = None
        self.highlighted = None
        self.attached = None
        self.drawing = False
        self.dragging = False
        self.menu = tk.Menu(self)
        self.menu.add_command(label='Bring to Front', command=self.bring_front)
        self.menu.add_command(label='Send to Back', command=self.send_back)
        self.menu.add_command(label='Delete', command=self.delete_selected)
        self.bind_events()

    def back_order(self):
        self.low -= 1
        return self.low

    def front_order(self):
        self.high += 1
        return self.high

    def bind_events(self):
        commands = {'Motion': ['', '', '<Motion>', self.motion],  # show the end of drawing
                    'ButtonPress-1': ['', '', '<ButtonPress-1>', self.b1_press],  # begin annotating
                    'B1-Motion': ['', '', '<B1-Motion>', self.b1_motion],  # annotating
                    'ButtonRelease-1': ['', '', '<ButtonRelease-1>', self.b1_release],  # end
                    # todo: remove this line
                    'ButtonPress-2': ['', '', '<ButtonPress-2>', self.b3_press],  # popup menu for macOS
                    'ButtonPress-3': ['', '', '<ButtonPress-3>', self.b3_press],  # popup menu
                    # todo: remove this line
                    'B2-Motion': ['', '', '<B2-Motion>', self.b3_motion],
                    'B3-Motion': ['', '', '<B3-Motion>', self.b3_motion],
                    # todo: remove this line
                    'ButtonRelease-2': ['', '', '<ButtonRelease-2>', self.b3_release],
                    'ButtonRelease-3': ['', '', '<ButtonRelease-3>', self.b3_release],
                    }
        for (key, value) in commands.items():
            self.canvas.bind(value[2], value[3])

    def set_changed(self, changed):
        self.changed = changed

    def motion(self, event):
        if self.has_page() and not self.drawing:
            # self.lowlight()
            # self.highlight()
            self.detach()
            self.attach((event.x, event.y))

    def detach(self):
        self.attached = None
        self.canvas.delete(tag_attach)

    def attach(self, p):
        # all squared distances from terminating points
        items = self.draw.items()
        disquared = {k: (d[-1][0] - p[0]) ** 2 + (d[-1][1] - p[1]) ** 2
                     for k, (_, _, d) in items if d[0] != d[-1]}
        if len(disquared):
            min_uid = min(disquared, key=disquared.get)
            # if minimum distance is less than or equal to vertex_radius
            if disquared[min_uid] <= vertex_radius_squared:
                self.attached = min_uid
                # draw[min_uid] = [type, points]; points[-1] is the last point
                ep = self.draw[min_uid][-1][-1]
                self.canvas.create_oval(ep[0] - vertex_radius, ep[1] - vertex_radius,
                                        ep[0] + vertex_radius, ep[1] + vertex_radius,
                                        tags=[min_uid, tag_attach], width=1, fill='')

    def toggle_draw(self):
        self.draw_type = 1 - self.draw_type

    def b1_press(self, event):
        p = (int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y)))
        # if self.has_page() and self.on_image(p):
        #     self.drawing = True
        #     # todo: disable it more often
        #     self.parent.menu.set_item_state(edit_commands, 'disabled')
        #     if self.attached is not None:
        #         self.current_id = self.attached
        #         _, self.current_type, self.current_points = self.draw.pop(self.attached)
        #         self.detach()
        #         self.extend_draw(p)
        #     self.b1_position = p

    def b1_motion(self, event):
        p = (int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y)))
        # if self.drawing and self.on_image(p):
        #     # self.lowlight()
        #     self.extend_draw(p)
        #     self.b1_position = p

    def b1_release(self, event):
        if self.drawing:
            self.end_draw()  # the last point is included in the motion
        #     if len(self.draw) != 0:
        #         self.parent.menu.set_item_state(edit_commands, 'normal')
        #     self.drawing = False
        #     self.b1_position = None

    def b3_press(self, event):
        # todo: the highlighted object does not update
        self.update()
        self.motion(event)
        if self.highlighted is None:
            self.dragging = True
            self.canvas.scan_mark(event.x, event.y)
        else:
            self.menu.tk_popup(event.x_root, event.y_root)

    def b3_motion(self, event):
        if self.dragging:
            self.canvas.scan_dragto(event.x, event.y, 1)

    def b3_release(self, event):
        self.dragging = False

    def send_back(self):
        if self.has_page() and self.highlighted is not None:
            self.canvas.tag_lower(self.highlighted + '&&' + tag_boundary)
            self.canvas.tag_lower(self.highlighted + '&&' + tag_area)
            self.canvas.tag_lower(tag_back)
            self.canvas.tag_lower(tag_background)
            self.draw[self.highlighted] = (self.back_order(), *self.draw[self.highlighted][1:])
            # self.lowlight()
            # todo: fix; highlight do the same action it did last time
            # self.canvas.update()
            # self.highlight()

    def bring_front(self):
        if self.has_page() and self.highlighted is not None:
            self.canvas.tag_raise(self.highlighted + '&&' + tag_area)
            self.canvas.tag_raise(self.highlighted + '&&' + tag_boundary)
            self.draw[self.highlighted] = (self.front_order(), *self.draw[self.highlighted][1:])
            # todo: fix; highlight do the same action it did last time
            # self.canvas.update()
            # self.highlight()

    # def draw_mask(self, mask_id, mask_type, mask_points):
    #     self.canvas.create_polygon(mask_points, tags=(mask_id, tag_draw[mask_type], tag_area),
    #                                width=0, fill=color_fill[mask_type], stipple=color_stipple[mask_type])
    #     self.canvas.create_line(mask_points, tags=(mask_id, tag_draw[mask_type], tag_boundary),
    #                             fill=color_outline[mask_type], width=line_width)
    #     self.canvas.create_line((mask_points[-1], mask_points[0]),
    #                             tags=(mask_id, tag_draw[mask_type], tag_boundary, tag_wrapper),
    #                             fill=color_outline[mask_type], width=line_width, dash=(6, 4))

    # def extend_draw(self, point):
    #     if len(self.current_points) == 0 and self.on_image(self.b1_position):
    #         self.current_points = [self.b1_position]
    #         self.current_type = self.draw_type
    #     if self.on_image(point):
    #         self.current_points.append(point)
    #     self.changed = True
    #     if len(self.current_points) == 1:
    #         return
    #     if self.drawing:
    #         self.canvas.delete(self.current_id)
    #     self.current_id = self.uid()
    #     self.draw_mask(self.current_id, self.current_type, self.current_points)
    #
    # def end_draw(self):
    #     if len(self.current_points) <= 2:
    #         if self.drawing:
    #             self.canvas.delete(self.current_id)
    #     else:
    #         self.draw[self.current_id] = (self.front_order(), self.current_type, self.current_points)
    #     self.current_points = []
    #     self.current_id = None

    # def highlight(self):
    #     tags = self.canvas.gettags('current')
    #     if tag_nucleus in tags:
    #         self.canvas.itemconfigure(tags[0] + '&&' + tag_boundary, fill=color_outline_highlighted[type_nucleus])
    #         self.highlighted = tags[0]
    #     elif tag_cytoplasm in tags:
    #         self.canvas.itemconfigure(tags[0] + '&&' + tag_boundary, fill=color_outline_highlighted[type_cytoplasm])
    #         self.highlighted = tags[0]

    # def lowlight(self):
    #     if self.highlighted is not None:
    #         highlighted_type = type_nucleus if tag_nucleus in self.canvas.gettags(self.highlighted) else type_cytoplasm
    #         self.canvas.itemconfigure(self.highlighted + '&&' + tag_boundary, fill=color_outline[highlighted_type])
    #         self.highlighted = None

    def delete_last(self):
        if not self.drawing and len(self.draw):
            last_draw = max(self.draw, key=lambda x: int(x[len(uid):]))  # not string comparison because uid99 < uid101
            self.canvas.delete(last_draw)
            self.draw.pop(last_draw)
            if self.highlighted == last_draw:
                self.highlighted = None
            self.update()
            # self.highlight()
            self.changed = True
        if len(self.draw) == 0:
            self.parent.menu.set_item_state(edit_commands, 'disabled')

    def delete_selected(self):
        if not self.drawing and self.highlighted is not None:
            self.canvas.delete(self.highlighted)
            self.draw.pop(self.highlighted)
            self.highlighted = None
            self.update()
            # self.highlight()
            self.changed = True

    def open(self):
        if not super().open():
            return False
        self.open_mask()
        return True

    def save_mask(self):
        if self.drawing:
            return
        # save vector mask
        with open(get_m(self.npimages[1]) + mask_extension, 'w') as f:
            values = sorted(self.draw.values())
            for _, t, d in values:  # order, type, points
                f.write(str(t) + ' ' + ' '.join(str(c) for p in d for c in p) + '\n')
        nucleus_file, cytoplasm_file = get_clean_nc(self.npimages[1])
        # save all nuclei to a single mask
        nucleus = (p for _, t, p in values if t == type_nucleus)  # order, type, points
        mask = Image.new('1', (self.image.width(), self.image.height()))
        draw = ImageDraw.Draw(mask)
        for points in nucleus:
            draw.polygon(points, fill=1, outline=1)
        mask.save(nucleus_file + mask_export_extension)
        # save each cytoplasm to a separate mask
        cytoplasm = (p for _, t, p in values if t == type_cytoplasm)
        for i, points in enumerate(cytoplasm):
            mask = Image.new('1', (self.image.width(), self.image.height()))
            draw = ImageDraw.Draw(mask)
            draw.polygon(points, fill=1, outline=1)
            mask.save(cytoplasm_file + f'{i + 1:03}' + mask_export_extension)

        self.changed = False

    def open_mask(self):
        try:
            with open(get_m(self.npimages[1], False) + mask_extension) as f:
                for line in f:
                    line = [int(x) for x in line.split()]
                    mask_type, mask_points, mask_id = line[0], list(zip(*[iter(line[1:])] * 2)), self.uid()
                    self.draw[mask_id] = (self.front_order(), mask_type, mask_points)
                    self.draw_mask(mask_id, mask_type, mask_points)
            self.current_points = []
            self.current_id = None
        except Exception as e:
            print(str(e))
            self.draw = {}

    def if_save_file(self):
        return tk.messagebox.askyesnocancel('Close', 'Do you want to save the mask?', parent=self.parent)

    def close(self):
        if self.has_page():
            self.end_draw()
            save = self.if_save_file() if self.changed else False
            if save is None:
                return False
            if save:
                self.save_mask()
            self.changed = False
            self.canvas.delete('all')
        return super().close()

    def clear_mask(self):
        self.canvas.delete(tag_nucleus)
        self.canvas.delete(tag_cytoplasm)
        self.canvas.delete(tag_attach)
        self.draw = {}
        self.parent.menu.set_item_state(edit_commands, 'disabled')
        self.changed = True
