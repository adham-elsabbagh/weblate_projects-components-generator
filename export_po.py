import os
import subprocess
import argparse
import warnings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_odoo_bin", type=str,
                        help="path to odoo-bin")
    parser.add_argument("--path_to_modules", type=str,
                        help="path to odoo modules")
    parser.add_argument("--d", type=str, help="database name")
    parser.add_argument("--l", type=str, help="language code")
    return parser.parse_args()


def _odoo_command(o_path, database, lang, module_name):
    """
    odoo-bin command for exporting po files
    """
    return subprocess.run(["python3", o_path, "-d", database, "-l", lang,
                           "--i18n-export="+lang+".po",
                           "--modules="+module_name])


def generate_po(m_path, o_path, database, lang):
    """
    Description : this function covers 3 cases:
    1- if we don't have i18n dir we will create a dir and export he po file.
    2- if we have localization dir and we don't have a specific language
    then it export the po file.
    3- if we already have the language po file the function will override
    the function by removing the old one and export new version
    """
    # ignore all files and select just the directories
    module_names = [f for f in os.listdir(m_path) if os.path.isdir(
        os.path.join(m_path, f)) and not f.startswith('.')]
    for module_name in module_names:
        os.chdir(m_path+'/'+module_name+'/')
        module_path = os.getcwd()
        module_files = [f for f in os.listdir(module_path) if os.path.isdir(
            os.path.join(module_path, f)) and not f.startswith('.')]
        loc_names = ('i18n', 'l10n', 'i10n')
        if not any(f in loc_names for f in module_files):
            os.system('mkdir i18n')
            os.chdir('i18n'+'/')
            _odoo_command(o_path, database, lang, module_name)
        else:
            for mod_file in module_files:
                if mod_file in loc_names:
                    os.chdir(mod_file+'/')
                    trans = os.listdir(os.getcwd())
                    if not any(File.endswith(".po") for File in trans):
                        _odoo_command(o_path, database, lang, module_name)

                    else:
                        subprocess.run(['rm', '-f', lang+".po"])
                        _odoo_command(o_path, database, lang, module_name)
                        warnings.warn("the module %s is overridden with po "
                                      "file"
                                      % module_name)


def main():
    args = parse_args()
    generate_po(args.path_to_modules, args.path_to_odoo_bin, args.d, args.l)


if __name__ == "__main__":
    main()
