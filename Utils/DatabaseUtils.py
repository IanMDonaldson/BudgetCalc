import Repositories.ClassificationRepository
from Repositories import ClassificationRepository
from Services.StorageService import insert_transaction_and_classification


# transaction row = [id, date, description, amount, balance, 'BANKNAME']
def insert_helper(table, repository):
    for row in table:
        print(row)
        print(repository.get_transactions_by_date(row[0]))
        insert_transaction_and_classification(row)
    return True





