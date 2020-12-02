from tkinter import Frame, Button, LEFT
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import GetText, FileOperations

global new_image, process_image, clear_image, template_image, bulk_image


class MenuBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        global new_image, process_image, clear_image, template_image, bulk_image
        new_image = Image.open('Resources\\New.png')
        new_image = new_image.resize((80, 30))
        new_image = ImageTk.PhotoImage(new_image)

        process_image = Image.open('Resources\\Process.png')
        process_image = process_image.resize((80, 30))
        process_image = ImageTk.PhotoImage(process_image)

        clear_image = Image.open('Resources\\Clear.png')
        clear_image = clear_image.resize((80, 30))
        clear_image = ImageTk.PhotoImage(clear_image)

        template_image = Image.open('Resources\\AddTemplate.png')
        template_image = template_image.resize((110, 30))
        template_image = ImageTk.PhotoImage(template_image)

        bulk_image = Image.open('Resources\\BulkProcess.png')
        bulk_image = bulk_image.resize((110, 30))
        bulk_image = ImageTk.PhotoImage(bulk_image)

        self.new_button = Button(self, image=new_image, borderwidth=0)
        self.process_button = Button(self, image=process_image, borderwidth=0)
        self.clear_button = Button(self, image=clear_image, borderwidth=0)
        self.template_button = Button(self, image=template_image, borderwidth=0)
        self.bulk_button = Button(self, image=bulk_image, borderwidth=0)

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.process_button.bind("<ButtonRelease>", self.process_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)
        self.template_button.bind("<ButtonRelease>", self.template_button_released)
        self.bulk_button.bind("<ButtonRelease>", self.bulk_button_released)

        self.new_button.pack(side=LEFT, pady=20)
        self.process_button.pack(side=LEFT, pady=20, padx=30)
        self.clear_button.pack(side=LEFT, pady=20)
        self.template_button.pack(side=LEFT, pady=20, padx=30)
        self.bulk_button.pack(side=LEFT)

    def new_button_released(self, event):
        self.master.image_viewer.clear_canvas()
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:

            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def process_button_released(self, event):
        tags_list = GetText.process_image(self.master.filename, self.master.rectangle_coordinates)
        FileOperations.write_file(tags_list)

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            self.master.image_viewer.clear_canvas()

    def template_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.template_button:
            self.master.image_viewer.save_template()

    def bulk_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.bulk_button:
            template, image_path = self.master.image_viewer.get_bulk_process_data()
            print('template: {}, image_path: {}'.format(template, image_path))
            if (template and image_path) is not None:
                tags, values = GetText.process_bulk(template, image_path)
                FileOperations.write_bulk(tags, values)
