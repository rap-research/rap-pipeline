import json
import logging
import os
from datetime import datetime

import pandas as pd
from openai import OpenAI

from config.settings import OPENAI_API_KEY, PROCESSED_DATA_DIR, TAGGING_MODEL

log = logging.getLogger(__name__)

_client: OpenAI | None = None

_PROMPT = """\
아래 논문 초록을 보고 JSON 형식으로만 반환해줘.
{
  "topics": ["topic1", "topic2", ...],
  "keywords": ["keyword1", "keyword2", ...]
}
topics는 3~5개, keywords는 5~10개."""


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _tag(abstract: str) -> tuple[list[str], list[str]]:
    """abstract → (topics, keywords), 실패 시 빈 배열 반환"""
    try:
        response = _get_client().chat.completions.create(
            model=TAGGING_MODEL,
            messages=[
                {"role": "user", "content": f"{_PROMPT}\n\n{abstract}"},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("topics", []), result.get("keywords", [])
    except Exception as e:
        log.warning("태깅 실패: %s", e)
        return [], []


def tag_papers(raw_path: str) -> str:
    """
    raw parquet에서 abstract 읽어 topics, keywords 추출
    결과를 _tags.json으로 저장
    반환: 저장된 태그 파일 경로
    """
    df = pd.read_parquet(raw_path)
    tags: dict[str, dict] = {}
    for _, row in df.iterrows():
        topics, keywords = _tag(row.get("abstract") or "")
        tags[row["arxiv_id"]] = {"topics": topics, "keywords": keywords}
        log.info("[%s] 태깅 완료: topics=%s", row["arxiv_id"], topics)

    filename = os.path.basename(raw_path).replace(".parquet", "_tags.json")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    tags_path = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(tags_path, "w") as f:
        json.dump(tags, f, ensure_ascii=False)
    log.info("태그 저장 완료: %s", tags_path)
    return tags_path


def save_processed(embedded_path: str, tags_path: str, execution_date: datetime) -> str:
    """
    임베딩 중간 parquet + 태그 JSON을 병합하여 최종 processed parquet 저장
    중간 파일(embedded, tags) 삭제
    반환: 저장된 파일 경로
    """
    df = pd.read_parquet(embedded_path)
    with open(tags_path) as f:
        tags = json.load(f)

    df["topics"]   = df["arxiv_id"].map(lambda aid: tags.get(aid, {}).get("topics",   []))
    df["keywords"] = df["arxiv_id"].map(lambda aid: tags.get(aid, {}).get("keywords", []))

    exec_date = (
        execution_date.date() if isinstance(execution_date, datetime) else execution_date
    )
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    file_path = os.path.join(PROCESSED_DATA_DIR, f"{exec_date.strftime('%Y-%m-%d')}.parquet")
    df.to_parquet(file_path, index=False)

    os.remove(embedded_path)
    os.remove(tags_path)
    log.info("저장 완료: %s", file_path)
    return file_path
