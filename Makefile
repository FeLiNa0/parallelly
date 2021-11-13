LINUX_SHELLS=dash bash zsh
STRICT_SHELLS=yash ksh
MACOS_SHELLS=bash zsh
SHELLSCRIPT=parallely
TEST_SHELLSCRIPTS=tests/bash-3.1 $(shell ls tests/*.sh)
ALL_SHELLSCRIPTS=$(TEST_SHELLSCRIPTS) $(SHELLSCRIPT)

all: install

build-readme:
	./utils/generate_readme.py ./README.template.md > ./README.md

release:
	# Checking that title is set
	@[ "$(TITLE)" != "" ] || (echo Please set the title with \`making thate TITLE=...\`; false)
	# Checking that version is set and valid
	@echo "$(VERSION)" | grep '^[0-9]\+\.[0-9]\+\(\.[0-9]\+\)\?$$' > /dev/null || (echo Must pass version string as \`making thate VERSION=XX.YY[.ZZ]\`; false)
	# Checking that no changes need to be committed.
	@[ "$(shell git status --porcelain | wc -l)" = 0 ] || (echo Please commit all your changes first. ; false )
	./utils/bump-version.sh "$(VERSION)"
	make build-readme
	git commit -am "Bump version to $(VERSION)" -m "$(TITLE)" || echo Version is bumped and README is up to date.
	git push
	gh release create --target main "v$(VERSION)" --title "v$(VERSION) $(TITLE)" $(SHELLSCRIPT)

install:
	cp ${SHELLSCRIPT} /usr/bin/
	./tests/test-install.sh /usr/bin

install-to-user:
	cp ${SHELLSCRIPT} $(HOME)/bin
	./tests/test-install.sh $(HOME)/bin

install-symlink-to-user:
	unlink "$(HOME)/bin/${SHELLSCRIPT}" || true
	ln -s "$(PWD)/${SHELLSCRIPT}" "$(HOME)/bin/${SHELLSCRIPT}"
	./tests/test-install.sh $(HOME)/bin

uninstall:
	echo Remove the file ${SHELLSCRIPT} from your PATH

check:
	shellcheck ${ALL_SHELLSCRIPTS}

line-count:
	cloc ${SHELLSCRIPT}
	cloc ${TEST_SHELLSCRIPTS}
