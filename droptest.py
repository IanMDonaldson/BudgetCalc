import re
from tkinter import StringVar, TOP, RIGHT, LEFT, BOTTOM

import tkinterdnd2.TkinterDnD
from tkinterdnd2 import TkinterDnD, DND_ALL, DND_FILES
import customtkinter as ctk
from UI import CalendarDialog, UIFunctions
from Utils.InputUtils import handle_input

#TODO handle Input
#   2. Create Input for new Classifications
#       - Create method creating new input fields
#       - call it from input handler
#   3.

#todo make CSV_handler
#   0. Use default dates to test normal functionality
#   1. Make Datepickers for date range
#   2. Populate input fields with that, otherwise allow for manual input of dates
#   3. Pass these to handleCsv
#   4.


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        self.entryWidget = ctk.CTkEntry(self, width=100, height=100, placeholder_text='Drop Files Here')
        self.entryWidget.grid(row=1, column=3, padx=20)

        self.browserButton = ctk.CTkButton(self, text='Browse for Files', width=50, height=30, command=lambda: buttonEvent)
        self.browserButton.grid(row=1, column=1, padx=20)

        self.pathLabel = ctk.CTkLabel(self, text=" OR ", width=30, height=10)
        self.pathLabel.grid(row=1, column=2, padx=20)

        self.generateCsvButton = ctk.CTkButton(self, text='Generate CSV?', width=50, height=30,
                                          command=lambda: (self.hide_all_elems(),UIFunctions.create_csv_inputs_hide_root(self, 4)))
        self.generateCsvButton.grid(row=2, column=2, pady=50)


        self.entryWidget.drop_target_register(DND_FILES)
        self.entryWidget.dnd_bind("<<Drop:DND_Files>>", get_path)

    def hide_all_elems(self):
        self.entryWidget.grid_remove()
        self.browserButton.grid_remove()
        self.pathLabel.grid_remove()
        self.generateCsvButton.grid_remove()
        




def buttonEvent():
    fileBrowser = ctk.filedialog
    files = fileBrowser.askopenfilenames(initialdir='C:\\Users\\drago\\Downloads')
    print(files)
    for file in files:
        print('file below' + str(file) + '\n\n')
        handle_input(file)

def get_path(events: TkinterDnD.DnDEvent):
    #Filenames with spaces are surrounded by {} so remove everything surrounded by those
    #   then split on spaces
    match_between_brackets = r'(?<=\{).*?(?=})'
    match_files_not_brackets = r'([A-Z]:[^ ]*)'
    file_arr = []

    nothing_between_brackets = re.sub(match_between_brackets, lambda m: file_arr.append(m.group(0)), events.data)
    matches = re.findall(match_files_not_brackets, nothing_between_brackets)
    for match in matches:
        file_arr.append(match)

    # print(file_arr)
    for file_string in file_arr:
        handle_input(file_string)


def create_label_and_input(root_ui, labelText):
    classLabel = ctk.CTkLabel(root_ui, text=labelText, width=300, height=25)
    classLabel.grid(row=2, column=1, padx=10)

    classEntry = ctk.CTkEntry(root_ui, width=50, height=25)
    classEntry.grid(row=3, column=1, padx=10)

    #todo return entry value if exists



ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("blue")

root = Tk()
root.geometry("550x350")
root.title("Get file path")


root.mainloop()

def get_root():
    return root
