from tkinter import StringVar, TOP, RIGHT, LEFT, BOTTOM, messagebox, simpledialog
from tkinter.simpledialog import askstring
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from UI import CalendarDialog, UIFunctions
from Services import ExcelService
from PIL import Image



def create_label_and_input(root_elem, labelText):
    classLabel = ctk.CTkLabel(root_elem, text=labelText, width=300, height=25)
    classLabel.grid(row=2, column=1, padx=10)

    classEntry = ctk.CTkEntry(root_elem, width=50, height=25)
    classEntry.grid(row=3, column=1, padx=10)


def create_csv_inputs_hide_root(root_elem, row):
    img = ctk.CTkImage(light_image=Image.open('resources/img/calendar.png'),
                       dark_image=Image.open('resources/img/calendar.png'),
                       size=(20,20))
    beginDateEntry = ctk.CTkEntry(root_elem, width=80, height=25, placeholder_text="Begin Date")
    beginDateEntry.grid(row=row, column=1, padx=(30, 0))


    beginDateCalButton = ctk.CTkButton(root_elem, width=30, height=30, image=img, text='',
                                       command=lambda: CalendarDialog.create_elem(root_elem))
    beginDateCalButton.grid(row=row, column=2, padx=(0, 10))


    endDateEntry = ctk.CTkEntry(root_elem, width=80, height=25, placeholder_text="End Date")
    endDateEntry.grid(row=row, column=3, padx=(30, 0))


    endDateCalButton = ctk.CTkButton(root_elem, width=30, height=30, image=img, text='',
                                     command=lambda: CalendarDialog.create_elem(root_elem))
    endDateCalButton.grid(row=row, column=4, padx=(0, 10))


    downloadButton = ctk.CTkButton(root_elem, width=100, height=30, text="Download CSV",
                                   command=lambda: download_csv(root_elem, beginDateEntry, endDateEntry))
    downloadButton.grid(row=row+2, column=2, padx=40, pady=(10, 0))


def download_csv(root_elem, beginEntry: ctk.CTkEntry, endEntry: ctk.CTkEntry):
    print("hello")
    if not (beginEntry.get() or endEntry.get()):
        dialog = messagebox.showerror(title="No date Entered", message="Please enter a beginning and ending date")
        return
    ExcelService.create_xl_from_dates(beginEntry.get(), endEntry.get())


def create_classification_input_dialog(description):
    print("create_classification_input_dialog")
    dialog = askstring("Insert Classification", "Please enter the classification for: " + description)
    try :
        while len(dialog) == 0:
            warn = messagebox.showwarning(title="Nothing entered", message="Please enter a value")
            dialog = askstring("Insert Classification", "Please enter the classification for: " + description)
        else:
            print('value entered!')
            print(dialog)
            return dialog
    except TypeError:
        messagebox.showerror(title="don't click cancel", message='cancel was clicked - exiting program')
        exit()





'''root = Tkinter.Tk()
    root.wm_title("CalendarDialog Demo")

    def onclick():
        cd = CalendarDialog(root)
        print cd.result

    button = Tkinter.Button(root, text="Click me to see a calendar!", command=onclick)
    button.pack()
    root.update()

    root.mainloop()'''



