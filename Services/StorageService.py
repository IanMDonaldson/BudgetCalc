import sqlite3

from Consts import DATABASE
from Repositories import TransactionRepository, ClassificationRepository, TransClassRepository
from UI import UIFunctions


# debug helper function for when stuff goes wrong
def create_classifications_from_transactions():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    transactions = TransactionRepository.get_transactions()
    for transaction in transactions:
        result = con.execute("select * from Classification where trans_description = ?", (transaction[2],))
        con.commit()
        if result.fetchall():
            continue
        print("transaction is: " + str(transaction))
        con.execute("""INSERT INTO Classification (classification_id, classification, trans_description)
        VALUES (?, ?, ?)""", (transaction[0], input("Classification: "), transaction[2]))
        con.commit()
    result = cur.fetchall()
    cur.close()
    con.close()


def insert_transaction_and_classification(row):
    trans_date, trans_description, trans_amount, trans_balance, trans_banktype = row[0], row[1], row[2], row[3], row[4]

    transaction_row = []
    classification_rows = ClassificationRepository.get_classification_by_description(trans_description)
    if len(classification_rows) > 1:
        raise Exception("classification exists more than once, clean DB please", str(classification_rows))
    elif len(classification_rows) == 0:
        # classification does NOT exist, need transaction ID
        classification_name = UIFunctions.create_classification_input_dialog(trans_description)
        # If transaction already exists, just insert classification, otherwise we need to insert transaction to get transid

        stored_transaction = TransactionRepository.get_transaction_by_all(trans_date, trans_description,
                                                                          trans_amount, trans_balance,
                                                                          trans_banktype)
        # return value indicates identical transaction, passing -1 all the way down to the root to skip this file
        if stored_transaction == -1:
            return False
        elif stored_transaction:
            inserted_classification_row = ClassificationRepository.insert_classification(
                classification_name, trans_description)[0]
            TransClassRepository.insert_trans_class(transaction_id=stored_transaction[0],
                                                    class_id=inserted_classification_row[0])
        else:
            inserted_transaction_row = TransactionRepository.insert_transaction(row)[0]
            classification_row = ClassificationRepository.insert_classification(classification_name,
                                                                                trans_description)[0]
            TransClassRepository.insert_trans_class(trans_id=inserted_transaction_row[0],
                                                    class_id=classification_row[0])
    else:
        classification_row = classification_rows[0]
        # Classification exists, see if transaction exists
        stored_transaction = TransactionRepository.get_transaction_by_all(trans_date, trans_description,
                                                                          trans_amount, trans_balance,
                                                                          trans_banktype)
        if stored_transaction == -1:
            return False
        elif stored_transaction:
            # classification exists, transaction exists...now check if transclassrepo entry exists
            if not TransClassRepository.does_trans_class_exist(trans_id=stored_transaction[0],
                                                               class_id=classification_row[0]):
                TransClassRepository.insert_trans_class(trans_id=stored_transaction[0],
                                                        class_id=classification_row[0])
        else:
            # insert transaction, map the new transaction to the existing classification
            inserted_transaction_row = TransactionRepository.insert_transaction(row)[0]
            TransClassRepository.insert_trans_class(trans_id=inserted_transaction_row[0],
                                                    class_id=classification_row[0])
    return True
