short_ver = $(shell git describe --abbrev=0)
long_ver = $(shell git describe --long 2>/dev/null || echo $(short_ver)-0-unknown-g`git describe --always`)

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

.PHONY: rpm
rpm:
	git archive --prefix=cloud-emission-estimator/ HEAD -o rpm-src-cloud-emission-estimator.tar
	rpmbuild -bb cloud-emission-estimator.spec \
		--define '_sourcedir $(CURDIR)' \
		--define '_rpmdir $(PWD)/rpms' \
		--define 'major_version $(short_ver)' \
		--define 'minor_version $(subst -,.,$(subst $(short_ver)-,,$(long_ver)))'

.PHONY: clean
clean:
	$(RM) rpm-src-cloud-emission-estimator.tar
	$(RM) -r rpms/
