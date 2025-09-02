RAWVERSION = $(filter-out __version__ = , $(shell grep __version__ selectjs/__init__.py))
VERSION = $(strip $(shell echo $(RAWVERSION)))

PACKAGE = django-selectjs

clean:
	rm -rf *.tar.gz dist build *.egg-info *.rpm
	find . -name "*.pyc" | xargs rm
	find . -name "__pycache__" | xargs rm -rf

version:
	@echo $(VERSION)

dist: clean
	@python -m build

release: dist
	@bin/release.sh

compile: uv.lock
	# @uv pip compile --group demo --group docs --group test pyproject.toml -o requirements.txt
	@uv pip compile pyproject.toml -o requirements.txt

MAIN_BRANCH = master

# --- Gate checks ---
check-branch:
	@branch="$$(git rev-parse --abbrev-ref HEAD)"; \
	[[ "$$branch" == "$(MAIN_BRANCH)" ]] || { echo "You're not on $(MAIN_BRANCH); aborting."; exit 1; }

check-clean:
	@[[ -z "$$(git status --untracked-files=no --porcelain)" ]] || { echo "You have uncommitted changes; aborting."; exit 1; }

# --- Shared release pipeline ---
# Expects BUMP=dev|patch|minor|major
_release: compile check-branch check-clean
	@echo "Releasing $(BUMP) version"
	@bumpversion "$(BUMP)"
	@bin/release.sh

# --- Explicit release targets (better tab-complete & discoverability) ---
release-dev:
	$(MAKE) _release BUMP=dev

release-patch:
	$(MAKE) _release BUMP=patch

release-minor:
	$(MAKE) _release BUMP=minor

release-major:
	$(MAKE) _release BUMP=major

pypi: dist
	@twine upload dist/*

tox:
	# create a tox pyenv virtualenv based on 2.7.x
	# install tox and tox-pyenv in that ve
	# actiave that ve before running this
	@tox
