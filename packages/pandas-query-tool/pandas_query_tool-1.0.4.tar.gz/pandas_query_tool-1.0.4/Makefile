.PHONY: test  clean-pyc release dist install clean dev-pkg



clean-pyc: ## remove Python file artifacts
	python scripts/clean_pyc.py


clean: clean-pyc
	python scripts/clean_build.py

test:
	cls
	pytest -v __tests 



release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python -m build -n

install:   ## install the package to the active Python's site-packages
	pip install dist/pandas_query_tool-1.0.0-py3-none-any.whl

dev-pkg: ## 
	pip install --editable .

	