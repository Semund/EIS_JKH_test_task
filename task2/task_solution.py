from pymongo import MongoClient

from write_json import write_to_json_file


def clear_information(pay):
    return {
        'id': pay['id'],
        'date': pay['date']
    }


def get_verified_payments(payments_collection, accruals_collection):
    verified_payments = {
        'confirmed_payments': [],
        'unused_payments': []
    }
    closed_accruals = set()

    for payment in payments_collection.find().sort('date', 1):
        accrual = find_accrual_to_payment(payment, accruals_collection, closed_accruals)
        if accrual:
            verified_payments['confirmed_payments'].append(
                {
                    'payment': clear_information(payment),
                    'accrual': clear_information(accrual)
                }
            )
        else:
            verified_payments['unused_payments'].append(
                clear_information(payment)
            )

    return verified_payments


def find_accrual_to_payment(payment, accruals_collection, closed_accruals):
    accrual_same_month = parsing_accrual_collection(
        accruals_collection,
        closed_accruals,
        filter={'date': {'$lt': payment['date']}, 'month': payment['month']})

    if accrual_same_month:
        return accrual_same_month

    accrual_most_older = parsing_accrual_collection(
        accruals_collection,
        closed_accruals,
        filter={'date': {'$lt': payment['date']}})

    if accrual_most_older:
        return accrual_most_older

    return None


def parsing_accrual_collection(accruals_collection, closed_accruals, filter):
    for accrual in accruals_collection.find(filter).sort('date', 1):
        if accrual and accrual['id'] not in closed_accruals:
            closed_accruals.add(accrual['id'])
            return accrual
    return None


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.task2_db
    accrual_collection = db.accrual
    payment_collection = db.payment

    verified_payments = get_verified_payments(payment_collection, accrual_collection)
    write_to_json_file(verified_payments, 'verified_payments')
