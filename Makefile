PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo ""
	@echo "  clean               -- to clean EVERYTHING"
	@echo "  clean-install       -- to clean installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo ""
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  tests               -- to launch tests using Pytest"
	@echo "  quality             -- to launch Flake8 checking and Pytest"
	@echo

clean-pycache:
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
	rm -Rf .pytest_cache
	rm -Rf .tox
.PHONY: clean-pycache

clean-install:
	rm -Rf $(VENV_PATH)
	rm -Rf boussole.egg-info
.PHONY: clean-install

clean: clean-install clean-pycache
.PHONY: clean

venv:
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using ubuntu<16.04
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install: venv
	mkdir -p data
	$(PIP) install -e .[dev]
.PHONY: install

flake:
	$(FLAKE) --show-source --statistics boussole tests
.PHONY: flake

tests:
	$(PYTEST) -vv tests/
.PHONY: tests

quality: tests flake
.PHONY: quality
