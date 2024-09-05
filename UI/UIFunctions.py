import tkinter.dialog
from tkinter import StringVar, TOP, RIGHT, LEFT, BOTTOM, messagebox, simpledialog
from tkinter.simpledialog import askstring

from Repositories import ClassificationRepository
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from UI import CalendarDialog, UIFunctions, InputOptionBox
from Services import ExcelService
from PIL import Image

global_root = tkinter.Toplevel


def create_label_and_input(root_elem, labelText):
    classLabel = ctk.CTkLabel(root_elem, text=labelText, width=300, height=25)
    classLabel.grid(row=2, column=1, padx=10)

    classEntry = ctk.CTkEntry(root_elem, width=50, height=25)
    classEntry.grid(row=3, column=1, padx=10)


def create_csv_inputs_hide_root(root_elem, row):
    img = ctk.CTkImage(light_image=Image.open('resources/img/calendar.png'),
                       dark_image=Image.open('resources/img/calendar.png'),
                       size=(20,20))
    beginDateString = tkinter.StringVar(value='')
    endDateString = tkinter.StringVar(value='')
    beginDateEntry = ctk.CTkEntry(root_elem, width=80, height=25, placeholder_text="Begin Date", textvariable=beginDateString)
    beginDateEntry.grid(row=row, column=1, padx=(30, 0), pady=(50, 0))


    beginDateCalButton = ctk.CTkButton(root_elem, width=30, height=30, image=img, text='', textvariable=beginDateString,
                                       command=lambda: (beginDateString.set(CalendarDialog.create_elem(root_elem)),
                                                        print(beginDateString.get())))
    beginDateCalButton.grid(row=row, column=2, padx=(0, 10), pady=(50, 0))


    endDateEntry = ctk.CTkEntry(root_elem, width=80, height=25, placeholder_text="End Date", textvariable=endDateString)
    endDateEntry.grid(row=row, column=3, padx=(30, 0), pady=(50, 0))


    endDateCalButton = ctk.CTkButton(root_elem, width=30, height=30, image=img, text='', textvariable=endDateString,
                                     command=lambda: (endDateString.set(CalendarDialog.create_elem(root_elem))))
    endDateCalButton.grid(row=row, column=4, padx=(0, 10), pady=(50, 0))

    downloadButton = ctk.CTkButton(root_elem, width=100, height=30, text="Download CSV",
                                   command=lambda: download_csv(root_elem, beginDateEntry, endDateEntry))
    downloadButton.grid(row=row+2, column=2, padx=40, pady=(30, 0))


def download_csv(root_elem, beginEntry: ctk.CTkEntry, endEntry: ctk.CTkEntry):
    print("hello")
    if not (beginEntry.get() or endEntry.get()):
        dialog = messagebox.showerror(title="No date Entered", message="Please enter a beginning and ending date")
        return
    ExcelService.create_xl_from_dates(beginEntry.get(), endEntry.get())


def createctkInput(root, desription):
    dialog = tkinter.dialog.Dialog

    l1 = ClassificationRepository.get_unique_classifications()
    print(str(l1))
    options = ctk.CTkOptionMenu(dialog, width=50, height=20, values=l1)
    options.grid(row=3, column=1)


def create_classification_input_dialog(description):
    popup = InputOptionBox.InputOptionBox(global_root, description)
    popup.wait_window(popup.top)
    result = popup.selectedValue.get().upper() if (popup.selectedValue.get() != "Select an Option") else popup.enteredValue.get().upper()
    return result


def set_root(root):
    global global_root
    global_root = root

