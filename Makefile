.PHONY: up down restart logs help

# 환경변수 로드 후 Airflow 실행
up:
	mkdir -p .airflow && \
	set -a && source .env && set +a && \
	export AIRFLOW_HOME=$(PWD)/.airflow && \
	export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="sqlite:///$(PWD)/.airflow/airflow.db" && \
	export AIRFLOW__CORE__DAGS_FOLDER=$(PWD)/dags && \
	airflow standalone

# Airflow 종료
down:
	pkill -f airflow || true

# Airflow 재시작
restart: down up

# Airflow 로그 확인
logs:
	tail -f .airflow/logs/scheduler/latest/*.log

help:
	@echo "사용 가능한 명령어:"
	@echo "  make up       - Airflow 실행"
	@echo "  make down     - Airflow 종료"
	@echo "  make restart  - Airflow 재시작"
	@echo "  make logs     - 스케줄러 로그 확인"