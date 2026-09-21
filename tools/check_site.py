#!/usr/bin/env python3
"""Consistency checks for the RoboCam site.  Standard library only - run from anywhere:

    python tools/check_site.py

Exit status is 0 when everything passes, 1 otherwise.  Checks:
  1. every local href/src points at a file that exists
  2. link policy: each page links to the original hub (proghouse.ru/tags/robocam) exactly once
     (index.html: once per language) and to no other proghouse.ru page
  3. index.html is exactly what build-index.sh makes from robocam.html
  4. hub-*.html and v1-*.html are exactly what tools/gen_hub.py and tools/gen_articles.py make
     from the data in tools/data (i.e. nobody hand-edited generated pages)
  5. HTML tags are balanced
  6. translated pages contain no leftover Russian text (apart from names and quoted Russian titles)
  7. every file in files/ is linked from some page; language attributes are right
"""
import pathlib, re, shutil, subprocess, sys, tempfile
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
HUB = "http://proghouse.ru/tags/robocam"
CYR = re.compile(r"[А-Яа-яЁё]")
failures = []


def fail(check, msg):
    failures.append(f"[{check}] {msg}")


def pages():
    return sorted(p for p in ROOT.glob("*.html") if p.name != "robocam.html")


def gen_pages():
    return sorted(list(ROOT.glob("hub-*.html")) + list(ROOT.glob("v1-*.html")))


# ---- 1 + 2: links -----------------------------------------------------------------------
def check_links():
    referenced_files = set()
    for page in pages():
        s = page.read_text(encoding="utf-8")
        for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
            u = m.group(1)
            if u.startswith(("#", "mailto:", "data:", "javascript:")):
                continue
            if re.match(r"(https?:)?//", u):
                host = urlparse(u if u.startswith("http") else "http:" + u).hostname or ""
                if host in ("proghouse.ru", "www.proghouse.ru") and u.rstrip("/") != HUB:
                    fail("links", f"{page.name}: forbidden proghouse.ru link {u}")
                continue
            target = (ROOT / u.split("#")[0].split("?")[0])
            if not target.exists():
                fail("links", f"{page.name}: missing local target {u}")
            elif u.startswith("files/"):
                referenced_files.add(target.name)
        n = s.count(f'href="{HUB}"')
        want = 2 if page.name == "index.html" else 1
        if n != want:
            fail("links", f"{page.name}: {n} link(s) to {HUB}, expected {want}")
    for f in sorted((ROOT / "files").iterdir()):
        if f.name not in referenced_files:
            fail("files", f"files/{f.name} is not linked from any page")


# ---- 3: index.html ------------------------------------------------------------------------
def check_index():
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(ROOT / "robocam.html", tmp)
        shutil.copy(ROOT / "build-index.sh", tmp)
        subprocess.run(["bash", str(pathlib.Path(tmp) / "build-index.sh")], check=True,
                       capture_output=True)
        if (pathlib.Path(tmp) / "index.html").read_bytes() != (ROOT / "index.html").read_bytes():
            fail("index", "index.html is out of date - run: bash build-index.sh")


# ---- 4: generated pages -------------------------------------------------------------------
def check_generated():
    before = {p: p.read_bytes() for p in gen_pages()}
    try:
        for script in ("gen_hub.py", "gen_articles.py"):
            r = subprocess.run([sys.executable, str(ROOT / "tools" / script)], capture_output=True, text=True)
            if r.returncode:
                fail("generated", f"{script} failed: {r.stderr.strip()[-300:]}")
                return
        for p, old in before.items():
            if p.read_bytes() != old:
                fail("generated", f"{p.name} differs from the generator output - "
                                  "edit tools/ data instead of the page, then re-run the generators")
    finally:
        for p, old in before.items():      # leave the working tree as we found it
            p.write_bytes(old)


# ---- 5: balanced HTML ---------------------------------------------------------------------
class Balance(HTMLParser):
    VOID = {"meta", "link", "br", "img", "hr", "input", "source", "area", "base", "col", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed <{self.stack.pop()}>")
            self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}>")


def check_html():
    for page in pages():
        p = Balance()
        p.feed(page.read_text(encoding="utf-8"))
        # <html> is closed by the page; anything else left open is an error
        left = [t for t in p.stack if t != "html"]
        if p.errors or left:
            fail("html", f"{page.name}: {(p.errors + ['unclosed <%s>' % t for t in left])[:3]}")


# ---- 6 + 7: language ----------------------------------------------------------------------
def check_language():
    for page in gen_pages():
        s = page.read_text(encoding="utf-8")
        lang = "sv" if page.stem.endswith("-sv") else "en"
        if f'<html lang="{lang}">' not in s:
            fail("lang", f'{page.name}: expected <html lang="{lang}">')
        text = re.sub(r'<span class="ru" lang="ru">.*?</span>', "", s, flags=re.S)   # quoted Russian titles
        text = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = text.replace("ПрогХаус", "")
        bad = sorted(set(re.findall(r"[^\s]*[А-Яа-яЁё]+[^\s]*", text)))
        if bad:
            fail("lang", f"{page.name}: untranslated Russian text: {bad[:5]}")
        other = "sv" if lang == "en" else "en"
        for m in re.finditer(r'src="img/(en|sv)/', s):
            if m.group(1) != lang:
                fail("lang", f"{page.name}: uses an image for the wrong language (img/{m.group(1)}/)")
                break
        if f'hreflang="{other}"' not in s:
            fail("lang", f"{page.name}: missing hreflang link to the {other} version")


def main():
    for name, fn in (("links", check_links), ("index", check_index), ("generated", check_generated),
                     ("html", check_html), ("language", check_language)):
        before = len(failures)
        fn()
        print(f"{'ok  ' if len(failures) == before else 'FAIL'}  {name}")
    print()
    if failures:
        print(f"{len(failures)} problem(s):")
        for f in failures:
            print("  -", f)
        return 1
    print(f"all checks passed ({len(pages())} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
