from collections.abc import Iterator
from ImageManager.im import save_image, setup_directory, IMAGE_PATTERN
import customtkinter as gui
import os
import re
from PIL import Image

WIN_X = 1000
WIN_Y = 900
END_OF_FOLDER   = -1
CONTINUE_FOLDER = 0

class ImageLoader(gui.CTk):
    _images: Iterator = None
    _cur_image = ''
    _base_path = ''
    _save_path = ''
    _OPTION_ROW = 3
    _HEADER_ROW = 1
    _PICTURE_ROW = 2

    def __init__(self, directory:str):
        super().__init__()
        gui.set_appearance_mode("System")  # Modes: system (default), light, dark
        gui.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        if directory:
            self._base_path = os.path.abspath(directory)
            self._images, self._cur_image = setup_directory(directory)

        self.title("Photo Sorter")
        self.bind('s', self.save_callback)
        self.geometry(f"{WIN_X}x{WIN_Y}")
        self.grid_columnconfigure((0, 1), weight=1)

        self.option_bar = gui.CTkButton(self, text='Settings', command=self.option_callback, height=10)
        self.option_bar.grid(row=self._OPTION_ROW, column=1, padx=10, pady=4, sticky='se')

        self.info_frame = HeaderPanel(self)
        self.info_frame.grid(row=self._HEADER_ROW, column=0, padx=10, pady=10, sticky="nsw")

        self.image_frame = ImagePanel(self)
        self.image_frame.grid(row=self._PICTURE_ROW, column=0, padx=10, pady=10, sticky="w")

        self.settings_window = None
    
    def setCurrentDirectory(self, dir_iter, cur_image):
        if cur_image:
            self._base_path = os.path.dirname(cur_image)
        self._images = dir_iter
        self._cur_image = cur_image

    def save_callback(self, key):
        if not key.state:
            return
        file_name = save_image(
            self.info_frame.name.get(),
            self.info_frame.source.get(),
            self._base_path,
            save_path=self._save_path
        )
        self.image_frame.update_name(f'{file_name}')

    def next_callback(self)->int:
        status = CONTINUE_FOLDER
        try:
            self._cur_image = self._images.__next__()
            while not IMAGE_PATTERN.findall(self._cur_image):
                self._cur_image = self._images.__next__()
        except StopIteration:
            self._images, self._cur_image = setup_directory(self._base_path)
            status = END_OF_FOLDER
        self.image_frame.reload_gui()
        return status
    
    def option_callback(self)->None:
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)  # create window if its None or destroyed
        self.settings_window.focus()
        self.settings_window.attributes('-topmost', 1)

class HeaderPanel(gui.CTkFrame):
    _NAV_ROW: int = 2
    _SOURCE_ROW: int = 1
    _NAME_ROW: int = 0

    def __init__(self, main: ImageLoader):
        super().__init__(main)

        self.name = gui.CTkEntry(self,placeholder_text='Name')
        self.source = gui.CTkEntry(self,placeholder_text='Source')

        self.name.grid(row=self._NAME_ROW, column=0, padx=10, pady=10, sticky='w')
        self.source.grid(row=self._SOURCE_ROW, column=0, padx=10, pady=10, sticky='w')

        self.next = gui.CTkButton(self, text="next", command=main.next_callback)
        self.next.grid(row=self._NAV_ROW, column=0, padx=10, pady=10, sticky='ew')

class ImagePanel(gui.CTkFrame):
    _IMAGE_LOAD_FAIL = 'No Images Found'
    _NAME_ROW = 0
    _PICTURE_ROW = 1
    IMAGE_Y = WIN_Y * .65
    gui_image: gui.CTkImage = None

    def __init__(self, main: ImageLoader):
        super().__init__(main)
        self.main = main
        self.file_name = self._IMAGE_LOAD_FAIL
        if main._cur_image:
            self.file_name = os.path.basename(main._cur_image)
            self.gui_image = self.load_image(main._cur_image)

        self.file_name_label = gui.CTkLabel(self, text=f'{self.file_name}')
        self.file_name_label.grid(row=self._NAME_ROW, column=0, padx=10, pady=10, sticky='w')
        
        self.gui_image_label = gui.CTkLabel(self, image=self.gui_image, text='')
        self.gui_image_label.grid(row=self._PICTURE_ROW, column=0, padx=20, pady=20, sticky='w')

    def reload_gui(self):
        self.gui_image = self.load_image(self.main._cur_image)
        if not self.gui_image:
            self.file_name_label.configure(require_redraw=True, text=self._IMAGE_LOAD_FAIL)
            return False
        self.gui_image_label.configure(require_redraw=True, image=self.gui_image)
        self.file_name = os.path.basename(self.main._cur_image)
        self.file_name_label.configure(require_redraw=True, text=f'{self.file_name}')

    def update_name(self, name):
        self.file_name_label.configure(require_redraw=True, text=f'{name}')

    def load_image(self, to_load:str)->gui.CTkImage:
        is_image = IMAGE_PATTERN.findall(to_load)
        if not is_image:
            return None
        img = Image.open(to_load)
        ratio = img.width/img.height
        h = self.IMAGE_Y
        w = int(self.IMAGE_Y * ratio)
        return gui.CTkImage(dark_image=img, size=(w, h))
    
class SettingsWindow(gui.CTkToplevel):
    main: ImageLoader = None

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.geometry("400x150")
        self.grid_columnconfigure((0, 1), weight=1)

        self.source_dir_label = gui.CTkLabel(self, text="Source Folder")
        self.source_dir_label.grid(row=0, column=0, padx=10, pady=10)
        self.source_dir = gui.CTkEntry(self)
        self.source_dir.grid(row=0, column=1, padx=10, pady=10)

        self.dest_dir_label = gui.CTkLabel(self, text="Destination Folder")
        self.dest_dir_label.grid(row=1, column=0, padx=10, pady=10)
        self.dest_dir = gui.CTkEntry(self)
        self.dest_dir.grid(row=1, column=1, padx=10, pady=10)

        self.save = gui.CTkButton(self, text="Cancel", command=self.cancel_callback)
        self.save.grid(row=3, column=0, padx=10, pady=10)
        self.cancel = gui.CTkButton(self, text="Save", command=self.save_callback)
        self.cancel.grid(row=3, column=1, padx=10, pady=10)

    def save_callback(self):
        new_dir = self.source_dir.get()
        img_itr, cur_img = setup_directory(new_dir)
        self.main._images = img_itr
        self.main._cur_image = cur_img
        self.main.image_frame.reload_gui()
    
    def cancel_callback(self):
        self.destroy()