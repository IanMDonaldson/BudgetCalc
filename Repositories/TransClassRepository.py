import sqlite3

from Consts import DATABASE


def insert_trans_class(trans_id, class_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO Trans_Classification (transaction_id, classification_id) "
                "Values (?, ?)", (trans_id, class_id))
    conn.commit()
    cur.close()
    conn.close()


def get_all_between_dates(date1, date2):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''select *
        from Transactions t
        JOIN Trans_Classification tc on t.transaction_id = tc.transaction_id
        JOIN Classification c on tc.classification_id = c.classification_id
        WHERE t.date between ? and ?
        order by c.classification''', (date1, date2))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def update_classification_id(trans_id, class_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE Trans_Classification "
                "SET classification_id = ? "
                "WHERE transaction_id = ?", (class_id, trans_id))
    conn.commit()
    cur.close()
    conn.close()


def update_transaction_id(trans_id, class_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE Trans_Classification "
                "SET transaction_id = ? "
                "WHERE classification_id = ?", (trans_id, class_id))
    conn.commit()
    cur.close()
    conn.close()


def does_trans_class_exist(trans_id, class_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * from Trans_Classification "
                "WHERE transaction_id = ? AND classification_id = ?", (trans_id, class_id))
    results = cur.fetchall()
    if results:
        cur.close()
        conn.close()
        return True
    cur.close()
    conn.close()
    return False
