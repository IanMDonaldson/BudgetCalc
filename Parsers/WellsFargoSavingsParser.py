import tabulate
import pdfplumber
from Utils.ParserUtils import convert_currency_to_intstr, format_date, clean_description


# ['Date Posted', 'Transaction Name', 'Deposits', 'Withdrawals', 'Balance']
def create_table(filename):
    transactions = []
    pdf = pdfplumber.open(filename)
    page = pdf.pages[1]
    crop_page = page.within_bbox((0, page.height*0.17, page.width, 0.5*float(page.height)))
    table = crop_page.extract_table({"explicit_vertical_lines":[60, 100,400,470,526, 565]})
    for row in table:
        if 'Ending bal' in row[0]:
            break
        date = format_date(row[0])
        description = clean_description(row[1])
        deposit = convert_currency_to_intstr(row[2])
        withdrawal = convert_currency_to_intstr(row[3])
        balance = convert_currency_to_intstr(row[4])
        if deposit:
            transactions.append([date, description, deposit, balance, 'WFSavings'])
        else:
            transactions.append([date,description, "-"+withdrawal, balance, "WFSavings"])

    return sorted(transactions, key=lambda transaction: transaction[0])






# print(tabulate.tabulate(create_table('C:\\Users\\drago\\Downloads\\marchLaurenSavings.pdf')))
# print(tabulate.tabulate(create_table('C:\\Users\\drago\\Downloads\\AprilLaurenSavings.pdf')))
# print(tabulate.tabulate(create_table('C:\\Users\\drago\\Downloads\\MayLaurenSavings.pdf')))


# text = """Ending daily
# balance
# 5/14 Online Transfer From Schmidt L Everyday Checking xxxxxx6399 Ref
# #Ib0N7587Kj on 05/14/24
# 1,499.83 29,500.00
# 5/31 Interest Payment 0.25
# 5/31 Federal Tax Withheld 0.06 29,500.19
# Ending balance on 5/31 29,500.19
# Totals $1,500.08 $0.06
# The Ending Daily Balance does not reflect any pending withdrawals or holds on deposited funds
# Statement period activity summary
# Beginning balance on 5/1 $28,000.17
# Deposits/Additions 1,500.08
# Withdrawals/Subtractions - 0.06
# Ending balance on 5/31 $29,500.19
# Ending daily
# balance
# 4/24 Online Transfer From Schmidt L Everyday Checking xxxxxx6399 Ref
# #Ib0Mynrl6G on 04/23/24
# 1,437.66 28,000.00
# 4/30 Interest Payment 0.22
# 4/30 Federal Tax Withheld 0.05 28,000.17
# Ending balance on 4/30 28,000.17
# Totals $1,437.88 $0.05
# The Ending Daily Balance does not reflect anStatement period activity summary
# Beginning balance on 4/1 $26,562.34
# Deposits/Additions 1,437.88
# Withdrawals/Subtractions - 0.05
# Ending balance on 4/30 $28,000.17
# balance
# 3/20 Mobile Deposit : Ref Number :021190852794 6.51 26,562.16
# 3/29 Interest Payment 0.23
# 3/29 Federal Tax Withheld 0.05 26,562.34
# Ending balance on 3/31 26,562.34
# Totals $6.74 $0.05
# The Ending Daily Balance does
# Beginning balance on 3/1 $26,555.65
# Deposits/Additions 6.74
# Withdrawals/Subtractions - 0.05
# Ending balance on 3/31 $26,562.34"""


# def extract_begin_balance_savings(text):
#     beginning_balance_row = []
#     regex = r'(Beginning[ +]balance)[\s+]on[\s+](\d{1,2}\/\d{1,2})[\s+](?:\$)([\d|\,]+\.\d\d)'
#     matches = re.finditer(regex, text, re.MULTILINE)
#     for matchNum, match in enumerate(matches, start=0):
#         name = match.group(1)
#         date = match.group(2)
#         begin_balance = match.group(3)
#         beginning_balance_row = [date, name, '', begin_balance]
#     return beginning_balance_row
#
#
# def extract_transfers_or_mobile_deposit(text):
#     rows = []
#     regex = r'(\d{1,2}\/\d{1,2})(?:\s+)(.+\n.+\d\d\/\d\d\/\d\d)(?:\s+)([\d{1,3}|(?:\,)]+(?:\.)\d\d)(?:\s+)([\d|\,]+\.\d\d)|(\d{1,2}\/\d{1,2})(?: +)(.+\:+\d+ +)([\d{1,3}|(?:\,)]+(?:\.)\d\d)(?: +)([\d{1,3}|(?:\,)]+(?:\.)\d\d)'
#     matches = re.findall(regex, text, re.MULTILINE)
#     for match in matches:
#         print('values begin for mobile/transfer')
#         for i in range(len(match)):
#             if match[i] != '':
#                 print(match[i])
#                 date = match[i]
#                 print(match[i + 1])
#                 name = match[i + 1]
#                 print(match[i + 2])
#                 amount = match[i + 2]
#                 print(match[i + 3])
#                 balance = match[i + 3]
#                 rows = [date, name, amount, balance]
#                 break
#     return rows
#
#
# def extract_interest(text):
#     interest = []
#     regex = r'(\d{1,2}\/\d{1,2})(?: +)(Interest(?: +)Payment(?: +))([\d{1,3}|(?:\,)]+(?:\.)\d\d)'
#     matches = re.findall(regex, text, re.MULTILINE)
#     for match in matches:
#         print('values for interest begin')
#         for i in range(len(match)):
#             if match[i] != '':
#                 date = match[i]
#                 name = match[i + 1]
#                 amount = match[i + 2]
#                 interest = [date, name, amount, '']
#                 break
#     return interest
#
#
# def extract_date_name_amount_balance(text):
#     trans = []
#     regex = r'(\d{1,2}\/\d{1,2})(?: +)(.+)(?: )([\d{1,3}|(?:\,)]+(?:\.)\d\d)(?: *)([\d{1,3}|(?:\,)]+(?:\.)\d\d)'
#     matches = re.findall(regex, text, re.MULTILINE)
#     for match in matches:
#         print('values for generic transactions begin')
#         for i in range(len(match)):
#             if match[i] != '':
#                 date = match[i]
#                 name = match[i + 1]
#                 amount = match[i + 2]
#                 balance = match[i + 3]
#                 trans = [date, name, amount, balance]
#                 break
#     return trans
#
#
# def extract_ending_balance(text):
#     ending_balance_row = []
#     regex = r'(Ending[ +]balance)[\s+]on[\s+](\d{1,2}\/\d{1,2})[\s+](?:\$)([\d|\,]+\.\d\d)'
#     matches = re.finditer(regex, text, re.MULTILINE)
#     for matchNum, match in enumerate(matches, start=0):
#         name = match.group(1)
#         date = match.group(2)
#         ending_balance = match.group(3)
#         ending_balance_row = [date, name, '', ending_balance]
#     return ending_balance_row
#
#
# def create_savings_table(filename):
#     transaction_table = [['Date Posted', 'Transaction Name', 'Amount', 'Balance']]
#     text = return_pages_text_pdfium(filename)
#     print('begin balance below')
#     print(extract_begin_balance_savings(text))
#     print('mobile/transfers below')
#     transfers = extract_transfers_or_mobile_deposit(text)
#     print(transfers)
#
#     print('interest below')
#     interest = extract_interest(text)
#     print(interest)
#
#     print('generic below')
#     generics = extract_date_name_amount_balance(text)
#     print(generics)
#
#     print('ending balance below')
#     print(extract_ending_balance(text))
#     transaction_table.append(extract_begin_balance_savings(text))
#     if transfers:
#         transaction_table.append(transfers)
#     if interest:
#         transaction_table.append(interest)
#     if generics:
#         transaction_table.append(generics)
#     transaction_table.append(extract_ending_balance(text))
#     return transaction_table