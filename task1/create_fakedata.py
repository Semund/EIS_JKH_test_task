import datetime
import hashlib
import random

from faker import Faker
from pymongo import MongoClient
from pymongo import errors

fake = Faker('ru_RU')
actions_types = ['read', 'create', 'update', 'delete']


def create_user_accounts(accounts, number_of_users=10):
    user_accounts = []
    for i in range(number_of_users):
        user_name = fake.name()
        user = {
            'number': f'{7800000000001 + i}',
            'name': user_name,
            'sessions': []
        }
        create_sessions(user)
        user_accounts.append(user)

    try:
        accounts.insert_many(user_accounts)
    except (errors.WriteError, errors.WriteConcernError) as e:
        print(e)


def create_sessions(user):
    for j in range(5):
        session_created_at = fake.date_time()
        session = {
            'created_at': session_created_at,
            'session_id': hashlib.sha256((user['name'] + str(j)).encode('utf-8')).hexdigest(),
            'actions': []
        }

        create_actions_for_session(session, session_created_at)

        user['sessions'].append(session)


def create_actions_for_session(session, created_at):
    for _ in range(6):
        action = {
            'type': random.choice(actions_types),
            'created_at': fake.date_time_between(
                created_at,
                created_at + datetime.timedelta(hours=2))
        }

        session['actions'].append(action)


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.task1_db
    accounts = db.account
    create_user_accounts(accounts)
