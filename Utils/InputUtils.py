# Go Between from DB and CSV
from Parsers import (ArvestParser, TargetParser, UsBankParser, WellsFargoBankParser,
                     WellsFargoCreditCardParser, WellsFargoSavingsParser)
from Repositories import TransactionRepository
from Utils.ParserUtils import return_pages_text_pdfium, return_text_for_all_pages
from Utils.DatabaseUtils import insert_helper
from Services import ExcelService


def handle_input(filename):
    pdfium_text = return_pages_text_pdfium(filename)
    pdfreader_text = return_text_for_all_pages(filename)
    if "FREE BLUE XXXXXXXX3977" in pdfium_text:
        table = ArvestParser.create_table(pdfium_text)
        if not insert_helper(table, TransactionRepository):
            return
    elif "PORTIONWITHYOURPAYMENTMADEPAYBLETOTARGETCARDSERVICE" in pdfium_text:
        table = TargetParser.extractLines(pdfium_text)
        if not insert_helper(table, TransactionRepository):
            return
    elif "U.S. Bank National Association" in pdfium_text:
        table = UsBankParser.extractLines(filename)
        if not insert_helper(table, TransactionRepository):
            return
    elif "Wells Fargo Everyday Checking" in pdfium_text:
        table = WellsFargoBankParser.create_bank_table(filename)
        if not insert_helper(table, TransactionRepository):
            return
    elif "WELLS FARGO CASH WISE VISA" in pdfium_text:
        table = WellsFargoCreditCardParser.extract_credit_card_lines(pdfium_text)
        if not insert_helper(table, TransactionRepository):
            return
    elif "Wells Fargo Way2Save" in pdfium_text:
        table = WellsFargoSavingsParser.create_table(filename)
        if not insert_helper(table, TransactionRepository):
            return
    else:
        raise Exception("Statement Type Not Found")
    return "Success for filename: {filename}".format(filename)

def handle_csv():
    start_date = input("What would you like the start date to be: ")
    end_date = input("What would you like the end date to be: ")
    csvfile = ExcelService.create_xl_from_dates(start_date, end_date)
