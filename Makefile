PYTHON ?= python3.11
VENV_DIR ?= .venv

.PHONY: setup install-dev install-hooks docs docs-build

setup: install-dev install-hooks
	@echo "Developer environment is ready."

install-dev:
	@test -d "$(VENV_DIR)" || $(PYTHON) -m venv "$(VENV_DIR)"
	@"$(VENV_DIR)/bin/python" -m pip install --upgrade pip && "$(VENV_DIR)/bin/python" -m pip install -e ".[dev]"

install-hooks:
	@"$(VENV_DIR)/bin/pre-commit" install && "$(VENV_DIR)/bin/pre-commit" install --hook-type pre-push

docs:
	@cd website && (test -d node_modules || npm install) && npm start

docs-build:
	@cd website && (test -d node_modules || npm install) && npm run build
