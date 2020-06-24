import json
import string
import random

from user_api import settings
from user_api.exeptions import NoUserIdFound

json_data_file = settings.BASE_DIR + '/user_api/data_file.json'


def id_generator(data: dict,
                 size=10,
                 chars=string.ascii_lowercase + string.digits):

    new_key = ''.join(random.choice(chars) for _ in range(size))
    if new_key in data['users']:
        return id_generator(data)
    else:
        return new_key


def create_user(user_name: str, email: str):
    with open(json_data_file, 'r+') as file:
        data = json.load(file)

        user_id = id_generator(data=data)

        data['users'][user_id] = {'name': user_name, 'email': email}
        file.seek(0)
        json.dump(data, file)
        file.truncate()

        return True


def get_users():
    with open(json_data_file, 'r+') as file:
        data = json.load(file)

        user_list = []
        for key, value in data.items():
            user_list.append({key: value})

    return user_list


def get_user_by_id(user_id: str):
    with open(json_data_file, 'r+') as file:
        data = json.load(file)

        if user_id not in data['users']:
            raise NoUserIdFound

        user = data['users'][user_id]

    return user


def update_user(user_id: str, request_data: dict):
    with open(json_data_file, 'r+') as file:
        data = json.load(file)

        if user_id not in data['users']:
            raise NoUserIdFound

        if 'email' in request_data:
            data['users'][user_id]['email'] = request_data['email']

        if 'name' in request_data:
            data['users'][user_id]['name'] = request_data['name']

        file.seek(0)
        json.dump(data, file)
        file.truncate()

    return data['users'][user_id]


def delete_user(user_id: str):
    with open(json_data_file, 'r+') as file:
        data = json.load(file)

        if user_id not in data['users']:
            raise NoUserIdFound

        del data['users'][user_id]
        file.seek(0)
        json.dump(data, file)
        file.truncate()
