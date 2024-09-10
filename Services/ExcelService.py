import xlsxwriter
import Repositories.TransactionRepository, Repositories.ClassificationRepository
from Repositories import TransactionRepository


def create_xl_from_dates(begin_date, end_date):
    classifications_and_count = (TransactionRepository
        .get_unique_classifications_and_count_between_dates(begin_date, end_date))
    # transaction_entries = TransactionRepository.get_transactions_and_classifications_between_dates(begin_date, end_date)
    workbook = xlsxwriter.Workbook(
        'ExpensesFrom{date1}-to-{date2}.xlsx'.format(date1=begin_date, date2=end_date)
    )
    worksheet = workbook.add_worksheet('Expenses')
    create_header(worksheet, "Classification", 'Date', 'Description', 'Bank Type', 'Amount')
    row, col = 1, 0
    sums = []
    '''Sort by classification, extract into separate lists, and for each separated list, sort by date and write it'''
    for classification, counter in classifications_and_count:
        transactions_by_classification = TransactionRepository.get_transactions_by_classification_and_date(classification, begin_date, end_date)
        if len(transactions_by_classification) != counter:
            raise Exception("number of transactions for classification doesn't match the transaction count function")
            break
        end_row = write_transactions_and_classification_to_sheet(worksheet, transactions_by_classification,
                                                       classification, counter, row)
        if end_row != row:
            worksheet.write(end_row, 3, 'TOTAL this Classification')
            worksheet.write(end_row, 4, '=SUM(E{start_row}:E{current_row})'.format(start_row=row+1, current_row=end_row))
            sums.append('E{num}'.format(num=end_row+1))
            row = end_row + 2
    worksheet.write(row+2, 0, 'Total This Month')
    worksheet.write(row+2, 1, '=SUM('+','.join([str(x) for x in sums])+')')
    workbook.close()


def write_transactions_and_classification_to_sheet(worksheet, transactions_by_classification,
                   classification, count, current_row):
    newrow = current_row
    worksheet.write(newrow, 0, classification)
    for transaction in transactions_by_classification:
        date = transaction[1]
        description = transaction[2].strip()
        amount = transaction[3]/100
        banktype = transaction[5]

        if (('Online Transfer' in description) or ('BILL PAY' in description) or
            ('CARDMEMBER SERV WEB PYMT' in description) or ('Rent' in description) or
             ('Zelle From Ian Donaldson' in description) or ('ZELLE' in description)):
            continue
        worksheet.write(newrow, 1, date)
        worksheet.write(newrow, 2, description)
        worksheet.write(newrow, 3, banktype)
        worksheet.write(newrow, 4, amount)
        newrow += 1
    return newrow


def write_total(worksheet, start_row, current_row):
    worksheet.write(current_row, 4, '=SUM(E{start_row}:E{current_row})'.format(start_row=start_row, current_row=current_row))
    # create_header(worksheet, "Classification", "Date", "description", "Amount", "Bank")
    # for transaction in transaction_entries:
    #     worksheet.write(row, col, transaction[4])
    #     worksheet.write(row, col + 1, transaction[0])
    #     worksheet.write(row, col + 2, transaction[1])
    #     worksheet.write(row, col + 3, transaction[2])
    #     worksheet.write(row, col + 4, transaction[3])
    #     col = 0
    #     row += 1
    # worksheet.write(row, 2, "=SUM(D:{lastrow}".format(lastrow=row - 1))
    # workbook.close()
    # return workbook

def create_header(worksheet, *args):
    row = 0
    col = 0
    for arg in args:
        worksheet.write(row, col, arg)
        col += 1

#create_xl_from_dates("04-05-2024", "05-05-2024")
# print(create_xl_from_dates("04-15-2024", "05-15-2024"))
