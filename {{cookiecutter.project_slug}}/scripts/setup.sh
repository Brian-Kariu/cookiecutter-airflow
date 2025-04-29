#!/bin/bash

# Check for and install pre-commit
if ! command -v pre-commit &> /dev/null
then
    echo "pre-commit could not be found, installing..."
    pip install pre-commit
    pre-commit install
else
    echo "pre-commit is already installed."
fi

# Install other necessary libraries or tools
pip install --quiet --no-cache-dir pip==23.2.1
pip install  -e .[airflow,test] -c https://raw.githubusercontent.com/apache/airflow/constraints-{{cookiecutter.airflow_version}}/constraints-{{cookiecutter.python_version}}.txt

# Initialize local db
# If you are encountering any issue check this page https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html
echo "Setting up local database to connect to airflow. Add you postgres password when prompted."
psql -U postgres < scripts/setup.sql

echo "Setup complete!"
