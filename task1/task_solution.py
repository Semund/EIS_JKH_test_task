from pprint import pprint

from pymongo import MongoClient


def collect_all_user_statistic(accounts):
    all_users_statistic = []
    for user in accounts.find():
        user_actions_info = collect_user_actions_info(user)
        all_users_statistic.append(user_actions_info)
    return all_users_statistic


def collect_user_actions_info(user):
    user_actions = {}

    for session in user['sessions']:
        parsing_user_session(session, user_actions)

    user_statistic = {
        'number': user['number'],
        'actions': []
    }

    for type_action, values in user_actions.items():
        user_statistic['actions'].append(
            {
                'type': type_action,
                'last': values[1],
                'count': values[0]
            }
        )
    return user_statistic


def parsing_user_session(session, user_actions):
    for action in session['actions']:
        action_info = user_actions.get(action['type'], [0, None])

        action_info[0] += 1
        if action_info[1] is None or action['created_at'] > action_info[1]:
            action_info[1] = action['created_at']

        user_actions[action['type']] = action_info


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.task1_db
    accounts = db.account

    all_users_statistic = collect_all_user_statistic(accounts)
    pprint(all_users_statistic)
