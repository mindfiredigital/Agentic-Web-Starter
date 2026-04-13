PYTHON ?= python3.11
VENV_DIR ?= .venv

.PHONY: setup install-dev install-hooks

setup: install-dev install-hooks
	@echo "Developer environment is ready."

install-dev:
	@test -d "$(VENV_DIR)" || $(PYTHON) -m venv "$(VENV_DIR)"
	@. "$(VENV_DIR)/bin/activate" && python -m pip install --upgrade pip && python -m pip install -e ".[dev]"

install-hooks:
	@. "$(VENV_DIR)/bin/activate" && pre-commit install && pre-commit install --hook-type pre-push
