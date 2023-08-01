PROJECT = "TagMark\(Python\)"

all: install lint test build

install: ;@echo "Installing ${PROJECT}.....\n"; \
    poetry install

lint: ;@echo "Linting ${PROJECT}.....\n"; \
	black .; \
	isort --profile black .; \
	flake8 --ignore=E203,E501,W503 --exclude=.venv .

test: ;@echo "Testing ${PROJECT}.....\n"; \
    poetry run pytest -v --cov=tagmark --cov-report=term-missing tests/

build: ;@echo "Building ${PROJECT}.....\n"; \
    poetry build

clean: ;@echo "Cleaning ${PROJECT}.....\n"; \
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf; \
    rm -rf dist; \
	rm -rf .coverage; \
	rm -rf .pytest_cache; \
	rm -rf htmlcov

changelog: ;@echo "Making ${PROJECT} Changelog......\n"; \
	git log $(o)..$(n) --oneline --abbrev-commit --pretty="* %h %s" > $(f) && \
	echo "changelog between $(o) and $(n) has been written into file $(f)"

.PHONY: install lint test build clean changelog