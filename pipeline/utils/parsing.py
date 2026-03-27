import logging
import tempfile
import urllib.request

from llama_parse import LlamaParse

from config.settings import LLAMA_CLOUD_API_KEY

log = logging.getLogger(__name__)

_parser: LlamaParse | None = None


def _get_parser() -> LlamaParse:
    global _parser
    if _parser is None:
        _parser = LlamaParse(
            api_key=LLAMA_CLOUD_API_KEY,
            result_type="markdown",
            verbose=False,
        )
    return _parser


def parse_pdf(pdf_url: str) -> str | None:
    """
    PDF URL을 LlamaParse로 파싱하여 마크다운 텍스트 반환
    실패 시 None 반환
    """
    try:
        parser = _get_parser()
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            urllib.request.urlretrieve(pdf_url, f.name)
            documents = parser.load_data(f.name)
        return "\n\n".join(doc.text for doc in documents)
    except Exception as e:
        log.warning("LlamaParse 실패 (url=%s): %s", pdf_url, e)
        return None
