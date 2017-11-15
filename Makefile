PYTHON=python3

PIP=venv/bin/python -m pip
FLAKE=venv/bin/flake8
PYTEST=venv/bin/py.test

.PHONY: help clean delpyc tests flake quality

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  clean               -- to clean local repository from all stuff created during development"
	@echo "  delpyc              -- to remove all *.pyc files, this is recursive from the current directory"
	@echo "  flake               -- to launch Flake8 checking on boussole code (not the tests)"
	@echo "  tests               -- to launch tests using py.test"
	@echo "  quality             -- to launch Flake8 checking and tests with py.test"
	@echo "  release             -- to release new package on Pypi (WARNING)"
	@echo

delpyc:
	find . -name "*\.pyc"|xargs rm -f

clean: delpyc
	rm -Rf venv dist .tox boussole.egg-info .cache tests/__pycache__/

venv:
	$(PYTHON) -m venv venv
	# This is required for those ones using ubuntu<16.04
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools

install: venv
	$(PIP) install -e .

install-dev: install
	$(PIP) install -r requirements/dev.txt

flake:
	$(FLAKE) --show-source boussole

tests:
	$(PYTEST) -vv tests

quality: tests flake

release:
	python setup.py sdist
	python setup.py sdist upload
