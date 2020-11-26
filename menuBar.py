from tkinter import Frame, Button, LEFT
from tkinter import filedialog
import cv2
import GetText, FileOperations


class MenuBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_button = Button(self, text="New")
        self.process_button = Button(self, text="Process")
        self.clear_button = Button(self, text="Clear")

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.process_button.bind("<ButtonRelease>", self.process_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.new_button.pack(side=LEFT)
        self.process_button.pack(side=LEFT)
        self.clear_button.pack()

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

