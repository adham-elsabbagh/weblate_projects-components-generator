"""
    author : adham
    description: script for creating projects
"""
import os
import argparse
import warnings
from pprint import pprint
import requests


def parse_args():
    """
        Description : this function return args parse
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="project name")
    parser.add_argument("--web", type=str, help="project website")
    parser.add_argument("--path", type=str, help="projects path")
    parser.add_argument("--host", type=str, help="project website")
    parser.add_argument("--auth", type=str,
                        help="please enter Authorization:Token token")

    return parser.parse_args()


def _build_body(name, web="https://www.accomodata.be/en_US/"):
    """
    Description : this function returns the api body template
    """
    return {"name": name,
            "slug": name.replace(" ", "-"),
            "web": web,
            "source_language": {
                "code": "en",
                "name": "English",
                "plural": {
                    "source": None,
                    "number": None,
                    "formula": ""
                },
                "direction": None
            }
            }


def _get_projects(host, headers):
    """
        Description : get all the project names
    """
    get_projects = requests.get(host, headers=headers)
    if get_projects.status_code == 200 and get_projects.reason == 'OK':
        exist_projects = [i['name'] for i in get_projects.json()['results']]
        errors = False
    else:
        errors = True
        exist_projects = get_projects.json()['detail']
    return exist_projects, errors

    # # get_projects = requests.get(host, headers=headers).json()
    # exist_projects = [i['name'] for i in get_projects['results']]
    # return exist_projects


def auto_create_projects(p_path, host, headers, exist_projects, errors):
    """
        Description : this function for creating all not exist projects.
    """
    project_names = [f for f in os.listdir(p_path) if os.path.isdir(
        os.path.join(p_path, f)) and not f.startswith('.')]
    if not errors and project_names:
        for project_name in project_names:
            if project_name not in exist_projects:
                component_request = requests.post(host,
                                                  data=_build_body(
                                                      project_name),
                                                  headers=headers)
                component_request.raise_for_status()
                pprint(component_request.json())
            else:
                warnings.warn('Warning..!!! \n the project %s is already '
                              'exist' % project_name)


def create_separate_project(name, web, host, headers, exist_projects, errors):
    """
        Description : create one project based on the name.
    """

    if name not in exist_projects and not errors:
        component_request = requests.post(host, data=_get_projects(name, web),
                                          headers=headers)
        component_request.raise_for_status()
        pprint(component_request.json())
    else:
        warnings.warn('Warning..!!! \n the project %s is already '
                      'exist' % name)


def main():
    """
    Description : main function
    """
    args = parse_args()
    headers = {
        "Authorization": "Token " + args.auth
    }
    exist_projects, errors = _get_projects(args.host, headers)
    if args.path:
        auto_create_projects(args.path, args.host, headers, exist_projects,
                             errors)
    elif args.name:
        create_separate_project(args.name, args.web, args.host, headers,
                                exist_projects, errors)


if __name__ == "__main__":
    main()
