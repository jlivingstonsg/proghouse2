# Build tooling

Everything under the repository root that is *generated* is produced from data in `tools/data`.
Edit the data (or the generator), re-run it, commit both. Do not hand-edit generated files —
`check_site.py` will fail if you do.

| Generated file(s) | Made by | From |
|---|---|---|
| `index.html` | `build-index.sh` | `robocam.html` (hand-written, bilingual manual) |
| `hub-en.html`, `hub-sv.html` | `tools/gen_hub.py` | strings inside the script |
| `v1-*-en.html`, `v1-*-sv.html` | `tools/gen_articles.py` | `data/articles/*.seg.json` + `data/translations/*.txt` |
| `img/en/**`, `img/sv/**` | `tools/build_items.py` + `tools/render_all.py` | `tools/gloss.py`, `tools/extras.py`, `data/ocr/*.json`, originals in `img/` |

`make pages`, `make index`, `make images` and `make check` from the repository root run these.

## Changing a translation

1. Edit `data/translations/<article>.txt`. Each entry is `@n` followed by `en:` and `sv:` lines;
   `n` is the segment number in `data/articles/<article>.seg.json`.
2. `make pages` — regenerates the ten `v1-*` pages.
3. `make check`, then commit.

## Changing text inside a screenshot

The pictures are repainted from the originals in `img/articles/`: the Russian text is painted
over with the surrounding background and the translation is drawn in Roboto at the same size.

* `gloss.py` — Russian UI string → (English, Swedish). One entry fixes every screenshot that
  shows the string, and keeps the pictures consistent with the article text.
* `extras.py` — hand-placed items for things detection cannot do (wrapped file names, the two
  diagrams, toasts): explicit pixel box + text.
* Then `make images` (about 15 seconds) rewrites `img/en/` and `img/sv/`.

`python tools/review_sheets.py` writes side-by-side contact sheets (EN above SV) to a temp folder
so you can look at the result; `python tools/check_untranslated.py en` OCRs the output and lists
any Russian left (expect a few false positives: OCR reads English words as Cyrillic).

Requirements for the image pipeline: `pip install -r tools/requirements.txt`. Tesseract with the
Russian model (`apt install tesseract-ocr tesseract-ocr-rus`) is only needed to *re-detect* text
(`segs.py`, `ocr_lines.py`); the detection results are committed in `data/ocr/`, so rendering
needs no OCR. If you add or replace an original screenshot, add it to `data/imgindex.json`, run
`segs.py <index>` and `ocr_lines.py`, then `build_items.py` and check what is left unmatched.

## Provenance

`data/articles/*.seg.json` come from `import_articles.py`, which downloads the five Russian
tutorials from proghouse.ru and splits them into an HTML template plus the Russian text runs.
Re-running it reproduces the committed files except for live details such as download counters.
The tutorials, screenshots and downloads are the work of their author (ПрогХаус); see the
footer of every page. `data/fonts` holds Roboto (Apache License 2.0), used to draw the
translated text in screenshots.
