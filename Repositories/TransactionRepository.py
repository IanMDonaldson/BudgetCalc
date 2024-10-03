import sqlite3
import tkinter.messagebox

from Consts import DATABASE
from Utils.ParserUtils import clean_description


def get_transaction_by_all(date, desc, amount, balance, btype):
    transByNoBal = sorted(get_transactions_where_balance_null(date, desc, amount, btype),
                          key=lambda transaction: transaction[0])
    if len(transByNoBal) > 1:
        # now multiple transactions on the same day...just sort by transaction ID and we should just be able to insert the
        #   balance and be sure it's inserted earlier than the next one but debug just to be sure
        for trans in transByNoBal:
            result = update_transaction(trans[0], balance)
            return result[0]
    elif len(transByNoBal) == 1:
        result = update_transaction(transByNoBal[0][0], balance)
        return result[0]
    else:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT * from Transactions "
                    "WHERE (date, description, amount, balance, bank_type) = (?, ?, ?, ?, ?)",
                    (date, desc, amount, balance, btype))
        result = cur.fetchall()
        if len(result) > 1:
            tkinter.messagebox.showerror('''Duplicate Transactions", "There are duplicate Transactions:
            {result}
            for filename {filename}'''.format(str(result), filename))
            cur.close()
            con.close()
            return -1
        elif len(result) == 1:
            row = result[0]
            cur.close()
            con.close()
            return row
        cur.close()
        con.close()
        return result  # will be empty array


def get_transactions_where_balance_null(date, desc, amount, btype):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions "
                "WHERE (date, description, amount, bank_type) = (?, ?, ?, ?) AND (balance is null OR balance = '')",
                (date, desc, amount, btype))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result  # will be none


def get_transactions():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions")
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_transactions_by_date(date):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions where date = ?", (date,))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def insert_transactions(transactions):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.executemany("INSERT into Transactions (date, description, amount, balance, bank_type)"
                    "VALUES (?, ?, ?, ?, ?)", transactions)
    con.commit()
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def insert_transaction(transaction):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    print(transaction)
    cur.execute("INSERT into Transactions (date, description, amount, balance, bank_type)"
                "VALUES (?, ?, ?, ?, ?) RETURNING *",
                (transaction[0], transaction[1], transaction[2], transaction[3], transaction[4]))
    result = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return result


def get_transactions_between_dates(date1, date2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions t where t.date BETWEEN ? AND ?", (date1, date2))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_transactions_and_classifications_between_dates(date1, date2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('''select c.classification, t.transaction_id, t.date, t.description, t.amount, t.balance, t.bank_type
        from Transactions t
        JOIN Trans_Classification tc on t.transaction_id = tc.transaction_id
        JOIN Classification c on tc.classification_id = c.classification_id
        WHERE t.date between '03-01-2024' and '03-15-2024'
        order by c.classification, t.date''', (date1, date2))
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


def get_unique_classifications_and_count_between_dates(date1, date2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('''select c.classification, count(c.classification) counter
        from Transactions t
        JOIN Trans_Classification tc on tc.transaction_id = t.transaction_id
        JOIN Classification c on tc.classification_id = c.classification_id
        WHERE t.date between ? AND ?
        group by c.classification''', (date1, date2))
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


def get_transactions_by_classification_and_date(classification, begin_date, end_date):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('''select *
        from Transactions t
        join Trans_Classification tc on tc.transaction_id = t.transaction_id
        join Classification c on c.classification_id = tc.classification_id
        where t.date between ? AND ? AND c.classification = ?
        order by t.date''', (begin_date, end_date, classification))
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


# Don't use, only for fixing and debugging stuff
def cleanup_descriptions():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions")
    result = cur.fetchall()

    for transaction in result:
        cur.execute("""UPDATE Transactions
        SET description = ?
        WHERE transaction_id = ?
        """, (clean_description(transaction[2]), transaction[0]))

        con.commit()

    cur.close()
    con.close()
    return result


def check_unique():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT c.classification, count(c.classification) counter "
                "FROM Classification c "
                "Group BY c.classification;")
    results = cur.fetchall()
    print(results)
    cur.close()
    con.close()
    return results


def update_transaction(id, balance):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute('''UPDATE Transactions
    SET balance = ?
    WHERE transaction_id = ?
    RETURNING *''', (balance, id))
    result = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return result

# get_transaction_by_all('06-20-2024', 'CMSVENDCV ', -260, 0, 'USBank')
# get_transaction_by_all('06-20-2024', 'CMSVENDCV ', -260, -260, 'USBank')
# get_transaction_by_all('02-20-2024', 'Zelle to Matthew on Photos', -9500, 216871, 'WFBank')
# get_transaction_by_all(date, desc, amount, balance, btype)
# get_transaction_by_all(date, desc, amount, balance, btype)
