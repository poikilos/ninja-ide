PYTEST = pytest -v -s
CLEANUP_LIST = *.pyc *.pyo *.qmlc *.jsc

help:
	@echo "unittest		-- run unit tests"
	@echo "pep8		-- run pycodestyle"
	@echo "flake8		-- run flake8"
	@echo "lint		-- run pycodestyle and flake8"
	@echo "rc		-- build resources"


unittest:
	$(PYTEST) samurai_tests/unit

pep8:
	pycodestyle samurai_ide

flake8:
	flake8 samurai_ide

lint: pep8 flake8

rc:
	pyrcc5 samurai_ide/nresources.qrc -o samurai_ide/nresources.py

clean:
	for i in $(CLEANUP_LIST); do find . -name "$$i" -delete; done
