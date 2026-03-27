import json
import logging
import os
from datetime import date, datetime

import arxiv
import pandas as pd

log = logging.getLogger(__name__)

from config.settings import (
    COLLECT_CATEGORIES,
    COLLECT_MAX_RESULTS,
    COLLECT_START_DATE,
    RAW_DATA_DIR,
)


def fetch_papers(execution_date: datetime) -> str:
    """
    수집 모드 결정:
    - COLLECT_START_DATE 있음 → 해당 날짜 ~ 오늘까지 전체 수집 (형식: YYYY-MM-DD)
    - COLLECT_START_DATE 없음 → 오늘 데이터만 수집

    결과 제한:
    - COLLECT_MAX_RESULTS 있음 → 최신순으로 N개만
    - COLLECT_MAX_RESULTS 없음 → 전체

    결과를 RAW_DATA_DIR/YYYY-MM-DD.parquet으로 저장 후 파일 경로 반환
    """
    exec_date: date = (
        execution_date.date() if isinstance(execution_date, datetime) else execution_date
    )

    # 수집 날짜 범위 결정
    if COLLECT_START_DATE:
        start = date.fromisoformat(COLLECT_START_DATE)
    else:
        start = exec_date
    end = exec_date

    # arXiv 쿼리 구성
    date_query = f"submittedDate:[{start.strftime('%Y%m%d')}0000 TO {end.strftime('%Y%m%d')}2359]"
    cat_query = " OR ".join(f"cat:{c}" for c in COLLECT_CATEGORIES)
    query = f"({cat_query}) AND {date_query}"

    # 3초 딜레이는 Client가 페이지 요청 사이에 자동 적용
    client = arxiv.Client(delay_seconds=3.0, num_retries=3)
    search = arxiv.Search(
        query=query,
        max_results=COLLECT_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    log.info("query: %s", query)

    records = []
    for paper in client.results(search):
        arxiv_id = paper.entry_id.split("/abs/")[-1].split("v")[0]
        log.info("[%s] %s", arxiv_id, paper.title)
        records.append({
            "arxiv_id":     arxiv_id,
            "title":        paper.title,
            "authors":      json.dumps([a.name for a in paper.authors]),
            "abstract":     paper.summary.replace("\n", " "),
            "category":     paper.categories[0] if paper.categories else "",
            "published_at": paper.published,
            "arxiv_url":    f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url":      f"https://arxiv.org/pdf/{arxiv_id}",
        })

    df = pd.DataFrame(records).drop_duplicates(subset=["arxiv_id"])
    log.info("수집 완료: 총 %d건 (중복 제거 후)", len(df))

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    file_path = os.path.join(RAW_DATA_DIR, f"{exec_date.strftime('%Y-%m-%d')}.parquet")
    df.to_parquet(file_path, index=False)
    log.info("저장 완료: %s", file_path)

    return file_path
