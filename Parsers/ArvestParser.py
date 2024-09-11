from Utils.ParserUtils import calculate_amount, convert_currency_to_int, format_date, clean_description
import re

final_transaction_balance = -1


def extract_begin_balance(text):
    regex_begin_balance = r"(\d\d\/\d\d\/\d\d\d\d)(?: +)(Beginning Balance)(?: +)(?:\$)([\d{1,3}|(?:\,)]+(?:\.)\d\d)"
    begin_bal_row = []
    match_beginning_balance = re.finditer(regex_begin_balance, text, re.MULTILINE)
    match = next(match_beginning_balance)
    date = format_date(match.group(1))
    desc = clean_description(match.group(2))
    return convert_currency_to_int(match.group(3))


def extract_transactions(text):
    previous_balance = extract_begin_balance(text)
    transactions = []
    if previous_balance == -1:
        return
    regex = r"(\d{1,2}\/\d{1,2}\/\d\d\d\d)(?: +)(.+)(?: )(?:\$[\d{1,3}|(?:\,)]+(?:\.)\d\d)(?: +)(?:\$)([\d{1,3}|(?:\,)]+(?:\.)\d\d)"
    matches = re.finditer(regex, text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        date = format_date(match.group(1))
        description = clean_description(match.group(2))
        balance = convert_currency_to_int(match.group(3))
        amount = calculate_amount(previous_balance, balance)
        previous_balance = balance
        transactions.append([date, description, amount, balance, 'Arvest'])

    global final_transaction_balance
    final_transaction_balance = transactions.pop()[3]
    return sorted(transactions, key=lambda transaction: transaction[0])


def extract_ending_balance(text):
    regex = r'(\d\d\/\d\d\/\d\d\d\d)(?: +)(Ending Balance)(?: +)(?:\$)(.+)'
    matches = re.finditer(regex, text, re.MULTILINE)
    ending_balance = []
    for matchNum, match in enumerate(matches, start=0):
        date = format_date(match.group(1))
        desc = clean_description(match.group(2))
        bal = convert_currency_to_int(match.group(3))
        ending_balance = [date, desc, '', bal, 'Arvest']
    return ending_balance


# ['Date Posted', 'Transaction Name', 'Amount', 'Ending Balance', 'Bank Type']
def create_table(text):
    transaction_table = []
    ## required for
    beginning_balance = extract_begin_balance(text)
    transaction_list = extract_transactions(text)
    ending_balance = extract_ending_balance(text)
    if ending_balance[3] != final_transaction_balance:
        print("Error - final transaction or ending balance not parsed correctly")
        return
    for row in transaction_list:
        transaction_table.append(row)

    return transaction_table
