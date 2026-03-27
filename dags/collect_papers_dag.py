from datetime import datetime, timezone

from airflow.sdk import dag, task

from config.settings import SCHEDULE_COLLECT


@dag(
    dag_id="collect_papers_dag",
    schedule=SCHEDULE_COLLECT,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["collect"],
)
def collect_papers_dag():
    @task
    def collect(**context):
        from pipeline.collect.arxiv_client import fetch_papers
        return fetch_papers(context["logical_date"])

    collect()


collect_papers_dag()
