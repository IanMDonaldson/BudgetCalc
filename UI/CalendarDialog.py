import tkinter.simpledialog as simpledialog
from datetime import datetime

import tkcalendar


class CalendarDialog(simpledialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""

    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        thedate = datetime.strptime(self.calendar.get_date(), f'%m/%d/%y')
        self.result = datetime.strftime(thedate, "%m-%d-%Y")


def create_elem(root):
    cd = CalendarDialog(root)
    return cd.result
