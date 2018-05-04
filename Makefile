.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 istr tests

test: ## run tests quickly with the default Python
	py.test


test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source istr -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/istr.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ istr
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install


PIP_TOOLS_VERSION=2.0.2

upgrade-requirements-files:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find $(CURDIR) -maxdepth 3 -name 'requirements*.in' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			final_reqfile="$${reqfile%.*}.txt";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			pip-compile -U --output-file $$final_reqfile $$reqfile; done


compile-requirements-files:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find $(CURDIR) -maxdepth 3 -name 'requirements*.in' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			final_reqfile="$${reqfile%.*}.txt";\
			echo "Compiling $$reqfile to $$final_reqfile"; \
			pip-compile --output-file $$final_reqfile $$reqfile; done

sync-installed-pip-requirements:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		reqs=""; for reqfile in $$(find $(CURDIR) -maxdepth 3 -name 'requirements*.txt' -not -name '*-py2.txt' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			reqs="$$reqs $$reqfile"; done; \
			pip-sync $$reqs

upgrade-pip-requirement:
	pip install 'pip-tools==$(PIP_TOOLS_VERSION)' && \
		for reqfile in $$(find $(CURDIR) -maxdepth 3 -name 'requirements*.in' -not -name '*-py2.in' -print); do \
			reqfile=$$(realpath --relative-to=$(CURDIR) $$reqfile); \
			final_reqfile="$${reqfile%.*}.txt";\
			echo "Upgrading $(req) in $$final_reqfile"; \
			pip-compile --output-file $$final_reqfile $$reqfile -P $(req); done
