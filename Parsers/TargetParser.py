import re

import pdfplumber
from Utils.ParserUtils import convert_currency_to_int, abbr_to_month, format_date, \
    clean_description


# ['Date Posted', 'Transaction Name', 'Amount', 'Balance', 'BankType']
def extractLines(text):
    pdf = pdfplumber.open(text)
    page = pdf.pages[0]
    newtext = page.extract_text()
    page = pdf.pages[1]
    newtext += page.extract_text()
    newtext = newtext.replace("$", '')
    sum = 0
    transactions = []
    regex = r"(\D{3}\. \d\d|\D{3}\. \d)(?: +)(.+ )([-\d{1,3}|(?:\,)]+(?:\.)\d\d)"
    matches = re.findall(regex, newtext, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        post_date = format_date(abbr_to_month(match[0].replace(". ", '/')))
        name = clean_description(match[1])
        amount = -convert_currency_to_int(match[2])
        sum += amount
        transactions.append([post_date, name, amount, sum, 'Target'])
    return sorted(transactions, key=lambda transaction: transaction[0])
