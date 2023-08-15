PYTHON ?= PYTHONDONTWRITEBYTECODE=1 python3

.PHONY: test
test:
	$(PYTHON) -m pytest -vv tests/

.PHONY: flake8-src
flake8-src:
	$(PYTHON) -m flake8 cloud_emission_estimator/

.PHONY: flake8-test
flake8-test:
	$(PYTHON) -m flake8 tests/

.PHONY: flake8
flake8: flake8-src flake8-test

.PHONY: mypy-src
mypy-src:
	mypy cloud_emission_estimator/

.PHONY: mypy-test
mypy-test:
	mypy tests/

.PHONY: mypy
mypy: mypy-src mypy-test

.PHONY: test-static
test-static: flake8 mypy
