import re

import pdfplumber
from Utils.ParserUtils import format_date, convert_currency_to_int, clean_description


# ['Date Posted', 'Transaction Name', 'Amount', 'Balance']
def extractLines(filename):
    (transactions, sum) = get_transactions_text(filename)

    if credits_exist(filename):
        card_credits = append_credits(filename, sum)
        for credit in card_credits:
            transactions.append(credit)

    print(transactions)
    return sorted(transactions, key=lambda transaction: transaction[0])


def get_transactions_text(filename):
    pdf = pdfplumber.open(filename)
    text = ''
    for page in pdf.pages[3:5]:
        text += page.extract_text()
    transactions = []
    sum = 0
    regex = r"(\d\d\/\d\d)(?: \d\d\/\d\d \d\d\d\d )([^\n]*)(?:\$)([\d{1,3}|(?:\,)]+(?:\.)\d\d)|(\d\d\/\d\d)(?: \d\d\/\d\d \d\d\d\d )([^\n]+).+\n.+\n.+\n.+\n(?:\$)([\d{1,3}|(?:\,)]+(?:\.)\d\d\n)"
    matches = re.finditer(regex, text, flags=re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        post_date = format_date(match.group(1)[:5])
        name = clean_description(match.group(2))
        amount = -convert_currency_to_int(match.group(3))
        sum += amount
        transactions.append([post_date, name, amount, sum, 'USBank'])

    return (transactions, sum)


def append_credits(filename, sum):
    card_credits = []
    pdf = pdfplumber.open(filename)

    # Grab the Payments and Credits till the total line
    # differentiating credits and transactions on the same page is too hard of a regex
    fake_text = ''
    for page in pdf.pages[2:4]:
        fake_text += page.extract_text()
    payments_found = False
    real_text = ''
    for line in fake_text.split('\n'):
        if "Payments and Other Credits" in line:
            payments_found = True
        elif re.match(r"TOTAL THIS PERIOD \$[\d{1,3}|(?:\,)]+(?:\.)\d\dCR", line):
            break
        elif payments_found:
            real_text += line + '\n'

    regex = r'^(\d\d\/\d\d)(?:[^A-Za-z]+)([^\n]+)(?:\$)([\d{1,3}|(?:\,)]+(?:\.)\d\d)(?=CR)'
    matches = re.finditer(regex, real_text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        if match.group(1):
            name = clean_description(match.group(2))
            if 'PAYMENT THANK YOU' in name:
                continue
            post_date = format_date(match.group(1)[:7])
            amount = convert_currency_to_int(match.group(3))
            sum += amount
            card_credits.append([post_date, name, amount, sum, 'WFCard'])
        else:
            print(match.group(1))
            print(match.group(2))
            print(match.group(3))
            print(match.group(4))
            print(match.group(5))
            print(match.group(6))

    return card_credits


def credits_exist(filename):
    pdf = pdfplumber.open(filename)
    page = pdf.pages[0]
    text = page.extract_text()
    match = re.findall(r'(Other Credits +-+ +\$[\d{1,3}|(?:\,)]+(?:\.)\d\d)', text)
    if match and '$0.00' not in match:
        return True
    return False

# print(tabulate.tabulate(extractLines('C:\\Users\\drago\\Downloads\\usbankMay.pdf')))
# print(tabulate.tabulate(extractLines('C:\\Users\\drago\\Downloads\\usbankApril.pdf')))
# print(tabulate.tabulate(extractLines('C:\\Users\\drago\\Downloads\\JulyUSBank.pdf')))
#
# # print(tabulate.tabulate(extractLines(return_pages_text_pdfium('C:\\Users\\drago\\Downloads\\usbankMay.pdf'))))
# print(tabulate.tabulate(extractLines(return_pages_text_pdfium('C:\\Users\\drago\\Downloads\\usbankApril.pdf'))))
# print(tabulate.tabulate(extractLines(return_pages_text_pdfium('C:\\Users\\drago\\Downloads\\JulyUSBank.pdf'))))
