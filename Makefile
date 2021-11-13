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
	# Check version and title are set and valid
	@[ "$(TITLE)" != "" ] || (echo Please set the title with \`make TITLE=...\`; false)
	@echo "$(VERSION)" | grep '^[0-9]\+\.[0-9]\+\(\.[0-9]\+\)\?$$' || (echo Must pass version string as \`make VERSION=XX.YY[.ZZ]\`; false)
	./utils/bump-version.sh "$(VERSION)"
	make build-readme
	@[ "$(git status --porcelain | wc -l)" = 0 ] || (echo Please commit all your changes first. ; false )
	git commit -m "Bump version to $(VERSION)" -m "$(TITLE)"
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
