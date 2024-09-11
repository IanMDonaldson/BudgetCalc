import tabulate
from Utils.ParserUtils import return_pages_text_pdfium, convert_currency_to_int, format_date, clean_description
import re


# ['Date Posted', 'Transaction Name', 'Amount', 'Balance', 'Bank Type']
def extract_credit_card_lines(text):
    transactions = []
    sum = 0
    # Card Credits are always first
    card_credits, sum = extract_credits(text, sum)
    if card_credits:
        for credit in card_credits:
            transactions.append(credit)
    regex = r'(.{5})((?:.{19}))((?<=(?:\d{4} \d\d\/\d\d \d\d\/\d\d\s[A-Z0-9]{17}\s))(.*)(?=(?:\s[0-9]*\.[0-9]{2})))( [0-9]*\.[0-9]{2})'
    matches = re.finditer(regex, text, re.MULTILINE)
    counter = 0
    for matchNum, match in enumerate(matches, start=0):
        if counter < len(card_credits):
            counter += 1
            continue

        post_date = format_date(match.group(1)[:7])
        name = clean_description(match.group(4))
        amount = -convert_currency_to_int(match.group(5))
        sum += amount
        transactions.append([post_date, name, amount, sum, 'WFCard'])

    return sorted(transactions, key=lambda transaction: transaction[0])


def extract_credits(text, sum):
    card_credits = []
    extracted_lines = ""
    lines = text.splitlines()
    text_length = len(lines)
    i = 0
    while i < text_length:
        match = re.findall(r'(Other Credits)(?! \$[\d{1,3}|(?:\,)]+(?:\.)\d\d)', lines[i])
        if match and '$0.00' not in lines[i]:
            for j in range(i+1, text_length):
                if 'CREDITS FOR THIS PERIOD' in str(lines[j]):
                    break
                extracted_lines += lines[j] + "\n"
                i = j
        if extracted_lines:
            break
        i += 1

    regex = r'(.{5})((?:.{19}))((?<=(?:\d{4} \d\d\/\d\d \d\d\/\d\d\s[A-Z0-9]{17}\s))(.*)(?=(?:\s[0-9]*\.[0-9]{2})))( [0-9]*\.[0-9]{2})'
    matches = re.finditer(regex, extracted_lines, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        post_date = format_date(match.group(1)[:7])
        name = clean_description(match.group(4))
        amount = convert_currency_to_int(match.group(5))
        sum += amount
        card_credits.append([post_date, name, amount, sum, 'WFCard'])

    return card_credits, sum



def extract_credit_card_lines_test(filename):
    text = return_pages_text_pdfium(filename)
    transactions = []
    regex = r'(.{5})((?:.{19}))((?<=(?:\d{4} \d\d\/\d\d \d\d\/\d\d\s[A-Z0-9]{17}\s))(.*)(?=(?:\s[0-9]*\.[0-9]{2})))( [0-9]*\.[0-9]{2})'
    matches = re.finditer(regex, text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=0):
        post_date = format_date(match.group(1)[:7])
        name = clean_description(match.group(4))
        amount = -convert_currency_to_int(match.group(5))
        transactions.append([post_date, name, amount, '', 'WFCard'])

    card_credits = extract_credits(text)
    if card_credits:
        for credit in card_credits:
            index = transactions.index(credit)
            transactions[index][2] *= -1

    return sorted(transactions, key=lambda transaction: transaction[0])

# print(tabulate.tabulate(extract_credit_card_lines_test("C:\\Users\\drago\\Downloads\\MayWellsFargo.pdf")))
# print(tabulate.tabulate(extract_credit_card_lines_test("C:\\Users\\drago\\Downloads\\AprilWellsFargo.pdf")))
# print(tabulate.tabulate(extract_credit_card_lines_test("C:\\Users\\drago\\Downloads\\MarchWellsFargo.pdf")))




