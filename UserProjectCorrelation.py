from AccessLevel import AccessLevel
from common import _get_entity_from_file, _send_create_request


class UserProjectCorrelation:
    def __init__(self, user_id, project_id, access_level):
        self.id = project_id
        self.user_id = user_id
        self.access_level = access_level

    def __str__(self):
        return "project {0} - user {1}".format(str(self.id), str(self.user_id))


def create_user_project_correlation(filename, users, projects):
    url = "/projects/{0}/members"
    project_user_list = list(map(lambda project_user: UserProjectCorrelation(
        list(filter(lambda user: user.origin_id == project_user['UserID'], users))[0].id,
        list(filter(lambda project: project.origin_id == project_user['RepoID'], projects))[0].id,
        {1: AccessLevel.REPORTER_ACCESS, 2: AccessLevel.DEVELOPER_ACCESS, 3: AccessLevel.MAINTAINER_ACCESS}.get(project_user['Mode'])),
                                 _get_entity_from_file(filename)))
    return [_send_create_request(url.format(project_user.id), project_user) for project_user in project_user_list]