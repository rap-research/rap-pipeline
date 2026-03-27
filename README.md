# rap-pipeline

arXiv 논문 자동 수집 및 citation 업데이트 파이프라인
Apache Airflow 기반의 데이터 수집 파이프라인으로, 매일 arXiv 논문을 수집하고 Semantic Scholar API를 통해 인용수를 업데이트합니다.

---

## 기술 스택

- **Python** 3.13
- **Apache Airflow** 3.1.3
- **PostgreSQL** + pgvector
- **uv** (패키지 매니저)

---

## 프로젝트 구조

```
rap-pipeline/
├── dags/
│   ├── collect_papers_dag.py     # arXiv 논문 수집 DAG
│   └── update_citations_dag.py   # Citation 업데이트 DAG
├── .airflow/                     # Airflow 자동 생성 파일 (git 제외)
├── .env                          # 환경변수 (git 제외)
├── .env.example                  # 환경변수 예시
├── .gitignore
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 시작하기

### 사전 요구사항

- Python 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 설치

### 1. 레포 클론

```bash
git clone https://github.com/your-id/rap-pipeline.git
cd rap-pipeline
```

### 2. 가상환경 생성 및 의존성 설치

```bash
uv venv
source .venv/bin/activate

# Airflow 설치 (constraint 파일 사용)
AIRFLOW_VERSION=3.1.3
PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# DAG 의존성 설치
uv sync
```

### 3. 환경변수 설정

```bash
cp .env.example .env
```

### 4. Airflow 실행

```bash
make up
```

→ `localhost:8080` 접속

### 5. 초기 아이디/비밀번호 확인

```bash
cat .airflow/simple_auth_manager_passwords.json.generated
```

---

## 명령어

```bash
make up       # Airflow 실행
make down     # Airflow 종료
make restart  # Airflow 재시작
make logs     # 스케줄러 로그 확인
make help     # 명령어 목록
```

---

## DAG 목록

| DAG | 스케줄 | 설명 |
|---|---|---|
| `collect_papers_dag` | 매일 02:00 (UTC) | arXiv에서 전날 논문 수집, 임베딩, 태깅 |
| `update_citations_dag` | 매일 03:00 (UTC) | Semantic Scholar API로 citation 업데이트 |

---

## 환경변수 목록

| 변수 | 설명 | 기본값 |
|---|---|---|
| `AIRFLOW__CORE__LOAD_EXAMPLES` | 예제 DAG 로드 여부 | `False` |
| `AIRFLOW__WEBSERVER__WEB_SERVER_PORT` | Airflow UI 포트 | `8080` |
| `AIRFLOW__WEBSERVER__DEFAULT_UI_TIMEZONE` | Airflow UI 타임존 | `Asia/Seoul` |

---

## 주의사항

- Airflow 메타DB는 로컬 개발 시 SQLite를 사용합니다. (`.airflow/airflow.db`)
- 프로덕션 환경에서는 PostgreSQL로 변경을 권장합니다.
- Semantic Scholar API는 100 req/5min 제한이 있어 요청 간 3초 간격을 둡니다.
- arXiv API는 요청 간 3초 간격을 권장합니다.