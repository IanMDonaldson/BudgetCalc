import tkinter as ttk
from tkinter import messagebox
import sys
import tkinter.dialog
from PIL.ImageTk import PhotoImage

import Repositories.ClassificationRepository as classrepo


class InputOptionBox(ttk.Frame):

    def __init__(self, master, description):
        super().__init__(master)
        top=self.top=ttk.Toplevel(master)

        self.description = description

        self.l1 = ttk.Label(top, text="Select an existing Category to place this Transaction under.\n" + description)
        self.l1.pack()

        self.vals = classrepo.get_unique_classifications()
        self.vals.insert(0, "Select an Option")
        self.selectedValue = ttk.StringVar(value="Select an Option")
        self.options = ttk.OptionMenu(top, self.selectedValue, *self.vals)
        self.options.pack()

        self.l2 = ttk.Label(top, text="\n\nOtherwise enter a new one\nCancelling will stop the program completely")
        self.l2.pack()
        # add an entry widget
        self.enteredValue = ttk.StringVar(value="")
        self.entryfield = ttk.Entry(top, textvariable=self.enteredValue)
        self.entryfield.pack()

        # add a button
        okbutton = ttk.Button(top, text="OK", command=self.OKButtonPressed)
        okbutton.pack()

        cancelbutton = ttk.Button(top, text="Cancel", command=lambda: (sys.exit()))
        cancelbutton.pack()


    def OKButtonPressed(self):

        # try:
        if ((len(self.entryfield.get()) == 0 and self.selectedValue.get() == "Select an Option") or (len(self.entryfield.get()) != 0 and self.selectedValue.get() != "Select an Option")):
            messagebox.showwarning(title="Only one field can be set", message="Only one field can be set")
            self.top.lift()
        else:
            self.exit_popup()


    def exit_popup(self):
        self.top.destroy()
