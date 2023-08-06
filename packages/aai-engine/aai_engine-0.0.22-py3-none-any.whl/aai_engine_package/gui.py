"""GUI for editing the screenshots"""
import argparse
from genericpath import isdir
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel
from tkinter import filedialog as fd
import os
import glob
import tempfile
import sys
from random import choice
from string import digits
from PIL.PngImagePlugin import PngImageFile
from matplotlib.pyplot import show, text
from pyparsing import col
from aai_engine_package.screenshot_taker import MessageBox, ScreenShotTaker, NORMAL_SCREENSHOT, OCR_SCREENSHOT, SCREENSHOT
from aai_engine_package import engine
from aai_engine_package.engine_util import screenshot


DEV = False

MIN_WIDTH = 900
MIN_HEIGHT = 550
SHOW_IMAGE_PADDING = 300


dirname = os.path.dirname(__file__)
if os.name == "posix":
    icon_path = os.path.join(dirname, r'style/icon.ico')
    theme_path = os.path.join(dirname, r'style/sun-valley.tcl')
else:
    icon_path = os.path.join(dirname, r'style\icon.ico')
    theme_path = os.path.join(dirname, r'style\sun-valley.tcl')

class ApplicationData():
    """
    Class to keep track of application data and notify the listeners.
    """
    def __init__(self):
        self._directory = ""
        self._observers = []

    @property
    def directory(self):
        """return directory
        """
        return self._directory

    def _observed(func):
        def wrapper(self,value):
            func(self, value) # call setter function

            # notify all observers (initiate their callbacks)
            for callback in self._observers:
                callback(self._directory)

        return wrapper

    @directory.setter
    @_observed
    def directory(self, value):
        print(f"Setting new directory: {value}")
        self._directory = value

    def bind_to(self, callback):
        """bind to
        """
        self._observers.append(callback)


# END ApplicationData
# --- --- --- --- --- --- --- --- ---
# START GUI

class Toolbar(tk.Frame):
    """
    Class to manage the toolbar for application level funcitons.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        menubar = tk.Menu(self.parent.master)
        self.parent.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open task folder", command=self.on_open)
        file_menu.add_command(label="New", command=self.on_new)
        file_menu.add_command(label="New OCR", command=self.on_new_ocr)
        file_menu.add_command(label="refresh", command=self.on_refresh)
        menubar.add_cascade(label="File", menu=file_menu)


    def on_open(self):
        """_summary_
        """
        directory = fd.askdirectory(title="Select a directory", master=self.parent)
        if isinstance(directory,str):
            self.parent.data.directory = directory

    def on_new(self):
        """_summary_
        """
        capture(self.parent.data.directory, update_function_after_edit=self.parent.load_files,)

    def on_new_ocr(self):
        """_summary_
        """
        capture(self.parent.data.directory, update_function_after_edit=self.parent.load_files, screenshot_type=OCR_SCREENSHOT)

    def on_refresh(self):
        """_summary_
        """
        self.parent.data.directory = self.parent.data.directory


class Main(tk.Frame):
    """
    Class to manage the main view of the application.
    """
    def __init__(self, parent, data, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.data = data
        self.button_width = 10
        self.lst = tk.Listbox(self, width=20)
        self.lst.pack(sid="left", fill=tk.BOTH, expand=0)
        self.lst.bind("<<ListboxSelect>>", self._show_img)
        self.parent = parent

        # edit_button = tk.Button(self, text="Edit", command = self._edit_img)
        edit_button = ttk.Button(self, text="Edit", command = self._edit_img, style='Accent.TButton', width = self.button_width)
        # edit_button.configure(width=10, background="#ffffff" ,activebackground="#33B5E5", relief = tk.FLAT)
        edit_button.pack(padx=(0, 25), pady=(25,0), side=tkinter.BOTTOM)

        delete_button = ttk.Button(self, text="Delete", command = self._delete_img, style= 'Accent.TButton', width = self.button_width)
        delete_button.pack(padx=(0, 25), pady=(25,0), side=tkinter.BOTTOM)

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.show_img_label = tk.Label(self, text="", )
        self.show_img_label.pack(side=tkinter.BOTTOM)


    # Observes application data (mainly current directory)
    def on_data_update(self, directory):
        """_summary_

        Args:
            directory (_type_): _description_
        """
        # Check if directory is valid
        if os.path.isdir(directory):
            self._load_files(directory)
        else:
            print(f"{directory} is not a valid directory!")

    def _load_files(self, directory):
        """_summary_

        Args:
            directory (_type_): _description_
        """
        self.lst.delete(0, tk.END) # clear previously opened folder list
        imgs = glob.glob(os.path.join(directory,'*.png'))
        for img in imgs:
            img = img.replace(directory + '/','')
            self.lst.insert(tk.END, img)

        if self.lst.size() > 0:
            self.lst.selection_set(0) # select first item of the list to show
            self._show_img(None) # show to selected item

    def _delete_img(self):
        """on click function for the deletion of an image
        """
        selec = self.lst.curselection()
        filename = os.path.join(self.data.directory, self.lst.get(selec))
        answer = askyesnocancel("Deleting image", f"Are you sure you want to delete {filename}?")
        if answer:
            os.remove(filename)
            print(f"Deleted image: {filename}")
            # Refresh the current directory
            self.on_data_update(self.data._directory)


    def _edit_img(self):
        """_summary_
        """
        selec = self.lst.curselection()
        try:
            filename = os.path.join(self.data.directory, self.lst.get(selec))
            print(f"Edit image: {filename}")
            img = PngImageFile(filename)
            img_keys = list(img.text.keys())
            if ('offset_x' not in img_keys) or ('offset_y' not in img_keys) or ('upper_confidence' not in img_keys) or ('lower_confidence' not in img_keys):
                print("  -The image does not contain the right metadata!")
                return

            if 'ocr_box_relative' in img.text:
                MessageBox(
                    self, self.parent,
                    "GUI - Message",
                    "You cannot edit OCR images because the OCR box could be placed outside the needle image!\nPlease create a new OCR image instead. (File -> new OCR)",
                    (650, 170)
                )
            else:
                capture(self.data.directory, update_function_after_edit=self._load_files, needle=filename, editing=True)
        except Exception as ex:
            print("Image could not be edited!")

    def process_ocr_box(self, ocr_box):
        """Processes the ocr_box metadata into readable information

        Args:
            ocr_box (str): ocr_box metadata

        Returns:
            str: The processed metadata
        """
        info = ocr_box[1:-1].split(',')
        result = "This is an OCR image. It has an OCR box attached to it, where you can perform OCR operations.\n"
        result += "The OCR box is drawn at the given offset, seen from the top left of the image \n"
        result += "The following metadata of the OCR box is available: \n"
        result += f"Offset=({info[0]},{info[1]}) - width: {info[2]}, height: {info[3]})"
        return result

    def _show_img(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """
        try:
            selec = self.lst.curselection()
            filename = os.path.join(self.data.directory, self.lst.get(selec))

            img = tk.PhotoImage(file=filename)
            metadata = PngImageFile(filename).text
            if 'ocr_box_relative' in metadata.keys():
                self.show_img_label.configure(text=self.process_ocr_box(metadata['ocr_box_relative']))
            else:
                self.show_img_label.configure(text="")
            width, height = img.width(), img.height()
            print(f"Currently showing: {filename}")
            self.canvas.image = img
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
            self.canvas.pack()

            # Adjust screensize to image dimensions
            height = img.height()
            width = img.width()
            # Height setting:
            if (height + SHOW_IMAGE_PADDING) > MIN_HEIGHT:
                height += SHOW_IMAGE_PADDING
                if height > self.parent.parent.winfo_screenheight():
                    height = self.parent.parent.winfo_screenheight()
            else:
                height = MIN_HEIGHT
            # Width setting:
            if (width + SHOW_IMAGE_PADDING) > MIN_WIDTH:
                width += SHOW_IMAGE_PADDING
                if width > self.parent.parent.winfo_screenwidth():
                    width = self.parent.parent.winfo_screenwidth()
            else:
                width = MIN_WIDTH
            self.parent.parent.geometry(f"{str(width)}x{str(height)}")
            print(f"New window dimensions: ({str(width)},{str(height)})")

        except Exception as ex:
            print(ex)
            self.canvas.delete("all")
            print("Image could not be shown!")


class MainApplication(tk.Frame):
    """
    Class to group all UI elements.
    """
    def __init__(self, parent, command_line_options, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.master.title("AAI Image manager")

        self.parent = parent

        self.data = ApplicationData()

        self.toolbar = Toolbar(self)
        self.main = Main(self, self.data)

        self.data.bind_to(self.main.on_data_update) # main view observes the data

        self.toolbar.pack(side="top", fill="x")
        self.main.pack(side="right", fill="both", expand=True)

        parent.tk.call('source', _get_theme_path())
        parent.tk.call("set_theme", "dark")

        print("The command line arguments are:")
        for key,value in command_line_options.items():
            print(f"  -Name= {key}, Value= {value}")

        self.data.directory = command_line_options['d']

        # DEV ONLY
        if DEV:
            self.data.directory = r'/home/toto/aai/aai_engine_example_app/rpa_challenge_1_linux/img'

    def load_files(self, directory):
        """_summary_
        """
        self.main._load_files(directory)

def get_args():
    """Parser for the command line options of the GUI

    Returns:
        dict: Dictionary of the command line options
    """
    parser = argparse.ArgumentParser("Arguments for the GUI")

    # Add arguments here:
    parser.add_argument("-d",metavar="DIRECTORY", type=str, help= "Enter a directory where the application will look for png images",default=os.path.join(os.path.expanduser('~'),"Pictures"))

    return vars(parser.parse_args())


def _get_theme_path():
    return theme_path


def cli():
    """_summary_
    """
    if len(sys.argv) == 2:
        save_location = sys.argv[1]
        print(os.getcwd(), save_location)
    else:
        print("ERROR: Please provide your desired save location, eg: aai-engine-capture './path/to/location'")
        return
    print("Called aai-engine-capture")
    capture(save_location)

def test_edit(save_location, param2):
    """Edit stub
    """
    pass


def edit(save_location, haystack):
    """Calls the edit routine
    """
    capture(save_location, haystack, editing=True)


def capture(save_location, update_function_after_edit=None, needle=r"C:\Users\Toto\Documents\AdAstraIndustries\aai_engine\img\cv.png", editing=False, screenshot_type = NORMAL_SCREENSHOT):
    """main
    """
    temp_screenshot = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_screenshot_path = temp_screenshot.name
    if sys.platform == "darwin":
        temp_screenshot_path = temp_screenshot_path.split(".")[0] + "_000.png"
    print("TEMP PATH: ", temp_screenshot_path)
    take_screenshot(temp_screenshot_path)

    root = tkinter.Tk()
    style = ttk.Style(root)
    root.wm_colormapwindows()

    root.tk.call('source', theme_path)
    root.tk.call("set_theme", "dark")

    if editing:
        print(" - EDIT MODE - ")
        app = ScreenShotTaker(root, save_location, update_function_after_edit=update_function_after_edit, needle=needle, haystack=temp_screenshot_path,
                              editing=True)  # When editing from extension
    else:
        print(" - CREATE MODE - ")
        app = ScreenShotTaker(root, save_location, update_function_after_edit=update_function_after_edit, haystack=temp_screenshot_path, editing=False, screenshot_type=screenshot_type)

    root.mainloop()
    temp_screenshot.close()
    os.unlink(temp_screenshot.name)



def take_screenshot(file_path='my_screenshot.png'):
    """
    Take a screenshot.
    Args:

    """
    print("Taking screenshot")
    # time.sleep(3)
    img = screenshot(file_path)
    print("Done")


def take_screenshot_save(save_location):
    """
    Take a screenshot.
    Args:

    """
    print("Taking screenshot")
    # time.sleep(3)
    save_path = ''.join([save_location, "/img/aai_", ''.join(choice(digits) for i in range(12)), ".png"])
    img = screenshot(save_path)
    print("Done")

def main():
    """The main function for the GUI
    """
    args = get_args()
    root = tk.Tk()
    root.geometry("800x495+50+50")
    MainApplication(root,args).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
