-- SQL SCRIPT TO SETUP A LOCAL DEV ENVIRONMENT
-- RUN THIS ON YOUR POSTGRES INSTANCE WITH psql
-- e.g psql < setup.sql

DROP USER IF EXISTS airflow_user;

CREATE USER airflow_user WITH CREATEDB CREATEROLE SUPERUSER LOGIN PASSWORD 'airflow_pass';

DROP DATABASE IF EXISTS airflow;

CREATE DATABASE airflow WITH OWNER postgres;

GRANT ALL ON DATABASE airflow TO airflow_user;
