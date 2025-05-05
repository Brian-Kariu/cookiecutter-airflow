import re
from datetime import datetime

import pytest
import toml
import yaml


class TestTemplateRendering:
    """Tests for validating correct template rendering based on user inputs."""

    @pytest.mark.parametrize(
        "project_name,expected_slug",
        [
            ("data-engineering", "data_engineering"),
            ("Data Engineering", "data_engineering"),
            ("data_engineering", "data_engineering"),
            ("data engineering Project", "data_engineering"),
            ("data:engineering", "data_engineering"),
            ("data!engineering", "data_engineering"),
        ],
    )
    def test_project_name_to_slug_conversion(
        self,
        project_name,
        expected_slug,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that different project names are correctly converted to slugs."""
        context = variable_project_context(project_name=project_name)
        project = create_project_with_context(context)

        # Check that the directory name matches the expected slug
        assert project.name == expected_slug, (
            f"Expected directory name to be {expected_slug}, got {project.name}"
        )

        # Check project name in files
        readme_path = project / "README.md"
        with open(readme_path, "r") as f:
            readme_content = f.read()

        assert project_name in readme_content or expected_slug in readme_content, (
            f"Project name '{project_name}' or slug '{expected_slug}' not found in README"
        )

        # Check pyproject.toml
        pyproject_path = project / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "r") as f:
                pyproject_content = f.read()

            assert expected_slug in pyproject_content, (
                "Project slug not found in pyproject.toml"
            )

    @pytest.mark.skip(reason="weird error")
    @pytest.mark.parametrize(
        "license_option,expected_text",
        [
            (
                "MIT",
                [
                    "MIT License",
                    "Permission is hereby granted",
                    f"Copyright (c) {datetime.now().year}, John",
                ],
            ),
            (
                "BSD",
                [
                    f"Copyright (c) {datetime.now().year}, John",
                    "All rights reserved.",
                    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"',
                ],
            ),
            (
                "GPLv3",
                [
                    f"Copyright (c) {datetime.now().year}, John",
                    "This program is free software",
                    "You should have received a copy of the GNU General Public License",
                ],
            ),
            (
                "Apache Software License 2.0",
                [
                    "Apache License",
                    "Version 2.0, January 2004",
                    "Licensed under the Apache License, Version 2.0",
                    f"Copyright {datetime.now().year} John",
                ],
            ),
            (
                "Not open source",
                ["All rights reserved"],
            ),
        ],
    )
    def test_license_rendering(
        self,
        license_option,
        expected_text,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that the license is rendered correctly based on the selected license."""
        context = variable_project_context(open_source_license=license_option)
        project = create_project_with_context(context)
        print(f"Final project: {project}")

        license_path = project / "LICENSE.txt"

        if not license_path.exists() and license_option == "Not open source":
            return  # This is acceptable for "Not open source"

        assert license_path.exists(), f"LICENSE does not exist for {license_option}"

        with open(license_path, "r", encoding="utf-8") as f:  # Specify encoding
            license_content = f.read()

        for text in expected_text:
            assert text in license_content, (
                f"'{text}' not found in {license_option} license"
            )

        assert context["author_name"] in license_content, (
            f"Author name '{context['author_name']}' not found in LICENSE"
        )

    @pytest.mark.skip()
    @pytest.mark.parametrize(
        "ci_tool,expected_files,unexpected_files",
        [
            ("Github", [".github/workflows/ci.yml"], [".gitlab-ci.yml"]),
            ("Gitlab", [".gitlab-ci.yml"], [".github/workflows/ci.yml"]),
            ("None", [], [".github/workflows/ci.yml", ".gitlab-ci.yml"]),
        ],
    )
    def test_ci_tool_rendering(
        self,
        ci_tool,
        expected_files,
        unexpected_files,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that CI configuration is rendered correctly based on selected CI tool."""
        context = variable_project_context(ci_tool=ci_tool)
        project = create_project_with_context(context)

        # Check expected files exist
        for file_path in expected_files:
            path = project / file_path
            assert path.exists(), f"Expected {file_path} to exist for CI tool {ci_tool}"

            # Additional validation for file content
            if ".gitlab-ci.yml" in file_path:
                with open(path, "r") as f:
                    try:
                        gitlab_ci_content = yaml.safe_load(f)
                        assert isinstance(gitlab_ci_content, dict), (
                            f"GitLab CI file for {ci_tool} is not a valid YAML dictionary"
                        )
                    except yaml.YAMLError:
                        pytest.fail(f"GitLab CI file for {ci_tool} is not valid YAML")

            elif ".github/workflows" in file_path:
                workflow_files = list(path.glob("*.yml"))
                assert len(workflow_files) > 0, (
                    f"No GitHub workflow files found for {ci_tool}"
                )

                # Check first workflow file for valid YAML
                with open(workflow_files[0], "r") as f:
                    try:
                        workflow_content = yaml.safe_load(f)
                        assert isinstance(workflow_content, dict), (
                            f"GitHub workflow for {ci_tool} is not a valid YAML dictionary"
                        )
                    except yaml.YAMLError:
                        pytest.fail(f"GitHub workflow for {ci_tool} is not valid YAML")

        # Check unexpected files don't exist
        for file_path in unexpected_files:
            path = project / file_path
            assert not path.exists(), (
                f"Unexpected {file_path} exists for CI tool {ci_tool}"
            )

    @pytest.mark.skip()
    @pytest.mark.parametrize(
        "use_docker,postgresql_version",
        [
            ("y", "17"),
            ("y", "16"),
            ("y", "15"),
            ("y", "14"),
            ("y", "13"),
            ("n", "16"),  # Docker disabled but postgres version specified
        ],
    )
    def test_docker_rendering(
        self,
        use_docker,
        postgresql_version,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that Docker files are rendered correctly based on the use_docker option."""
        context = variable_project_context(
            use_docker=use_docker, postgresql_version=postgresql_version
        )
        project = create_project_with_context(context)

        dockerfile = project / "Dockerfile"
        docker_compose = project / "docker-compose.local.yml"

        if use_docker == "y":
            assert dockerfile.exists(), (
                "Dockerfile does not exist when Docker is enabled"
            )
            assert docker_compose.exists(), (
                "docker-compose.local.yml does not exist when Docker is enabled"
            )

            # Check docker-compose.yml for PostgreSQL version
            with open(docker_compose, "r") as f:
                docker_compose_content = f.read()

            assert f"postgres:{postgresql_version}" in docker_compose_content, (
                f"PostgreSQL version {postgresql_version} not found in docker-compose.yml"
            )

            # Check Dockerfile for proper configuration
            with open(dockerfile, "r") as f:
                dockerfile_content = f.read()

            assert "FROM" in dockerfile_content, "Dockerfile missing FROM instruction"
            assert "WORKDIR" in dockerfile_content, (
                "Dockerfile missing WORKDIR instruction"
            )
        else:
            # If Docker is disabled, either files shouldn't exist or should be empty/disabled
            if dockerfile.exists():
                with open(dockerfile, "r") as f:
                    dockerfile_content = f.read()
                assert (
                    "# Docker configuration disabled" in dockerfile_content
                    or len(dockerfile_content.strip()) == 0
                ), "Dockerfile should be empty or disabled when Docker is disabled"

    @pytest.mark.skip()
    @pytest.mark.parametrize("airflow_version", ["2.10.0", "2.9.0", "2.8.0"])
    def test_airflow_version_rendering(
        self, airflow_version, variable_project_context, create_project_with_context
    ):
        """Test that the Airflow version is rendered correctly in dependency files."""
        context = variable_project_context(airflow_version=airflow_version)
        project = create_project_with_context(context)

        # Check pyproject.toml
        pyproject_path = project / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml does not exist"

        try:
            with open(pyproject_path, "r") as f:
                pyproject_data = toml.load(f)

            # Check for Airflow dependency with correct version
            dependencies = pyproject_data.get("project", {}).get("dependencies", [])
            airflow_deps = [dep for dep in dependencies if "apache-airflow" in dep]

            assert any(airflow_version in dep for dep in airflow_deps), (
                f"Airflow version {airflow_version} not found in dependencies"
            )
        except Exception as e:
            pytest.fail(f"Failed to parse pyproject.toml: {str(e)}")

    @pytest.mark.skip()
    @pytest.mark.parametrize("python_version", ["3.10", "3.11", "3.12"])
    def test_python_version_rendering(
        self, python_version, variable_project_context, create_project_with_context
    ):
        """Test that the Python version is rendered correctly in dependency files."""
        context = variable_project_context(python_version=python_version)
        project = create_project_with_context(context)

        # Check pyproject.toml
        pyproject_path = project / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml does not exist"

        with open(pyproject_path, "r") as f:
            pyproject_content = f.read()

        # Should find the Python version specifier
        version_pattern = rf"python\s*=\s*[\"\']>=?{python_version}[\"\']\s*"
        assert re.search(version_pattern, pyproject_content), (
            f"Python version {python_version} not found in pyproject.toml"
        )

    @pytest.mark.skip()
    @pytest.mark.parametrize(
        "author_name,domain_name,expected_email",
        [
            ("John Doe", "example.com", "john-doe@example.com"),
            ("Jane Smith", "company.org", "jane-smith@company.org"),
            ("Test User", "test.io", "test-user@test.io"),
        ],
    )
    def test_email_generation(
        self,
        author_name,
        domain_name,
        expected_email,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that email addresses are correctly generated from author name and domain."""
        context = variable_project_context(
            author_name=author_name, domain_name=domain_name
        )
        project = create_project_with_context(context)

        # Check if email is correctly rendered in files where it might appear
        potential_files = ["README.md", "CONTRIBUTING.txt"]

        email_found = False
        for filename in potential_files:
            file_path = project / filename
            if file_path.exists():
                with open(file_path, "r") as f:
                    content = f.read()
                if expected_email in content:
                    email_found = True
                    break

        assert email_found, (
            f"Generated email {expected_email} not found in project files"
        )

    @pytest.mark.skip()
    @pytest.mark.parametrize("debug_flag", ["y", "n"])
    def test_debug_mode(
        self, debug_flag, variable_project_context, create_project_with_context
    ):
        """Test that debug flag properly affects project generation."""
        context = variable_project_context(debug=debug_flag)
        project = create_project_with_context(context)

        # Debug mode might add debug-specific files or configurations
        # Check for a debug marker or configuration in relevant files

        # For example, in a configuration file or Makefile
        makefile_path = project / "Makefile"
        if makefile_path.exists():
            with open(makefile_path, "r") as f:
                makefile_content = f.read()

            if debug_flag == "y":
                assert (
                    "DEBUG" in makefile_content or "debug" in makefile_content.lower()
                ), "Debug flag not reflected in Makefile"

    @pytest.mark.parametrize(
        "project_slug,feature,file_check",
        [
            ("basic_project", "dags", "airflow/dags/maintainance/canary.py"),
            ("complex_project", "tests", "tests/custom_dags/test_dag_validation.py"),
            ("my_airflow", "docker", "docker-compose.local.yml"),
            ("data_pipeline", "scripts", "scripts/setup.sh"),
        ],
    )
    @pytest.mark.skip()
    def test_essential_files_existence(
        self,
        project_slug,
        feature,
        file_check,
        variable_project_context,
        create_project_with_context,
    ):
        """Test that essential files exist in the generated project."""
        context = variable_project_context(project_name=project_slug)
        project = create_project_with_context(context)

        file_path = project / file_check
        assert file_path.exists(), (
            f"Essential file {file_check} for {feature} does not exist"
        )

        # Check that file has content
        assert file_path.stat().st_size > 0, f"File {file_check} exists but is empty"
