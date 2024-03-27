# Makefile
# https://news.ycombinator.com/item?id=35328220
.PHONY: setup
setup:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install

.PHONY: lint
lint:
	black .


.PHONY: build
build:
	 poetry install

test:
	poetry run pytest
