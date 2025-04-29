import random
import shutil
from pathlib import Path

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_dotgitlabciyml_file():
    Path(".gitlab-ci.yml").unlink()


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def main():
    debug = "{{ cookiecutter.debug }}".lower() == "y"

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
