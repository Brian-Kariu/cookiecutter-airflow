import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture(scope="session")
def cookiecutter_template_path():
    """Return the absolute path to the cookiecutter template directory."""
    return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def default_context():
    """Return the default context for cookiecutter."""
    return {
        "project_name": "data-engineering",
        "description": "Repository for data engineering.",
        "python_version": "3.12",
        "author_name": "John",
        "domain_name": "example.com",
        "email": "john@example.com",
        "airflow_version": "2.10.0",
        "git_repo": "https://github.com/",
        "open_source_license": "MIT",
        "use_docker": "y",
        "ci_tool": "Github",
        "postgresql_version": "17",
        "debug": "n",
    }


@pytest.fixture(scope="function")
def cookiecutter_project(cookiecutter_template_path, default_context, tmp_path):
    """Generate a cookiecutter project using the template."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as f:
        import json

        json.dump(default_context, f)
        config_file = f.name

    try:
        output_dir = str(tmp_path)
        result = cookiecutter(
            template=str(cookiecutter_template_path),
            no_input=True,
            output_dir=output_dir,
            config_file=config_file,
        )
        project_path = Path(output_dir) / "data_engineering"
        yield project_path
    finally:
        os.unlink(config_file)


@pytest.fixture(scope="function")
def airflow_env(cookiecutter_project, monkeypatch):
    """Set up an Airflow environment for testing."""
    # Create a temporary directory for Airflow home
    airflow_home = cookiecutter_project / "airflow_home"
    airflow_home.mkdir(exist_ok=True)

    # Set Airflow environment variables
    monkeypatch.setenv("AIRFLOW_HOME", str(airflow_home))
    monkeypatch.setenv("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
    monkeypatch.setenv(
        "AIRFLOW__CORE__DAGS_FOLDER", str(cookiecutter_project / "airflow" / "dags")
    )

    # Initialize Airflow database
    try:
        subprocess.run(
            ["airflow", "db", "init"], check=True, cwd=str(cookiecutter_project)
        )
    except subprocess.CalledProcessError:
        pytest.skip("Airflow not available, skipping tests that require Airflow")

    yield

    # Clean up
    shutil.rmtree(airflow_home, ignore_errors=True)


@pytest.fixture(scope="function")
def variable_project_context(default_context):
    """Return a function that allows modifying the default context."""

    def _modify_context(**kwargs):
        modified_context = default_context.copy()
        modified_context.update(kwargs)
        return modified_context

    return _modify_context


@pytest.fixture()
def create_project_with_context(cookiecutter_template_path, tmp_path):
    """Create a project with a modified context."""

    def _create_project(context):
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as f:
            import json

            json.dump(context, f)
            config_file = f.name

        try:
            output_dir = str(tmp_path)
            result = cookiecutter(
                template=str(cookiecutter_template_path),
                no_input=True,
                output_dir=output_dir,
                config_file=config_file,
            )
            project_slug = context.get(
                "project_slug",
                context.get("project_name")
                .lower()
                .strip()
                .replace(" project", "")
                .replace(" ", "_")
                .replace(":", "_")
                .replace("-", "_")
                .replace("!", "_"),
            )
            print(f"project slug: {project_slug}")
            project_path = Path(output_dir) / project_slug
            return project_path
        finally:
            os.unlink(config_file)

    return _create_project
