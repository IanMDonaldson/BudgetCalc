from Services.StorageService import insert_transaction_and_classification


# transaction row = [id, date, description, amount, balance, 'BANKNAME']
def insert_helper(table, repository):
    for row in table:
        # print(row)
        # (repository.get_transactions_by_date(row[0]))
        # returns False if identical transaction, meaning that it's a duplicate file
        new_file = insert_transaction_and_classification(row)
        if not new_file:
            return False
    return True
