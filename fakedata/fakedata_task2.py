import datetime
import random

from pymongo import MongoClient, errors


def create_finance_fakedata(finance_collection):
    finance_data = []
    year = 2021
    id = 1
    for month in range(1, 13):
        for _ in range(2):
            day = random.randint(1, 29)
            finance_data.append(
                {
                    'id': id,
                    'date': datetime.datetime(year, month, day),
                    'month': month
                }
            )
            id += 1

    try:
        finance_collection.insert_many(finance_data)
    except (errors.WriteError, errors.WriteConcernError) as e:
        print(e)


if __name__ == '__main__':
    client = MongoClient('mongodb://root:example@mongo_db:27017/')
    db = client.task2_db
    accrual_collection = db.accrual
    payment_collection = db.payment

    create_finance_fakedata(accrual_collection)
    create_finance_fakedata(payment_collection)
