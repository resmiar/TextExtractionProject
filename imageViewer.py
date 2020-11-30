from tkinter import Frame, Canvas, CENTER, ROUND, commondialog, simpledialog, Label, Listbox, Button
from PIL import Image, ImageTk
import cv2
import PySimpleGUI as gui
import FileOperations


class ImageViewer(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="gray", width=600, height=400)

        self.shown_image = None
        self.x = 0
        self.y = 0
        self.ratio = 0
        self.rect = None
        self.rectangles = dict()
        self.draw = False

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.image_width = None
        self.image_height = None

        self.canvas = Canvas(self, bg="gray", width=600, height=400)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = None

        # create rectangle if not exists
        if not self.rect and self.master.is_image_selected:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.draw = True

        w, h = self.canvas.winfo_width()-1, self.canvas.winfo_height()-1
        # limit the draggable mouse area to just the image dimensions
        if event.x < 4:
            self.end_x = 4
        elif event.x > w:
            self.end_x = w
        else:
            self.end_x = event.x
        if event.y < 4:
            self.end_y = 4
        elif event.y > h:
            self.end_y = h
        else:
            self.end_y = event.y

        # expand rectangle as you drag the mouse if image available in canvas
        if self.master.is_image_selected:
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        if self.rect is not None and self.draw:
            # Hide main window here to show pop up on top of the main window
            # self.
            event, values = select_tag()
            if event == 'OK':
                selected_tag = str(values["LB"][0])
                if selected_tag in self.rectangles.keys():
                    self.canvas.delete(self.rectangles[selected_tag])
                self.rectangles[selected_tag] = self.canvas.create_rectangle(self.start_x,
                                                                             self.start_y, self.end_x, self.end_y)
                self.master.rectangle_coordinates[selected_tag] = list(([int(self.start_x), int(self.start_y)],
                                                                        [int(self.end_x), int(self.end_y)]))

        self.canvas.delete(self.rect)
        self.draw = False
        self.rect = None
        print(self.master.rectangle_coordinates)

    def delete_rectangle(self, name):
        self.canvas.delete(self.rect)

    def show_image(self, img=None):
        self.clear_canvas()

        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = image
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))

        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.image_width = new_width
        self.image_height = new_height
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.master.rectangle_coordinates.clear()
        self.master.is_image_selected = False

    def save_template(self):
        value, event = enter_template()
        print(value)
        template_name = value[0]
        if event == 'OK' and template_name is not None:
            print("Temp name: ", template_name)
            # template_dictionary = dict()
            template_dictionary = FileOperations.read_templates()
            template_dictionary[template_name] = [(self.image_height, self.image_width),
                                                  self.master.rectangle_coordinates]
            FileOperations.write_templates(template_dictionary)
            print("Templates available: ", template_dictionary)

    def bulk_process(self):
        pass
        # show window with dropdown to select a template and select a image path
        # get files in the given path and filter for valid ones and store in a list
        # inside a loop for all files in th list, resize the image for size in the template,
        # get text for coordinates specified in template
        # and save text in same file


def select_tag():
    gui.theme('SandyBeach')
    values = ['Name', 'ID', 'Address', 'Phone Number']
    layout = [[gui.Text('Select tag'), gui.Listbox(values, size=(15, 3), key='LB')],
              [gui.Button('OK'), gui.Button('Cancel')]]
    popup_window = gui.Window('Choose an option', layout)
    value, event = popup_window.read(close=True)
    return value, event


def enter_template():
    gui.theme('SandyBeach')
    layout = [
        [gui.Text('Please enter the name of the template')],
        [gui.Text('Name', size=(15, 1)), gui.InputText()],
        [gui.Button('OK'), gui.Cancel()]
    ]
    window = gui.Window('Enter Template Name', layout)
    event, value = window.read(close=True)
    return value, event


