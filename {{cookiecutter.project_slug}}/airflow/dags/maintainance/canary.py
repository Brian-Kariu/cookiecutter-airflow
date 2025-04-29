"""
This DAG is used to by the airflow liveness check and is crucial.
"""

from datetime import timedelta

import pendulum

from airflow.decorators import dag, task


@dag(
    dag_id="canary_dag",
    default_args={
        "owner": "airflow",
    },
    schedule_interval="*/5 * * * *",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    dagrun_timeout=timedelta(minutes=5),
    is_paused_upon_creation=False,
    catchup=False,
    tags=["maintainance"],
)
def run_canary() -> None:
    """
    This dag is used to by the airflow liveness check and is crucial.
    """

    @task.bash
    def canary() -> str:
        """
        Execute a dummy task
        """
        return "echo 'Hello World!'"

    canary()


canary_dag = run_canary()
