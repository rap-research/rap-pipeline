import os
from dotenv import load_dotenv

load_dotenv()

# ── 수집 설정 ────────────────────────────────────────────────────────
COLLECT_CATEGORIES  = ["cs.AI", "cs.MA", "cs.SE"]
COLLECT_START_DATE  = os.getenv("COLLECT_START_DATE", None)   # YYYY-MM-DD, 없으면 오늘만 수집
_max = os.getenv("COLLECT_MAX_RESULTS", None)
COLLECT_MAX_RESULTS = int(_max) if _max else None              # 없으면 전체 수집

# ── 파일 저장 경로 ───────────────────────────────────────────────────
RAW_DATA_DIR       = os.getenv("RAW_DATA_DIR",       "data/raw")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR", "data/processed")

# ── 스케줄 설정 ──────────────────────────────────────────────────────
SCHEDULE_COLLECT   = os.getenv("SCHEDULE_COLLECT",   "0 2 * * *")
SCHEDULE_CITATIONS = os.getenv("SCHEDULE_CITATIONS", "0 3 * * *")

# ── OpenAI 설정 ──────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAGGING_MODEL  = os.getenv("TAGGING_MODEL", "gpt-4o-mini")

# ── 청킹 설정 ────────────────────────────────────────────────────────
CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 512))   # 토큰 단위
CHUNK_OVERLAP = int(CHUNK_SIZE * 0.1)               # 10% 고정

# ── LlamaParse 설정 ──────────────────────────────────────────────────
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

# ── 임베딩 설정 ──────────────────────────────────────────────────────
EMBEDDING_MODEL  = os.getenv("EMBEDDING_MODEL",  "BAAI/bge-m3")
EMBEDDING_DIM    = int(os.getenv("EMBEDDING_DIM", 1024))
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")  # cpu | mps | cuda

# ── DB 설정 ──────────────────────────────────────────────────────────
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB       = os.getenv("POSTGRES_DB", "research_agent")
POSTGRES_USER     = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
