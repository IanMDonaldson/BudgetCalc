import sqlite3
from Consts import DATABASE
from Utils.ParserUtils import clean_description
#TODO change join statements to join on classification description and trans description instead of id :)

def get_transactions():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions")
    result = cur.fetchall()
    cur.close()
    return result


def get_transactions_by_date(date):
    print(date)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Transactions where date = ?", (date,))
    result = cur.fetchall()
    cur.close()
    return result


def insert_transactions(transactions):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.executemany("INSERT into Transactions (date, description, amount, balance, bank_type)"
                    "VALUES (?, ?, ?, ?, ?)", transactions)
    con.commit()
    result = cur.fetchall()
    cur.close()
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
    cur.execute("SELECT * from Transactions where date BETWEEN date(?) AND date(?)", (date1, date2))
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_transactions_and_classifications_between_dates(date1, date2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT c.classification, t.date, t.description, t.amount, t.bank_type "
                "FROM Transactions t "
                "INNER JOIN Classification c on t.description = c.trans_description "
                "WHERE t.date BETWEEN ? and ?", (date1, date2))
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


def get_unique_classifications_and_count_between_dates(date1, date2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT c.classification, count(c.classification) counter "
        "FROM Transactions t "
        "JOIN Classification c on t.transaction_id = c.classification_id "
        "WHERE t.date between ? and ? "
        "Group BY c.classification;", (date1, date2))
    results = cur.fetchall()
    cur.close()
    con.close()
    return results


def get_transactions_by_classification_and_date(classification, begin_date, end_date):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT t.date, t.description, t.amount, t.bank_type "
                "FROM Transactions t "
                "JOIN Classification c on t.description = c.trans_description "
                "WHERE t.date between ? and ? "
                "AND c.classification = ?", (begin_date, end_date, classification))
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



# cleanup_descriptions()
# check_unique()