import datetime
import json
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import airflow
import pytest
from airflow.models import DagBag
from airflow.utils.dag_cycle_tester import check_cycle

# Path constants - adjust as needed
TEMPLATE_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEST_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


@contextmanager
def change_dir(path):
    """Context manager for changing directory."""
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


class TestCookiecutterGeneration:
    """Test the generation of the cookiecutter template."""

    @pytest.fixture(scope="class")
    def temp_project_dir(self, tmp_path_factory):
        """Create a temporary directory for the test project."""
        temp_dir = tmp_path_factory.mktemp("test_project")
        return temp_dir

    @pytest.fixture(scope="class")
    def generated_project(self, temp_project_dir):
        """Generate a project from the cookiecutter template."""
        context = {
            "project_name": "data-engineering",
            "description": "Test project for data engineering",
            "python_version": "3.12",
            "author_name": "Test User",
            "domain_name": "example.com",
            "email": "test-user@example.com",
            "airflow_version": "2.10.0",
            "git_repo": "https://github.com/test/test-project",
            "open_source_license": "MIT",
            "use_docker": "y",
            "ci_tool": "Github",
            "postgresql_version": "16",
            "debug": "n",
        }

        # Write context to a temporary JSON file
        context_file = temp_project_dir / "context.json"
        with open(context_file, "w") as f:
            json.dump(context, f)

        # Run cookiecutter with the context file
        subprocess.run(
            [
                "cookiecutter",
                "--no-input",
                "--config-file",
                str(context_file),
                str(TEMPLATE_ROOT),
            ],
            check=True,
            cwd=str(temp_project_dir),
        )

        # Return the path to the generated project
        return temp_project_dir / "test_data_engineering"

    @pytest.mark.skip()
    def test_project_directory_structure(self, generated_project):
        """Test that the project directory structure is correct."""
        assert generated_project.exists()
        assert (generated_project / "airflow" / "dags").exists()
        assert (
            generated_project / "airflow" / "dags" / "maintainance" / "canary.py"
        ).exists()
        assert (generated_project / "README.md").exists()
        assert (generated_project / "Dockerfile").exists()
        assert (generated_project / "docker-compose.local.yml").exists()
        assert (generated_project / "Makefile").exists()
        assert (generated_project / "pyproject.toml").exists()
        assert (generated_project / "tests").exists()

    @pytest.mark.skip()
    def test_readme_content(self, generated_project):
        """Test that the README.md contains the expected content."""
        readme_path = generated_project / "README.md"
        assert readme_path.exists()

        with open(readme_path, "r") as f:
            content = f.read()

        assert "data-engineering" in content
        assert "Test project for data engineering" in content

    @pytest.mark.skip()
    def test_license_file(self, generated_project):
        """Test that the LICENSE file is correctly generated."""
        license_path = generated_project / "LICENSE.txt"
        assert license_path.exists()

        with open(license_path, "r") as f:
            content = f.read()

        assert "MIT" in content
        assert "Test User" in content
        assert str(datetime.datetime.now().year) in content

    @pytest.mark.skip()
    def test_pyproject_toml(self, generated_project):
        """Test that the pyproject.toml file contains correct dependencies."""
        pyproject_path = generated_project / "pyproject.toml"
        assert pyproject_path.exists()

        with open(pyproject_path, "r") as f:
            content = f.read()

        assert 'name = "test_data_engineering"' in content
        assert "apache-airflow" in content
        assert "2.10.0" in content  # Airflow version
        assert 'python = ">=3.12"' in content

    @pytest.mark.skip()
    def test_dockerfile(self, generated_project):
        """Test that the Dockerfile exists and contains expected content."""
        if os.path.exists(generated_project / "Dockerfile"):
            with open(generated_project / "Dockerfile", "r") as f:
                content = f.read()

            assert "FROM" in content
            assert "WORKDIR" in content
            assert "COPY" in content

    @pytest.mark.skip()
    def test_docker_compose(self, generated_project):
        """Test that the docker-compose file exists and contains expected services."""
        docker_compose_path = generated_project / "docker-compose.local.yml"
        assert docker_compose_path.exists()

        with open(docker_compose_path, "r") as f:
            content = f.read()

        assert "services:" in content
        assert "postgres:" in content
        assert "image: postgres:" in content
        assert "16" in content  # PostgreSQL version
        assert "airflow-webserver:" in content


class TestAirflowDags:
    """Test the Airflow DAGs included in the template."""

    @pytest.fixture
    def dagbag(self, generated_project):
        """Create a DagBag for testing the DAGs."""
        # Add the DAGs directory to the Python path
        dags_dir = str(generated_project / "airflow" / "dags")
        sys.path.append(dags_dir)

        # Create and return a DagBag
        return DagBag(dags_dir)

    @pytest.mark.skip()
    def test_dag_loading(self, dagbag):
        """Test that all DAGs load without errors."""
        assert not dagbag.import_errors

    @pytest.mark.skip()
    def test_canary_dag(self, dagbag):
        """Test that the canary DAG is properly defined."""
        canary_dag = dagbag.get_dag("canary_dag")
        assert canary_dag is not None

        # Check DAG attributes
        assert canary_dag.dag_id == "canary_dag"
        assert canary_dag.schedule_interval is not None

        # Check tasks
        task_ids = [task.task_id for task in canary_dag.tasks]
        assert "start" in task_ids

    @pytest.mark.skip()
    def test_dag_cycles(self, dagbag):
        """Test that DAGs don't contain cycles."""
        for dag_id, dag in dagbag.dags.items():
            try:
                check_cycle(dag)
            except airflow.exceptions.AirflowDagCycleException:
                pytest.fail(f"DAG {dag_id} contains a cycle")


class TestMakefile:
    """Test the Makefile commands."""

    @pytest.mark.skip()
    def test_makefile_exists(self, generated_project):
        """Test that the Makefile exists and contains expected targets."""
        makefile_path = generated_project / "Makefile"
        assert makefile_path.exists()

        with open(makefile_path, "r") as f:
            content = f.read()

        # Check for common targets
        assert "help:" in content
        assert "install:" in content
        assert "test:" in content
        assert "lint:" in content

    @pytest.mark.skipif(
        os.environ.get("SKIP_MAKE_TEST", "true").lower() == "true",
        reason="Skipping actual make command execution",
    )
    def test_make_help(self, generated_project):
        """Test that 'make help' runs successfully."""
        with change_dir(generated_project):
            result = subprocess.run(["make", "help"], capture_output=True, text=True)
            assert result.returncode == 0


class TestScripts:
    """Test the scripts in the template."""

    @pytest.mark.skip()
    def test_setup_script_exists(self, generated_project):
        """Test that the setup script exists and is executable."""
        setup_script = generated_project / "scripts" / "setup.sh"
        assert setup_script.exists()

        # Check if file is executable
        assert os.access(setup_script, os.X_OK) or setup_script.stat().st_mode & 0o111

    @pytest.mark.skip()
    def test_setup_sql_exists(self, generated_project):
        """Test that the setup SQL script exists."""
        setup_sql = generated_project / "scripts" / "setup.sql"
        assert setup_sql.exists()

        with open(setup_sql, "r") as f:
            content = f.read()

        # Basic check for SQL content
        assert "CREATE" in content or "SELECT" in content or "INSERT" in content


class TestCIConfiguration:
    """Test the CI configuration files."""

    @pytest.mark.skip()
    def test_github_workflow_exists(self, generated_project):
        """Test that GitHub workflow files exist if GitHub was selected as CI tool."""
        github_dir = generated_project / ".github" / "workflows"
        if os.path.exists(github_dir):
            workflow_files = list(github_dir.glob("*.yml"))
            assert len(workflow_files) > 0

            # Check content of the first workflow file
            with open(workflow_files[0], "r") as f:
                content = f.read()

            assert "name:" in content
            assert "jobs:" in content

    @pytest.mark.skip()
    def test_gitlab_ci_exists(self, generated_project):
        """Test that GitLab CI file exists if GitLab was selected as CI tool."""
        gitlab_ci = generated_project / ".gitlab-ci.yml"
        if os.path.exists(gitlab_ci):
            with open(gitlab_ci, "r") as f:
                content = f.read()

            assert "stages:" in content
            assert "test:" in content
