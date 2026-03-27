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

    @task
    def parse_embed(raw_path: str) -> str:
        from pipeline.process.parser import parse_embed_save
        return parse_embed_save(raw_path)

    @task
    def tag(raw_path: str) -> str:
        from pipeline.process.tagger import tag_papers
        return tag_papers(raw_path)

    @task
    def save(embedded_path: str, tags_path: str, **context) -> str:
        from pipeline.process.tagger import save_processed
        return save_processed(embedded_path, tags_path, context["logical_date"])

    raw = collect()
    save(parse_embed(raw), tag(raw))


collect_papers_dag()
