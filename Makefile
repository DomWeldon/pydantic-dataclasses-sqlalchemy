
.PHONY: setup
setup:
	poetry install

.PHONY: repl
repl:
	poetry run bpython

.PHONY: test
test:
	poetry run pytest tests/

.PHONY: fix
fix:
	poetry run black pdsqla tests
	poetry run isort .
