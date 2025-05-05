# Cookiecutter Airflow
Cookiecutter Airflow is the fastest way to get started with data orchestration with modern python tooling.

[![ci](https://github.com/Brian-Kariu/cookiecutter-airflow/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Brian-Kariu/cookiecutter-airflow/actions/workflows/ci.yml)
![codecov](https://img.shields.io/codecov/c/github/Brian-Kariu/cookiecutter-airflow)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![license: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Features

- For Apache Airflow > 2
- Works with Python 3.12
- Docker support using [docker-compose](https://github.com/docker/compose) for development and production
- Run tests with pytest
- Customizable PostgreSQL version
- Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review

## Usage

Let's pretend you want to create a Django project called "data-platform".

First, get Cookiecutter:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo:

    $ cookiecutter https://github.com/Brian-Kariu/cookiecutter-airflow

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'John Doe' etc to your own information.

Answer the prompts with your own desired. For example:

    Cloning into 'cookiecutter-airflow'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    [1/14] project_name (data-engineering): data-platform
    [2/14] project_slug (data_platform):
    [3/14] description (Repository for data engineering.): My very awsome project
    [4/14] python_version (3.12): 3.12
    [5/14] author_name (John): john.doe
    [6/14] domain_name (example.com): gmail.com
    [7/14] email (john.doe@gmail.com):
    [8/14] airflow_version (2.10.0):
    [9/14] git_repo (https://github.com/):
    [10/14] Select open_source_license
        1 - MIT
        2 - BSD
        3 - GPLv3
        4 - Apache Software License 2.0
        5 - Not open source
        Choose from [1/2/3/4/5] (1): 1
    [11/14] use_docker (n): y
    [12/14] Select ci_tool
        1 - None
        2 - Gitlab
        3 - Github
        Choose from [1/2/3] (1): 3
    [13/14] Select postgresql_version
        1 - 17
        2 - 16
        3 - 15
        4 - 14
        5 - 13
        Choose from [1/2/3/4/5] (1): 2
    [14/14] debug (n): n
    [SUCCESS]: Project initialized, keep up the good work!

Enter the project and take a look around:

    $ cd data-platform/
    $ ls

Create a git repo and push it there:

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:<USERNAME>/data-platform.git
    $ git push -u origin master


## Not Exactly What You Want?
If you have differences in your preferred setup, I encourage you to fork this to create your own version.

