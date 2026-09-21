#!/usr/bin/env python3
"""One-time importer for the five Russian RoboCam tutorials on proghouse.ru.

For each article it downloads the page, cuts out the article body and splits it into
  * a *template*  - the original HTML with every translatable text run replaced by {{n}}
  * *segments*    - the Russian text runs themselves (inline tags kept; image alt texts
                    are prefixed with "ALT:")
and writes data/articles/<slug>.seg.json.  gen_articles.py then fills the template with the
translations in data/translations/<slug>.txt.

The committed .seg.json files are the result of running this once; you only need to run it
again if the originals change.  Usage:  python tools/import_articles.py [OUT_DIR]
"""
import html, json, pathlib, re, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SLUGS = ["92-robocam", "97-robocam-settings", "102-robocam-keyboard",
         "128-robocam-arduino", "131-robocam-local-controls"]
BASE = "http://proghouse.ru/article-box/"

CYR = re.compile(r"[А-Яа-яЁё]")
BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "ul", "ol", "td", "th", "tr", "table", "tbody",
         "thead", "div", "center", "pre", "iframe", "script", "img", "hr", "blockquote"}


def fetch(slug):
    req = urllib.request.Request(BASE + slug, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="replace")
    return raw.replace("\r\n", "\n")


def article_core(page):
    """The article body: from the first paragraph after the rating widget up to the tag list."""
    a = page.find("<p", page.find("content_rating"))
    while "unseen" in page[a:a + 40]:
        a = page.find("<p", a + 5)
    ends = [x for x in (page.find('class="pager', a), page.find('<ul class="pager', a),
                        page.find('<div id="comments"', a), page.find("jcomments=new", a)) if x > 0]
    body = page[a:min(ends)]
    body = body[:body.find('<p class="taxonomy">')]
    return body.rstrip().removesuffix("</div>").rstrip()


def segment(s):
    """Split HTML into (template, segments)."""
    toks = re.split(r"(<[^>]+>)", s)
    tmpl, segs, buf = [], [], []
    inpre = inscript = False

    def flush():
        nonlocal buf
        if not buf:
            return
        inner, buf = "".join(buf), []
        if CYR.search(re.sub(r"<[^>]+>", "", inner)):
            segs.append(re.sub(r"\s+", " ", inner).strip())
            tmpl.append("{{%d}}" % (len(segs) - 1))
        else:
            tmpl.append(inner)

    for t in toks:
        if not t:
            continue
        if t.startswith("<"):
            m = re.match(r"</?\s*([a-zA-Z0-9]+)", t)
            name = m.group(1).lower() if m else ""
            closing = t.startswith("</")
            if inpre:
                tmpl.append(t)
                inpre = not (closing and name == "pre")
                continue
            if inscript:
                tmpl.append(t)
                inscript = not (closing and name == "script")
                continue
            if name == "pre" and not closing:
                flush(); tmpl.append(t); inpre = True; continue
            if name == "script" and not closing:
                flush(); tmpl.append(t); inscript = True; continue
            if name == "img":
                flush()
                am = re.search(r'alt="([^"]*)"', t)
                if am and CYR.search(am.group(1)):
                    segs.append("ALT:" + html.unescape(am.group(1)))
                    t = t.replace(am.group(0), 'alt="{{%d}}"' % (len(segs) - 1))
                tmpl.append(t)
                continue
            if name in BLOCK:
                flush(); tmpl.append(t)
            else:
                buf.append(t)
        else:
            (tmpl if inpre or inscript else buf).append(t)
    flush()
    return "".join(tmpl), segs


def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "data" / "articles"
    out.mkdir(parents=True, exist_ok=True)
    for slug in SLUGS:
        template, segments = segment(article_core(fetch(slug)))
        with open(out / f"{slug}.seg.json", "w", encoding="utf-8") as f:
            json.dump({"template": template, "segments": segments}, f, ensure_ascii=False, indent=0)
        print(f"{slug}: {len(segments)} segments")


if __name__ == "__main__":
    main()
