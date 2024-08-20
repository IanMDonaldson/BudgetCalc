import sqlite3
from Consts import DATABASE
from Utils.ParserUtils import clean_description

def insert_trans_class(transaction_id, classification_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO Trans_Classification (classification_id, transaction_id) "
                "Values (?, ?)", (classification_id, transaction_id))
    conn.commit()
    cur.close()
    conn.close()


def update_classification_id(class_id, trans_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE Trans_Classification "
                "SET classification_id = ? "
                "WHERE transaction_id = ?", (class_id, trans_id))
    conn.commit()
    cur.close()
    conn.close()


def update_transaction_id(class_id, trans_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE Trans_Classification "
                "SET transaction_id = ? "
                "WHERE classification_id = ?", (trans_id, class_id))
    conn.commit()
    cur.close()
    conn.close()
