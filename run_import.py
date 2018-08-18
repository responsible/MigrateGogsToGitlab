#!/usr/local/bin/python3

from Group import create_group, create_subgroup
from Key import create_user_ssh_key
from Label import create_project_label
from Project import create_project, check_projects_import_success
from User import create_user
from UserGroupCorrelation import create_user_group_correlation
from UserProjectCorrelation import create_user_project_correlation

groups = create_group("User")
create_subgroup("Team", groups)
users = create_user("User")
projects = create_project("Repository", [*users, *groups])
create_user_group_correlation("OrgUser", users, groups)
create_user_project_correlation("Collaboration", users, projects)
create_user_ssh_key("PublicKey", users)
create_project_label("Label", projects)
check_projects_import_success(projects)
