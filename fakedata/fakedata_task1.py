import datetime
import hashlib
import random

from faker import Faker
from pymongo import MongoClient
from pymongo import errors

fake = Faker('ru_RU')
actions_types = ['read', 'create', 'update', 'delete']


def create_user_accounts(user_accounts_collection, number_of_users=10):
    """
    Создание данных для пользователя и коллекции всех пользователей
    """
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
        user_accounts_collection.insert_many(user_accounts)
    except (errors.WriteError, errors.WriteConcernError) as e:
        print(e)


def create_sessions(user):
    """
    Создание данных сессии для каждого пользователя
    """
    for j in range(5):
        session_created_at = fake.date_time()
        session_hash = hashlib.sha256(
            session_created_at.strftime('%Y-%m-%d %H:%M').encode('utf-8')
        ).hexdigest()

        session = {
            'created_at': session_created_at,
            'session_id': session_hash,
            'actions': []
        }

        create_actions_for_session(session, session_created_at)

        user['sessions'].append(session)


def create_actions_for_session(session, created_at):
    """
    Создание данных для действий пользователя в каждой сессии
    """
    for _ in range(6):
        action = {
            'type': random.choice(actions_types),
            'created_at': fake.date_time_between(
                created_at,
                created_at + datetime.timedelta(hours=2))
        }

        session['actions'].append(action)


if __name__ == '__main__':
    client = MongoClient('mongodb://root:example@mongo_db:27017/')
    db = client.task1_db
    user_accounts_collection = db.account

    create_user_accounts(user_accounts_collection)
