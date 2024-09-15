from Parsers import ArvestParser, TargetParser, UsBankParser, WellsFargoBankParser, WellsFargoCreditCardParser, WellsFargoSavingsParser
from Utils.ParserUtils import return_pages_text_pdfium, return_text_for_all_pages
from tabulate import tabulate

# print(tabulate(ArvestParser.create_table(return_pages_text_pdfium("..\\..\\bankStatements\\June\\EStatement-2024-06-16-66272.pdf"))))
# print(tabulate(TargetParser.extractLines(return_pages_text_pdfium("..\\..\\bankStatements\\June\\eStatementJulyTarget.pdf"))))
# print(tabulate(UsBankParser.extractLines("..\\..\\bankStatements\\June\\2024-07-03 Statement - USB Credit Card 7031.pdf")))
# print(tabulate(WellsFargoBankParser.create_bank_table("..\\..\\bankStatements\\June\\_070824 WellsFargo.pdf")))
# print(tabulate(WellsFargoCreditCardParser.extract_credit_card_lines(return_pages_text_pdfium("..\\..\\bankStatements\\June\\JuneWFCC.pdf"))))
print(tabulate(WellsFargoSavingsParser.create_table("..\\..\\bankStatements\\June\\JuneWFSav.pdf")))

