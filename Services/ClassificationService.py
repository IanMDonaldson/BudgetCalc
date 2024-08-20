import sqlite3

from Consts import DATABASE
from Repositories import TransactionRepository, ClassificationRepository, TransClassRepository
from UI import UIFunctions


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
    date = row[0]
    description = row[1]
    transaction_row = []
    classification_row = ClassificationRepository.get_classification_by_description(description)
    # classification does NOT exist, need transaction ID
    if not classification_row:
        classification_name = UIFunctions.create_classification_input_dialog(description)
        transaction_row = set(row).intersection(TransactionRepository.get_transactions_by_date(date))
        # If transaction already exists, just insert classification, otherwise we need to insert transaction to get transid
        if transaction_row:
            classification_row = ClassificationRepository.insert_classification(classification=[
                transaction_row[0],
                classification_name,
                transaction_row[2]])
            TransClassRepository.insert_trans_class(transaction_id= transaction_row[0],
                                                    classification_id= classification_row[0])
        else:
            transaction_row = TransactionRepository.insert_transaction(row)[0]
            classification_row = ClassificationRepository.insert_classification(classification=[
                transaction_row[0],
                classification_name,
                transaction_row[2]])
            TransClassRepository.insert_trans_class(transaction_id= transaction_row[0],
                                                    classification_id= classification_row[0])
    else: # Classification does actually exist, see if transaction exists
        transaction_row = set(row).intersection(TransactionRepository.get_transactions_by_date(date))
        #transaction does not exist while classification DOES exist
        if not transaction_row:
            # insert transaction, map the new transaction to the existing classification
            transaction_row = TransactionRepository.insert_transaction(row)[0]
            TransClassRepository.insert_trans_class(transaction_row[0], classification_row[0])

    return
