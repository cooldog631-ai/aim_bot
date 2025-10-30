.PHONY: help install install-dev run test migrate init-db clean format lint docker-build docker-up

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make run          - Run the bot"
	@echo "  make test         - Run tests with coverage"
	@echo "  make migrate      - Run database migrations"
	@echo "  make init-db      - Initialize database"
	@echo "  make clean        - Clean up cache and temporary files"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Run linters (flake8, mypy)"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start services with docker-compose"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

run:
	python src/main.py

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

migrate:
	alembic upgrade head

init-db:
	python scripts/init_db.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

lint:
	flake8 src/ tests/ scripts/
	mypy src/

docker-build:
	docker build -t aim_bot:latest -f docker/Dockerfile .

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down
