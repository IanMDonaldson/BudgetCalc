import re
from datetime import datetime
from decimal import Decimal
from re import sub
from tkinter import messagebox

import pypdfium2 as pdfium
from pypdf import PdfReader

months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
          'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def return_text_for_all_pages(filename):
    print('pdfReader filename: ' + str(filename) + '\n\n')
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def return_pages_text_pdfium(filename):
    print("pdfium filename: " + str(filename) + '\n\n')
    reader = pdfium.PdfDocument(filename)
    text = ''
    for page in reader:
        text += page.get_textpage().get_text_range()
    return text


# use while creating the table so we don't have to reiterate through the table
# can't grab whether its a deposit or withdrawal so we need to calculate it
def calculate_amount(previous_balance, balance):
    # convert to int
    return balance - previous_balance


def convert_to_dec(money):
    return Decimal(sub(r'[^\d\-.]', '', money))


def convert_currency_to_int(money):
    newmoney = str(money).replace(",", '').replace('.', '').replace('$', '').replace('', '').replace("\\r\\n",
                                                                                                     '').replace("\\n",
                                                                                                                 '').replace(
        "\\r", '')
    return int(newmoney)


def convert_currency_to_intstr(money):
    return money.replace(",", '').replace('.', '').replace('$', '').replace('', '').replace("\\r\\n", '').replace("\\n",
                                                                                                                  '').replace(
        "\\r", '')


def abbr_to_month(abbreviatedDate):
    fixed = abbreviatedDate
    for abbr, month in months.items():
        if abbr in abbreviatedDate:
            fixed = abbreviatedDate.replace(abbr, month)

    return fixed


def format_date(date):
    date = date.replace("/", "-")
    try:
        datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        # Arvest and others don't have years on them, so add the year
        #   If it's January and it's going to be about decembers stuff then this won't work.get date elsewhere..?
        year_added_date = ''
        if datetime.now().month == 1 and date[:2] == '12':
            # add last year to date
            year_added_date = date + "-" + str(datetime.now().year - 1)
        else:
            year_added_date = date + "-" + str(datetime.now().year)
        # now format to 0 padded
        try:
            dateobj = datetime.strptime(year_added_date, "%m-%d-%Y")
            return datetime.strftime(dateobj, "%m-%d-%Y")
        except ValueError:
            # can't happen..but just in case..throw error and stop
            messagebox.showerror("Invalid Date", "There was an invalid date during parse of pdf statements..Quitting")
            sys.exit()
    return date


def clean_description(description):
    pattern = r'(#\d+)|(?<=Amazon Prime)(\*[\w\d]+)(?= Amzn)|LITTLE|(ROCK|\,)|(?: +)AR(?: )|Little Rock|LITTLEAR|(\d+)|\"|(x{3,})|Ref|[:\-#\/\.&\*]|(?<=Online Transfer )(\w+)(?= to Wells Fargo)|(?<=Zelle to Matthew on )(\w+)(?= )|(?<=Savings \\)(\w+ on)|(?<=\n)(\w+ on)|(?<= on )(\w{8})(?= \w|\n)|( \w+)(?= Amzncombill)|(?<= on )(\w+)|( {2,})'
    cleaned = sub(pattern, '', description)
    space_cleaned = remove_extra_spaces(cleaned)
    if (re.findall(pattern, space_cleaned)):
        extra_cleaned = sub(pattern, '', space_cleaned)
        extra_space_cleaned = remove_extra_spaces(extra_cleaned)
        return extra_space_cleaned
    else:
        return space_cleaned


def remove_extra_spaces(description):
    cleaned = sub(r' {2,}', ' ', description)
    return cleaned
