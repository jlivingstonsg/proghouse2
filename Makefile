# Common tasks. See tools/README.md.
PY ?= python3

.PHONY: pages index images check all
all: pages index check

pages:   ## regenerate hub-*.html and v1-*.html
	$(PY) tools/gen_hub.py
	$(PY) tools/gen_articles.py

index:   ## rebuild index.html from robocam.html
	bash build-index.sh

images:  ## repaint the translated screenshots (needs tools/requirements.txt)
	$(PY) tools/build_items.py
	$(PY) tools/render_all.py

check:   ## consistency checks (also run by GitHub Actions)
	$(PY) tools/check_site.py
