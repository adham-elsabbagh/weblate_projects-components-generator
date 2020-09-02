import os
import subprocess
import argparse


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
                           "--i18n-export="+lang+".tgz",
                           "--modules="+module_name])


def generate_po(m_path, o_path, database, lang):
    """
    Description : this function for exporting tgz file that containing all
    the po files for the project modules.
    """
    # ignore all files and select just the directories
    module_names = [f for f in os.listdir(m_path) if os.path.isdir(
        os.path.join(m_path, f)) and not f.startswith('.')]
    os.chdir(m_path)
    _odoo_command(o_path, database, lang, ",".join(module_names))
    subprocess.run(['tar', '-xvf', m_path+'/'+lang+".tgz"])
    subprocess.run(['rm', '-d', lang+".tgz"])


def main():
    args = parse_args()
    generate_po(args.path_to_modules, args.path_to_odoo_bin, args.d, args.l)


if __name__ == "__main__":
    main()
