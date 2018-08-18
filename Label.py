from common import _get_entity_from_file, _send_create_request


class Label:
    def __init__(self, project_id, name, color):
        self.id = project_id
        self.name = name
        self.color = color

    def __str__(self):
        return self.name


def create_project_label(filename, projects):
    url = "/projects/{0}/labels"
    project_label_list = list(map(lambda label: Label(list(filter(lambda project: project.origin_id == label['RepoID'], projects))[0].id,
                                                      label['Name'], label['Color']),
                                  _get_entity_from_file(filename)))
    return [_send_create_request(url.format(project_label.id), project_label) for project_label in project_label_list]