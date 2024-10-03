import sqlite3

from Consts import DATABASE
from Utils.ParserUtils import clean_description


def get_classifications():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Classification")
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_unique_classifications():
    con = sqlite3.connect(DATABASE)
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    cur.execute('''select c.classification
        from Classification c
        group by c.classification''')
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


def get_classification_by_description(description):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("select * from Classification where trans_description = ?", (description,))
    results = cur.fetchall()

    cur.close()
    con.close()
    return results


def insert_classifications(classifications):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.executemany("INSERT into Classification (classification, trans_description)"
                    "VALUES (?, ?, ?) returning *", classifications)
    result = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return result


def insert_classification(classification_name, transaction_description):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT into Classification (classification, trans_description)"
                "VALUES (?, ?) RETURNING *", (classification_name, transaction_description))
    result = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return result


def cleanup_descriptions():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Classification")
    result = cur.fetchall()

    for classification in result:
        con.execute("""UPDATE Classification
        SET trans_description = ?
        WHERE classification_id = ?
        """, (clean_description(classification[2]), classification[0]))
        con.commit()

    cur.close()
    con.close()
    return result


def cap_class():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from Classification")
    result = cur.fetchall()

    for classification in result:
        print(classification)
        con.execute("""UPDATE Classification
        SET classification = ?
        WHERE classification_id = ?
        """, (classification[1].upper(), classification[0]))
        con.commit()

    cur.close()
    con.close()
    return result
