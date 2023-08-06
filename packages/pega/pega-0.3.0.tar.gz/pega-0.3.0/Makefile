.PHONY: build clean release

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -f .coverage
	rm -fr .pytest_cache
	rm -fr htmlcov/
	rm -f dist/*


coverage:
	pytest --cov-report=term-missing --cov-config=pyproject.toml --cov=pega --cov=tests


checks:
	flake8 pega tests
	pytest -s


# Build source and wheel packages
build: clean checks
	hatch build


# Call example: make release version=0.3.0
release: build
	git tag -a $(version) -m 'Create version $(version)'
	git push --tags
	hatch publish
