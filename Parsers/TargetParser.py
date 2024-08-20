import tabulate

from Utils.ParserUtils import convert_currency_to_int, return_pages_text_pdfium, abbr_to_month, format_date, \
    clean_description
import re

#['Date Posted', 'Transaction Name', 'Amount', 'Balance', 'BankType']
def extractLines(text):
    transactions = []
    regex = r"(\D{3}\. \d\d)((?<= \d\d)(.*)(?=\$))(\$.+)"
    matches = re.finditer(regex, text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        post_date = format_date(abbr_to_month(match.group(1)[:7].replace(". ",'/')))
        name = clean_description(match.group(3))
        amount = -convert_currency_to_int(match.group(4))
        transactions.append([post_date, name, amount, '', 'Target'])
    return sorted(transactions, key=lambda transaction: transaction[0])


# print(tabulate.tabulate(extractLines('C:\\Users\\drago\\Downloads\\targetMayeStatement.pdf')))

