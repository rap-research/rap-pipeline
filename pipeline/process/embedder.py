import logging

from pipeline.utils.embedding import encode

log = logging.getLogger(__name__)


def embed_papers(papers: list[dict]) -> list[dict]:
    """
    각 청크에 bge 임베딩 추가
    반환: papers[i]["chunks"][j]["embedding"] 추가된 list[dict]
    """
    for paper in papers:
        chunks = paper.get("chunks") or []
        if not chunks:
            continue

        texts = [c["chunk_text"] for c in chunks]
        vectors = encode(texts)

        for chunk, vector in zip(chunks, vectors):
            chunk["embedding"] = vector

        log.info("[%s] 임베딩 완료: %d개 청크", paper["arxiv_id"], len(chunks))

    return papers
