"""
    author : adham
    description :script for creating components
"""
import os
import argparse
import warnings
from pprint import pprint
import glob
import requests


def parse_args():
    """
        Description : this function return args parse
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="component name")
    parser.add_argument("--repo", type=str, help="repo that you want to "
                                                 "contribute with")
    parser.add_argument("--branch", type=str,
                        help="Repository branch to translate")
    parser.add_argument("--host", type=str, help="host link")
    parser.add_argument("--auth", type=str, help="please enter "
                                                 "Authorization:Token token")
    return parser.parse_args()


def _get_components(host, headers):
    """
        Description : get all the component names.
    """
    get_comp = requests.get(host, headers=headers)
    if get_comp.status_code == 200 and get_comp.reason == 'OK':
        exist_comp = [i['name'] for i in get_comp.json()['results']]
        errors = False
    else:
        errors = True
        exist_comp = get_comp.json()['detail']
    return exist_comp, errors


def auto_create_components(c_path, repo, branch, host, headers, exist_comp,
                           errors):
    """
        Description : this function for creating multiple components based on
        the project path.
    """
    # ignore all files and select just the directories
    component_names = [f for f in os.listdir(c_path) if os.path.isdir(
        os.path.join(c_path, f)) and not f.startswith('.')]
    if not errors and component_names:
        # get request with the name of teh components
        for component_name in component_names:
            print(component_name)
            if component_name not in exist_comp:
                # getting all dirs in sepeci compo name
                localization_dirs = [os.path.basename(f) for f in
                                     glob.glob(c_path+'/'+component_name+'/*')
                                     if os.path.isdir(f) and not
                                     f.startswith('.')]
                for localization_file_name in localization_dirs:
                    loc_file_names = ('i18n', 'l10n', 'i10n')
                    if localization_file_name in loc_file_names:
                        trans = os.listdir(c_path + '/' + component_name +
                                           '/' + localization_file_name)
                        if any(File.endswith(".po") for File in trans):
                            data = {
                                "name": component_name,
                                "slug": component_name.replace(" ", "-"),
                                "vcs": "gitlab",
                                "repo": repo,
                                "git_export": "",
                                "branch": branch,
                                "filemask":
                                    component_name+'/'+localization_file_name +
                                    '/*.po',
                                "template": "",
                                "edit_template": False,
                                "new_base": '',
                                "file_format": "po",
                                "license": "LGPL-3.0-or-later",
                                "new_lang": "none",
                                "push": "",
                                "check_flags": "",
                                "enforced_checks": "",
                                "restricted": False
                            }
                            component_request = requests.post(host,
                                                              json=data,
                                                              headers=headers)
                            component_request.raise_for_status()
                            pprint(component_request.json())
                        else:
                            warnings.warn("Warning..!!!There are no '.po' "
                                          "files")
                    else:
                        warnings.warn("Warning..!!!There are no localization "
                                      "directories in %s" % component_name)
            else:
                warnings.warn('Warning..!!! \n the component %s '
                              'is already exist' % component_name)
    else:
        warnings.warn("warning.... %s" % exist_comp)


def create_separate_component(name, repo, branch, filemask, newbase,
                              headers, host, exist_comp, errors):
    """
        Description : creates a separate component based on the name.
    """
    if name not in exist_comp and not errors:
        data = {
            "name": name,
            "slug": name.replace(" ", "-"),
            "vcs": "gitlab",
            "repo": repo,
            "git_export": "",
            "branch": branch,
            "filemask": filemask,
            "template": "",
            "edit_template": False,
            "new_base": newbase,
            "file_format": "po",
            "license": "LGPL-3.0-or-later",
            "new_lang": "add",
            "push": "",
            "check_flags": "",
            "enforced_checks": "",
            "restricted": False
        }
        component_request = requests.post(host, json=data,
                                          headers=headers)
        component_request.raise_for_status()
        pprint(component_request.json())
    else:
        warnings.warn('Warning..!!! \n the component %s '
                      'is already exist' % name)


def main():
    """
    Description : main function
    """
    args = parse_args()
    headers = {
        "Authorization": "Token " + args.auth
    }
    exist_comp, errors = _get_components(args.host, headers)
    if args.path:
        auto_create_components(args.path, args.repo, args.branch, args.host,
                               headers, exist_comp, errors)
    elif args.name:
        create_separate_component(args.name, args.repo, args.branch,
                                  args.filemask, args.newbase, headers,
                                  args.host, exist_comp, errors)


if __name__ == "__main__":
    main()
