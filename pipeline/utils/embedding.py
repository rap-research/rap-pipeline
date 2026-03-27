import logging

from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_DEVICE, EMBEDDING_MODEL

log = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        log.info("임베딩 모델 로딩: %s", EMBEDDING_MODEL)
        _model = SentenceTransformer(EMBEDDING_MODEL, device=EMBEDDING_DEVICE)
    return _model


def encode(texts: list[str]) -> list[list[float]]:
    """텍스트 리스트를 임베딩 벡터 리스트로 변환"""
    model = _get_model()
    return model.encode(texts, show_progress_bar=True).tolist()
