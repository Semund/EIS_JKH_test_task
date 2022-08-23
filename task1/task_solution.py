from pymongo import MongoClient

from write_json import write_to_json_file


def collect_all_user_statistic(accounts):
    all_users_statistic = []
    for current_user in accounts.find():
        current_user_statistic = collect_current_user_statistic(current_user)
        all_users_statistic.append(current_user_statistic)
    return all_users_statistic


def collect_current_user_statistic(user):
    user_actions_info = {}
    for session in user['sessions']:
        parsing_user_session(session, user_actions_info)

    user_statistic = {
        'number': user['number'],
        'actions': []
    }

    for type_action, action_info in user_actions_info.items():
        user_statistic['actions'].append(
            {
                'type': type_action,
                'last': action_info[1],
                'count': action_info[0]
            }
        )
    return user_statistic


def parsing_user_session(session, user_actions):
    for current_session_action in session['actions']:
        user_actions_info = user_actions.get(current_session_action['type'], [0, None])

        user_actions_info[0] += 1
        if user_actions_info[1] is None or current_session_action['created_at'] > user_actions_info[1]:
            user_actions_info[1] = current_session_action['created_at']

        user_actions[current_session_action['type']] = user_actions_info


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.task1_db
    accounts = db.account

    all_users_statistic = collect_all_user_statistic(accounts)
    write_to_json_file(all_users_statistic, 'user_statistics')
