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
	just up

lock:
	just lock

venv:
	just venv $(options) $(version)

venv312:
	$(MAKE) venv version=3.12

deps:
	just deps $(options)

start:
	just start

_check:
	jsut _check
check: deps _build _check

_lint:
	just _lint $(options)
lint: deps _build _lint

_test:
	just _test
test: deps _test

_style:
	just _lint --skip-mypy
style: deps _style

_build:
	just _build
build: deps _build

bump_part = patch

_bump:
	just _bump $(bump_part) $(bump_opts)
bump: deps _bump

release: deps _build
	just release

ci: check _test
