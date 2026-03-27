import json
import logging
import os

import pandas as pd
import tiktoken

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE, PROCESSED_DATA_DIR
from pipeline.utils.parsing import parse_pdf

log = logging.getLogger(__name__)

_tokenizer = tiktoken.get_encoding("cl100k_base")


def _chunk_text(text: str) -> list[str]:
    """토큰 기반 청킹 (CHUNK_SIZE 단위, CHUNK_OVERLAP 오버랩)"""
    tokens = _tokenizer.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunks.append(_tokenizer.decode(chunk_tokens))
        if end >= len(tokens):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def parse_papers(file_path: str) -> list[dict]:
    """
    RAW_DATA_DIR parquet에서 논문 읽기
    utils/parsing.py로 PDF 파싱 후 청킹
    LlamaParse 실패 시 abstract로 폴백

    반환: papers에 chunks 필드 추가된 list[dict]
    papers[i]["chunks"] = [
        {"chunk_index": 0, "chunk_text": "..."},
        ...
    ]
    """
    df = pd.read_parquet(file_path)
    papers = df.to_dict(orient="records")

    for paper in papers:
        arxiv_id = paper["arxiv_id"]
        pdf_url   = paper.get("pdf_url", "")
        abstract  = paper.get("abstract") or ""

        text = parse_pdf(pdf_url)
        if text:
            log.info("[%s] LlamaParse 파싱 완료", arxiv_id)
        else:
            log.warning("[%s] LlamaParse 실패 → abstract로 폴백", arxiv_id)
            text = abstract

        chunks = _chunk_text(text)
        paper["chunks"] = [
            {"chunk_index": i, "chunk_text": chunk}
            for i, chunk in enumerate(chunks)
        ]
        log.info("[%s] 청크 %d개 생성", arxiv_id, len(chunks))

    return papers


def parse_embed_save(raw_path: str) -> str:
    """
    parse_papers + embed_papers 수행 후 중간 parquet 저장
    chunks(임베딩 포함)는 JSON 직렬화하여 저장
    반환: 저장된 중간 파일 경로 (_embedded.parquet)
    """
    from pipeline.process.embedder import embed_papers

    papers = parse_papers(raw_path)
    papers = embed_papers(papers)

    rows = [
        {**{k: v for k, v in p.items() if k != "chunks"}, "chunks": json.dumps(p.get("chunks") or [])}
        for p in papers
    ]
    filename = os.path.basename(raw_path).replace(".parquet", "_embedded.parquet")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    embedded_path = os.path.join(PROCESSED_DATA_DIR, filename)
    pd.DataFrame(rows).to_parquet(embedded_path, index=False)
    log.info("임베딩 중간 저장 완료: %s", embedded_path)
    return embedded_path
