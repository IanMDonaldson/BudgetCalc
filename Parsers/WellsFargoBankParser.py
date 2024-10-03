import pdfplumber

from Utils.ParserUtils import format_date, convert_currency_to_intstr, clean_description


# ['Date Posted', 'Transaction Name', 'Deposits', 'Withdrawals', 'Balance']
def create_bank_table(filename):
    transactions = []
    prev_balance = 0
    pdf = pdfplumber.open(filename)
    page = pdf.pages[1]
    crop_page = page.within_bbox((0, page.height * 0.17, page.width, 0.5 * float(page.height)))
    table = crop_page.extract_table({"explicit_vertical_lines": [63, 115, 152, 400, 470, 526, 570]})
    for row in table:
        if 'Ending balanc' in row[0]:
            break
        date = format_date(row[0])
        description = clean_description(row[2])
        deposit = convert_currency_to_intstr(row[3])
        withdrawal = convert_currency_to_intstr(row[4])
        balance = convert_currency_to_intstr(row[5])
        if deposit:
            if balance:
                prev_balance = balance
            else:
                balance = int(prev_balance) + int(deposit)
                prev_balance = balance
            transactions.append([date, description, deposit, balance, 'WFBank'])
        else:
            if balance:
                prev_balance = balance
            else:
                balance = int(prev_balance) - int(withdrawal)
                prev_balance = balance
            transactions.append([date, description, "-" + withdrawal, balance, 'WFBank'])

    return sorted(transactions, key=lambda transaction: transaction[0])
