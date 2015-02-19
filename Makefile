.PHONY: clean deps develop clean-build lint test coverage coverage-html tox migrate runserver
PYTEST_OPTS :=
COVER := nobot
APP := .

help:
	@echo "clean-build - remove build artifacts"
	@echo "develop - install all packages required for development"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - generate test coverage report"
	@echo "coverage-html - generate test coverage report, html output"
	@echo "tox - Run all tests in a tox container"


clean: clean-build


develop:
	@echo "--> Installing python dependencies"
	pip install --upgrade pip setuptools wheel
	pip install --use-wheel -e .
	pip install --use-wheel -e .[tests]
	@echo ""


clean-build:
	find . -name "*.pyc" -exec rm {} \;
	rm -fr build/ src/build
	rm -fr dist/ src/dist
	rm -fr *.egg-info src/*.egg-info
	rm -fr htmlcov/


lint:
	flake8 nobot --ignore='E122,E124,E125,E126,E128,E501,F403' --exclude="**/migrations/**"


test:
	@py.test ${PYTEST_OPTS} ${APP}


coverage:
	py.test --cov=${COVER} --cov-report=term-missing ${PYTEST_OPTS} ${APP}


coverage-html:
	py.test --cov=${COVER} --cov-report=html ${PYTEST_OPTS} ${APP}


tox:
	@tox
