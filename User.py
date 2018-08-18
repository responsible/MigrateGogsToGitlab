import os

from common import _get_entity_from_file, _send_create_request, _get_all_namespaces
from variables import USER_PASSWD, GOGS_DB_FOLDER
from PIL import Image


class User:
    def __init__(self, id, origin_id, username, name, email, admin, skip_confirmation=True):
        self.id = id
        self.origin_id = origin_id
        self.username = username
        self.name = name
        self.email = email
        self.admin = admin
        self.skip_confirmation = skip_confirmation
        self.password = USER_PASSWD
        self._namespace_id = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name


def create_user(filename):
    url = "users"
    __pre_process_avatar()
    user_list = filter(lambda user: user['Type'] == 0, _get_entity_from_file(filename))
    user_list = list(map(
        lambda user: User(None, user['ID'], user['Name'], user['FullName'] or user['Name'], user['Email'], user["IsAdmin"]), user_list))
    user_list = [_send_create_request(url, user, files={'avatar': open("{0}/data/avatars/{1}.jpg".format(GOGS_DB_FOLDER, user.origin_id), 'rb')}) for user in user_list]
    namespaces = _get_all_namespaces()
    for user in user_list:
        user._namespace_id = list(filter(lambda namespace: namespace['name'] == user.username and namespace['kind'] == 'user', namespaces))[0]['id']
    return user_list


def __pre_process_avatar():
    avatars_path = '{0}/data/avatars/'.format(GOGS_DB_FOLDER)
    os.system("find {0} ! -name '*.jpg'".format(avatars_path) + " | xargs -I {} mv {} {}.jpg")
    while True:
        path, dirs, files = list(os.walk(avatars_path))[0]
        large_avatars = [os.path.join(avatars_path, file) for file in files if os.path.getsize(os.path.join(avatars_path, file)) > 200000]
        if len(large_avatars) == 0:
            break
        else:
            for avatar in large_avatars:
                avatar_file = Image.open(avatar)
                avatar_file.save(avatar, optimize=True, quality=95)
