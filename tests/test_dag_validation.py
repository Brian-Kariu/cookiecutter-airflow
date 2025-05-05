import os

import pytest
from airflow.exceptions import AirflowDagCycleException
from airflow.models import DagBag
from airflow.utils.dag_cycle_tester import check_cycle
from pendulum import datetime

APPROVED_TAGS = {
    "maintainance",
}


def get_dags():
    """
    Generate a tuple of dag_id, <DAG objects> in the DagBag
    """

    dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


def test_dags_parse():
    """
    Test that all dags can parse on the UI.
    """
    dagbag = DagBag(include_examples=False)
    dagbag.collect_dags(
        dag_folder=f"{os.environ.get('AIRFLOW_HOME')}/dags",
        include_examples=False,
    )
    assert dagbag.import_errors == {}


def test_no_cycles():
    """
    Test that all dags have no cycles.
    i.e the tasks dependencies do not form loops.
    """
    dag_bag = DagBag(include_examples=False)
    try:
        for _, dag in dag_bag.dags.items():
            check_cycle(dag)
    except AirflowDagCycleException:
        pytest.fail(f"DID RAISE {AirflowDagCycleException}")


def test_task_parameters():
    """
    Test all dags have set owner and catchup to false
    """
    dag_bag = DagBag(include_examples=False)
    for dag_id, dag in dag_bag.dags.items():
        for task_id, task in dag.task_dict.items():
            assert task.owner, f"Task {task_id} in DAG {dag_id} has no owner set"
            assert dag.catchup is False, (
                f"Task {task_id} in DAG {dag_id} has not set catchup to False"
            )


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    """
    test if a DAG is tagged and if those TAGs are in the approved list
    """
    assert dag.tags, f"{dag_id} in {fileloc} has no tags"
    if APPROVED_TAGS:
        assert not set(dag.tags) - APPROVED_TAGS


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_task(dag_id, dag, fileloc):
    """
    Test if all DAGs contain a task or taskgroup
    and all tasks use the trigger_rule all_success
    """
    has_task = len(dag.tasks) > 0

    has_task_group = dag.task_group
    assert has_task or has_task_group, f"DAG {dag_id} has no tasks or task groups"
    for task in dag.tasks:
        t_rule = task.trigger_rule
        assert t_rule == "all_success", (
            f"{task} in {dag_id} has the trigger rule {t_rule}"
        )


def test_dag_ids_unique():
    """
    Test that all DAG IDs are unique globally.
    """
    dag_bag = DagBag(include_examples=False)
    dag_ids = [dag.dag_id for dag in dag_bag.dags.values()]
    unique_dag_ids = set(dag_ids)

    assert len(dag_ids) == len(unique_dag_ids), "DAG IDs are not unique"


@pytest.mark.skip()
def test_canary_dag(capsys):
    canary_dag = None

    for dag_id, dag, _ in get_dags():
        if dag_id == "canary_dag":
            canary_dag = dag
            break

    assert canary_dag is not None
    result = canary_dag.test(execution_date=datetime(2025, 5, 5))
    assert result is not None

    captured = capsys.readouterr()
    assert "canary_dag ran successfully" in captured.out
