help:
	@echo  "Development makefile"
	@echo
	@echo  "Usage: make <target>"
	@echo  "Targets:"
	@echo  "    up      Updates dev/test dependencies"
	@echo  "    deps    Ensure dev/test dependencies are installed"
	@echo  "    check   Checks that build is sane"
	@echo  "    test    Runs all tests"
	@echo  "    style   Auto-formats the code"
	@echo  "    lint    Auto-formats the code and check type hints"
	@echo  "    build   Build wheel file and tar file from source to dist/"

up:
	uv lock --upgrade
	uv sync --frozen

lock:
	uv lock

venv:
	pdm venv create $(options) $(version)

venv312:
	$(MAKE) venv version=3.12

deps:
	uv sync --all-extras --all-groups $(options)

start:
	pre-commit install
	$(MAKE) deps

_check:
	uvx --from fastdevcli-slim fast check
check: deps _build _check

_lint:
	uvx --from fastdevcli-slim fast lint $(options)
lint: deps _build _lint

_test:
	uvx --from fastdevcli-slim fast test
test: deps _test

_style:
	uvx --from fastdevcli-slim fast lint --skip-mypy
style: deps _style

_build:
	rm -fR dist/
	uv build
build: deps _build

bump_part = patch

_bump:
	uvx --from fastdevcli-slim fast bump $(bump_part) $(bump_opts)
bump: deps _bump

release: deps _build
	# fast upload -- Use github action instead
	$(MAKE) _bump bump_opts=--commit
	$(MAKE) deps
	uvx --from fastdevcli-slim fast tag

ci: check _test
