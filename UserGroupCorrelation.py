from AccessLevel import AccessLevel
from common import _get_entity_from_file, _send_create_request


class UserGroupCorrelation:
    def __init__(self, user_id, org_id, access_level):
        self.id = org_id
        self.user_id = user_id
        self.access_level = access_level

    def __str__(self):
        return "group {0} - user {1}".format(str(self.id), str(self.user_id))


def create_user_group_correlation(filename, users, groups):
    url = "/groups/{0}/members"
    group_user_list = list(map(lambda group_user: UserGroupCorrelation(
        list(filter(lambda user: user.origin_id == group_user['Uid'], users))[0].id,
        list(filter(lambda group: group.origin_id == group_user['OrgID'], groups))[0].id,
        AccessLevel.OWNER_ACCESS if group_user['IsOwner'] else AccessLevel.DEVELOPER_ACCESS),
                               _get_entity_from_file(filename)))
    group_user_list = [_send_create_request(url.format(group_user.id), group_user) for group_user in group_user_list]
    return group_user_list