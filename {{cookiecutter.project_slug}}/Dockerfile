FROM apache/airflow:{{cookiecutter.airflow_version}}-python{{cookiecutter.python_version}}

ARG CI_COMMIT_REF_NAME
ARG CI_COMMIT_SHORT_SHA
ARG REQUIREMENTS

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libmysqlclient-dev \
        default-libmysqlclient-dev \
        curl \
        apt-transport-https \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/airflow/
COPY . /opt/airflow/

# install your pip packages
RUN pip install --no-cache-dir "apache-airflow[google, sentry, statsd]" \
    -c https://raw.githubusercontent.com/apache/airflow/constraints-{{cookiecutter.airflow_version}}/constraints-{{cookiecutter.python_version}}.txt \
    -e .[airflow,dbt]
