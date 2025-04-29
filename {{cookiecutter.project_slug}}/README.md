# {{cookiecutter.project_slug}}
{{cookiecutter.description}}

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

## Getting Started

### Dependencies
To set up this project, you will need the following:
* Python {{cookiecutter.python_version}}
* Docker and Docker Engine

### Installing
To get started first clone this repo to your local machine.
```bash
git clone {{cookiecutter.git_repo}}.git
```

Next you have to run the makefile commands to initialize your project.
> NOTE: if you are using a tool like `virtualenv`,`virtualenvwrapper` or any other venv management tool (conda), create your own env and save the path to it in the `VIRTUAL_ENV_PATH` environment variable before proceeding.
```bash
make init

# To install all envs run
make install

# To install only airflow run
make install-airflow
```

### Running the service
To automate running our services we use this make commands to start airflow and airbyte.

```bash
make airflow-init
make airflow-up
```

After this you can follow the user guide to learn how to work in the environment.

### User Guide
We usually use a combination of `tox` and `make` commands to manage our development workflows locally. Tox is what we use on on CI/CD pipelines but we can use make if your comfortable using it.

## Testing
To run tests and coverage you can either of these commands

```bash
make test
make coverage

# or you can run
tox -e unittest # for unit tests
tox -e validation_tests # for validation tests
```

## Linting
To run the lint tests run any of these commands

```bash
ruff .
mypy dags/elt/

# alternatively run
tox -e lint
tox -e types
```

## Docs
To build docs run this command

```bash
make docs

# alternatively run
tox -e docs
```

## Authors
{{ cookiecutter.author_name }} - {{ cookiecutter.email }}

## Version History
For a list of changes look at the [changelog]({{ cookiecutter.git_repo }}/-/blob/master/CHANGELOG.md)

## License

This project is licensed under the {{ cookiecutter.open_source_license }} License - see the [license]({{ cookiecutter.git_repo }}/-/blob/master/LICENSE.txt) file for details

