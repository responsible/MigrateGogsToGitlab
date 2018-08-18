from common import _get_entity_from_file, _send_create_request


class Key:
    def __init__(self, id, title, key):
        self.id = id
        self.title = title
        self.key = key

    def __str__(self):
        return "user - {0}".format(self.id)


def create_user_ssh_key(filename, users):
    url = "/users/{0}/keys"
    key_list = list(
        map(lambda key: Key(list(filter(lambda user: user.origin_id == key['OwnerID'], users))[0].id, key['Name'], key['Content']),
            _get_entity_from_file(filename)))
    return [_send_create_request(url.format(key.id), key) for key in key_list]
