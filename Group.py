from common import _get_entity_from_file, _send_create_request, _get_all_namespaces


class Group:
    def __init__(self, id, origin_id, name, path, description, visibility, parent_id=None):
        self.id = id
        self.origin_id = origin_id
        self.name = name
        self.path = path
        self.description = description
        self.visibility = visibility
        self.parent_id = parent_id
        self._namespace_id = None

    def __str__(self):
        return self.name


def create_group(filename):
    url = "groups"
    group_list = filter(lambda user: user['Type'] == 1, _get_entity_from_file(filename))
    group_list = list(map(lambda group: Group(None, group['ID'], group['FullName'], group['Name'], group['Description'], "public"), group_list))
    group_list = [_send_create_request(url, group) for group in group_list]
    namespaces = _get_all_namespaces()
    for group in group_list:
        group._namespace_id = list(filter(lambda namespace: namespace['name'] == group.name and namespace['kind'] == 'group', namespaces))[0]['id']
    return group_list


def create_subgroup(filename, parent_group):
    url = "groups"
    if len(list(filter(lambda group: group.id == None, parent_group))) != 0:
        print("Group and subgroup should be created together!")
        return
    group_list = map(lambda group: Group(None, group['ID'], group['Name'], group['LowerName'], group['Description'], "public",
                                         list(filter(lambda parent_group: parent_group.origin_id == group['OrgID'], parent_group))[0].id),
                     _get_entity_from_file(filename))
    return [_send_create_request(url, group) for group in group_list]