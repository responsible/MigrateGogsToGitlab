from time import sleep

import requests

from User import User
from common import _get_entity_from_file, _send_create_request
from variables import GOGS_REPO_URL, BASE_URL


class Project:
    def __init__(self, id, origin_id, user_id, namespace_id, name, description, visibility, import_url, mirror):
        self.id = id
        self.origin_id = origin_id
        self.user_id = user_id
        self.namespace_id = namespace_id
        self.name = name
        self.description = description
        self.visibility = visibility
        self.import_url = import_url
        self.mirror = mirror

    def __str__(self):
        return self.name


def create_project(filename, user_list):
    url = "projects/user/{0}"
    if len(list(filter(lambda user: user.id == None, user_list))) != 0:
        print("User and project should be created together!")
        return
    project_list = []
    for project in _get_entity_from_file(filename):
        owner = list(filter(lambda user: user.origin_id == project['OwnerID'], user_list))[0]
        project_list = [*project_list, Project(None,
                                               project['ID'],
                                               owner.id if type(owner) is User else 1,
                                               owner._namespace_id,
                                               project['Name'],
                                               project['Description'],
                                               "private" if project['IsPrivate'] else "public",
                                               GOGS_REPO_URL.format(
                                                   owner.username if type(owner) is User else owner.name,
                                                   project['Name']),
                                               project['IsMirror'])]
    return [_send_create_request(url.format(project.user_id), project) for project in project_list]


def check_projects_import_success(projects):
    def get_import_status(project):
        url = "projects/{0}/import"
        response = requests.get(BASE_URL.format(url.format(project.id)))
        return response.json()['import_status']

    while True:
        failed_project = list(filter(lambda project: project[1] != 'finished',
                                     [(project, get_import_status(project)) for project in projects]))
        for project in failed_project:
            print("{0} - {1}".format(project[0], project[1]))
        print("{0} of {1} projects is still importing.".format(len(failed_project), len(projects)))
        sleep(5)
        if len(failed_project) == 0:
            break
