PROJECT = "TagMark\(Python\)"

all: install lint test build

install: ;@echo "Installing ${PROJECT}.....\n"; \
    poetry install

lint: ;@echo "Linting ${PROJECT}.....\n"; \
	black .; \
	isort --profile black .; \
	flake8 --ignore=E501,W503 .

test: ;@echo "Testing ${PROJECT}.....\n"; \
    poetry run pytest -v --cov=tagmark tests/

build: ;@echo "Building ${PROJECT}.....\n"; \
    poetry build

clean: ;@echo "Cleaning ${PROJECT}.....\n"; \
    rm -rf dist; \
	rm -rf .coverage

.PHONY: install lint test build clean