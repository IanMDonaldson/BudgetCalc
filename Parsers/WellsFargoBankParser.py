import tabulate
import pdfplumber

from Utils.ParserUtils import format_date, convert_currency_to_intstr, clean_description


# ['Date Posted', 'Transaction Name', 'Deposits', 'Withdrawals', 'Balance']
def create_bank_table(filename):
    transactions = []
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
            transactions.append([date, description, deposit, balance, 'WFBank'])
        else:
            transactions.append([date, description, "-" + withdrawal, balance, 'WFBank'])

    return sorted(transactions, key=lambda transaction: transaction[0])

# print(tabulate.tabulate(create_bank_table('C:\\Users\\drago\\Downloads\\MarchLaurenBank.pdf')))
# print(tabulate.tabulate(create_bank_table('C:\\Users\\drago\\Downloads\\AprilLaurenBank.pdf')))
# print(tabulate.tabulate(create_bank_table('C:\\Users\\drago\\Downloads\\MayLaurenBank.pdf')))

# ther Wells Fargo Benefits
# Don't fall for an IRS imposter scam. Learn to spot scams and help avoid tax fraud at www.wellsfargo.com/spottaxscams.
# Statement period activity summary
# Beginning balance on 2/8 $2,638.49
# Deposits/Additions 2,860.14
# Withdrawals/Subtractions - 4,738.80
# Ending balance on 3/7 $759.83
# Number Description
# Deposits/
# Additions
# Withdrawals/
# Subtractions
# Ending daily
# balance
# 2/13 Zelle From Ian Donaldson on 02/13 Ref # Arv01Vv9Kxj6 Insurance 646.00
# 2/13 113Check 761.38 2,523.11
# 2/16 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,032.60 3,555.71
# 2/20 Online Transfer Ref #Ib0M97Mkks to Wells Fargo Cash Wise VISA
# Platinum Card Xxxxxxxxxxxx1956 on 02/16/24
# 1,292.00
# 2/20 Zelle to Matthew on 02/19 Ref #Rp0Rytrs33 Photos 95.00 2,168.71
# 2/22 Zelle to Matthew on 02/22 Ref #Rp0Rz3H9Zw April 27th Deposit 50.00 2,118.71
# 2/26 Online Transfer Ref #Ib0Mc7Cv57 to Wells Fargo Cash Wise VISA
# Platinum Card Xxxxxxxxxxxx1956 on 02/23/24
# 359.42
# 2/26 Online Transfer to Schmidt L Way2Save Savings xxxxxx4670 Ref
# #Ib0Mc7D4K9 on 02/23/24
# 1,000.00 759.29
# 3/1 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,181.54 1,940.83
# 3/5 ^ 115Brightwaters Apa Check Pmts 030524 0115 Ian Donaldson 1,181.00 759.83
# Ending balance on 3/7 759.83
# Totals $2,860.14 $4,738.80
# APRIL NEXT $$$$$$$$$$$$$$$$$$$$$$$
# Statement period activity summary
# Beginning balance on 3/8 $759.83
# Deposits/Additions 3,474.92
# Withdrawals/Subtractions - 777.02
# Ending balance on 4/5 $3,457.73
# Ending daily
# balance
# 3/15 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,116.50 1,876.33
# 3/19 Zelle From Ian Donaldson on 03/19 Ref # Arv01Wvwsv89
# Honeymoon and Rent
# 1,166.00 3,042.33
# 3/25 Zelle From Megan Trout on 03/23 Ref # 2Ph01Wzzicl0 A R T 25.00 3,067.33
# 3/29 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,167.42
# 3/29 Online Transfer Ref #Ib0Mpk46V4 to Wells Fargo Cash Wise
# VISA Platinum Card Xxxxxxxxxxxx1956 on 03/28/24
# 777.02 3,457.73
# Ending balance on 4/5 3,457.73
# Totals $3,474.92 $777.02
# MAY NEXT $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Statement period activity summary
# Beginning balance on 4/6 $3,457.73
# Deposits/Additions 2,149.08
# Withdrawals/Subtractions - 3,195.87
# Ending balance on 5/7 $2,410.94
# Ending daily
# balance
# 4/12 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,032.59 4,490.32
# 4/24 Online Transfer Ref #Ib0Mynrdtz to Wells Fargo Cash Wise VISA
# Platinum Card Xxxxxxxxxxxx1956 on 04/23/24
# 1,493.21
# 4/24 Online Transfer to Schmidt L Way2Save Savings xxxxxx4670 Ref
# #Ib0Mynrl6G on 04/23/24
# 1,437.66 1,559.45
# 4/26 Central Arkansas Payroll 02016 Lauren V. Schmidt 1,116.49 2,675.94
# 4/29 Zelle to Matthew on 04/27 Ref #Rp0S6Lblj2 Beautiful
# Gorgeous Wedding Photography
# 265.00 2,410.94
# Ending balance on 5/7 2,410.94
# Totals $2,149.08 $3,195.87
