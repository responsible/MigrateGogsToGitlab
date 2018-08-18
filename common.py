import json
import re
import sys

import requests

from variables import BASE_URL, GOGS_DB_FOLDER


def _send_create_request(url, resource, files=None):
    response = requests.post(BASE_URL.format(url), data=vars(resource), files=files)
    if response.status_code == 201:
        resource.id = response.json()['id']
        print("{0} {1}[{2}] created.".format(response.status_code, resource.__class__.__name__, str(resource)))
    else:
        print("{0} {1}[{2}] failed. {3}".format(response.status_code, resource.__class__.__name__, str(resource), str(response.content)))
    return resource


def _get_entity_from_file(entity_name):
    with open("{0}/{1}/db/{2}.json".format(sys.path[0], GOGS_DB_FOLDER, entity_name)) as entitys:
        entity_list = map(lambda entity: json.loads(entity), entitys.read().strip().split("\n"))
    return entity_list


def _get_all_namespaces():
    url = "namespaces"
    response = requests.get(BASE_URL.format(url))
    namespaces = [*response.json()]
    while True:
        next_link = re.match(r'<(.*)>; rel="next"', response.headers.get('link'))
        if next_link is None:
            break
        response = requests.get(next_link.group(1))
        namespaces = [*namespaces, *response.json()]
    print("{0} all namespaces fetched.".format(response.status_code))
    return namespaces
