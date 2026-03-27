import os
from dotenv import load_dotenv

load_dotenv()

# ── 수집 설정 ────────────────────────────────────────────────────────
COLLECT_CATEGORIES      = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
COLLECT_MAX_RESULTS     = int(os.getenv("COLLECT_MAX_RESULTS", 100))
COLLECT_DATE_RANGE_DAYS = int(os.getenv("COLLECT_DATE_RANGE_DAYS", 1))

# ── 스케줄 설정 ──────────────────────────────────────────────────────
SCHEDULE_COLLECT   = os.getenv("SCHEDULE_COLLECT",   "0 2 * * *")
SCHEDULE_CITATIONS = os.getenv("SCHEDULE_CITATIONS", "0 3 * * *")

# ── OpenAI 설정 ──────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAGGING_MODEL  = os.getenv("TAGGING_MODEL", "gpt-4o-mini")

# ── 임베딩 설정 ──────────────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_DIM   = int(os.getenv("EMBEDDING_DIM", 1024))

# ── DB 설정 ──────────────────────────────────────────────────────────
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB       = os.getenv("POSTGRES_DB", "research_agent")
POSTGRES_USER     = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
