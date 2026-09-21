import re, json, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen_hub as H

DATA = pathlib.Path(__file__).resolve().parent / "data"
OUT = DATA.parent.parent   # repository root

# (source slug, version label, file stem, ISO date, "Alex" byline)
ARTS = [
 ("92-robocam",                 "1.0",   "v1-0",   "2016-09-21"),
 ("97-robocam-settings",        "1.1",   "v1-1",   "2016-10-22"),
 ("102-robocam-keyboard",       "1.2",   "v1-2",   "2016-12-19"),
 ("128-robocam-arduino",        "1.3.1", "v1-3-1", "2017-10-06"),
 ("131-robocam-local-controls", "1.4.2", "v1-4-2", "2017-11-07"),
]
STEM = {a[0]: a[2] for a in ARTS}
FILES = {82: "robocam-withoutrenderscript-release-1.4.5.apk", 81: "robocam-withrenderscript-release-1.4.5.apk",
         56: "researcher.pdf", 59: "robocam_racing_car_std.xml", 60: "robocam_racing_car_high_speed_version.xml",
         61: "robocam_clawbot.xml", 62: "robocam_selenokhod.xml", 63: "selenokhodfpv.ev3",
         68: "researcher.ino", 69: "robocam_arduino.xml", 70: "dfrobot-servoholder.stl", 71: "dfrobot-beam.stl"}
MONTHS = {"en": ["January","February","March","April","May","June","July","August","September","October","November","December"],
          "sv": ["januari","februari","mars","april","maj","juni","juli","augusti","september","oktober","november","december"]}
def fdate(iso, lang):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[lang][int(m)-1]} {y}" if lang == "sv" else f"{MONTHS[lang][int(m)-1]} {int(d)}, {y}" if False else f"{int(d)} {MONTHS[lang][int(m)-1]} {y}"

UI = {
 "en": dict(kicker="Version {v} · translated article", byline="Translated from the Russian original by Alexey (ПрогХаус), published {d}.",
            shots="The screenshots are from the original article, retouched so that the interface text is in English. The untouched originals show the Russian interface.",
            lbl_date="Date", lbl_size="File size",
            all_h="All RoboCam versions", hub="All articles (hub)", manual="Field Manual", this_page="you are here",
            foot='Translation of an article by Alexey (ПрогХаус); RoboCam, its screenshots and downloads are the work of their author. The original tutorials are collected at <a href="http://proghouse.ru/tags/robocam">proghouse.ru/tags/robocam</a>. Unofficial reference, not affiliated with ПрогХаус.',
            title="RoboCam {v} &ndash; {t}"),
 "sv": dict(kicker="Version {v} · översatt artikel", byline="Översatt från den ryska originalartikeln av Alexej (ПрогХаус), publicerad {d}.",
            shots="Skärmbilderna är från originalartikeln och har retuscherats så att gränssnittstexten är på svenska. De orörda originalen visar det ryska gränssnittet.",
            lbl_date="Datum", lbl_size="Filstorlek",
            all_h="Alla RoboCam-versioner", hub="Alla artiklar (samlingssida)", manual="Field Manual", this_page="du är här",
            foot='Översättning av en artikel av Alexej (ПрогХаус); RoboCam, dess skärmbilder och nedladdningar är upphovspersonens verk. De ursprungliga handledningarna finns samlade på <a href="http://proghouse.ru/tags/robocam">proghouse.ru/tags/robocam</a>. Inofficiell referens, inte knuten till ПрогХаус.',
            title="RoboCam {v} &ndash; {t}"),
}

EXTRA_CSS = """
  .article{margin-top:22px}
  .article p{margin:0 0 14px}
  .article img{max-width:100%;height:auto;border-radius:4px}
  .article p>img{display:block;margin:6px auto}
  .article h3{font-size:1.2rem;margin:30px 0 8px;letter-spacing:-.01em}
  .article ul,.article ol{padding-left:1.3em;margin:0 0 14px}
  .article li{margin:3px 0}
  .article iframe{max-width:100%}
  .article pre{overflow:auto;background:var(--surface)!important;color:var(--ink);border-radius:8px;padding:12px 14px;font-size:.85rem;line-height:1.5!important}
  .article table{max-width:100%;border-collapse:collapse}
  .article table[style]{background:var(--surface-2)!important;border-color:var(--border)!important}
  .article td,.article th{padding:6px 8px;vertical-align:top}
  .article table.data td,.article table.data th{border:1px solid var(--border)}
  .article center{display:block}
  .byline{color:var(--ink-faint);font-size:.92rem;margin:0 0 8px}
  .shots{font-size:.88rem;color:var(--ink-faint);border-left:3px solid var(--border-strong);padding:2px 0 2px 12px;margin:14px 0 0}
  .versions{list-style:none;padding:0;margin:8px 0 0;display:grid;gap:6px}
  .versions a{display:flex;gap:10px;align-items:baseline;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:8px 12px}
  .versions a:hover{border-color:var(--accent-line)}
  .versions a[aria-current="page"]{border-color:var(--accent-line);background:var(--surface-2)}
  .versions .ver{flex:none}
  .versions .here{margin-left:auto;font-size:.78rem;color:var(--ink-faint)}
"""

def parse_tr(path):
    d, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("@"):
            cur = int(line[1:]); d[cur] = {}
        elif line[:3] in ("en:", "sv:"):
            d[cur][line[:2]] = line[3:].strip()
        elif line.strip() and cur is not None:  # continuation
            raise SystemExit(f"stray line in {path.name} @{cur}: {line[:60]}")
    return d

def rewrite_links(s, lang):
    def fix(m):
        attrs, href, inner = m.group(1), m.group(2), m.group(3)
        if href.rstrip("/") == "/tags/robocam":
            return f'<a href="hub-{lang}.html">{inner}</a>'
        am = re.match(r"/article-box/([^/?#]+)", href)
        if am and am.group(1) in STEM:
            return f'<a href="{STEM[am.group(1)]}-{lang}.html">{inner}</a>'
        fm = re.match(r"/component/jdownloads/finish/[^/]+/(\d+)-", href)
        if fm and int(fm.group(1)) in FILES:
            return f'<a href="files/{FILES[int(fm.group(1))]}" download>{inner}</a>'
        if href.startswith("/") or "proghouse.ru" in href:
            return inner   # no clone exists for this target: keep the text, drop the link
        return m.group(0)
    return re.sub(r'<a\b([^>]*?)href="([^"]*)"[^>]*>(.*?)</a>', fix, s, flags=re.S)

IMGS = set()
def fix_imgs(s,lang):
    def one(m):
        tag = m.group(0)
        sm = re.search(r'src="([^"]*)"', tag)
        if not sm: return tag
        src = sm.group(1)
        if "jdownloads" in src: return ""          # decorative download-widget icons
        pm = re.match(r"(?:https?://(?:www\.)?proghouse\.ru)?/images/(.+)", src)
        if pm:
            IMGS.add(pm.group(1))
            local = f'img/{lang}/{pm.group(1)}' if (OUT / 'img' / lang / pm.group(1)).exists() else f'img/{pm.group(1)}'
            tag = tag.replace(sm.group(0), f'src="{local}" loading="lazy"')
        return tag
    return re.sub(r"<img\b[^>]*>", one, s)

def build(slug, ver, stem, iso, lang):
    seg = json.load(open(DATA / "articles" / f"{slug}.seg.json", encoding="utf-8"))
    tr = parse_tr(DATA / "translations" / f"{slug}.txt")
    missing = [i for i in range(len(seg["segments"])) if i not in tr or lang not in tr[i]]
    if missing: raise SystemExit(f"{slug}: missing {lang} for segments {missing[:10]}... ({len(missing)})")
    body = seg["template"]
    def sub(m):
        i = int(m.group(1)); t = tr[i][lang]
        return t.replace('"', "&quot;") if seg["segments"][i].startswith("ALT:") else t
    body = re.sub(r"\{\{(\d+)\}\}", sub, body)
    cf = DATA / "translations" / f"{slug}.comments.txt"
    if cf.exists():                       # translate Russian comments inside code blocks
        for line in cf.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            ru, rest = line.split(" => ", 1)
            en, sv = rest.split(" | ", 1)
            assert ru in body, f"comment not found: {ru}"
            body = body.replace(ru, en if lang == "en" else sv)
    body = re.sub(r"<script\b.*?</script>", "", body, flags=re.S)
    body = fix_imgs(rewrite_links(body, lang), lang)
    # file boxes end with "<date> <size> <download count>"; the count belongs to the original
    # site and is stale here, so keep only date and size, with labels
    u0 = UI[lang]
    body = re.sub(r"<small>\s*&nbsp;(\d{2}\.\d{2}\.\d{4})\s*&nbsp;([^&<]+?)\s*&nbsp;\d+</small>",
                  lambda m: f"<small>{u0['lbl_date']}: {m.group(1)} &middot; {u0['lbl_size']}: {m.group(2).strip()}</small>", body)
    title = next(a[3][lang][0] for a in H.ARTICLES if a[0] == slug)
    c = H.T[lang]; u = UI[lang]
    other = "sv" if lang == "en" else "en"
    versions = "\n".join(
        f'      <li><a href="{s2[2]}-{lang}.html"{" aria-current=\"page\"" if s2[0]==slug else ""}><span class="ver">v{s2[1]}</span> {next(a[3][lang][0] for a in H.ARTICLES if a[0]==s2[0])}{f"<span class=\"here\">{u[chr(116)+chr(104)+chr(105)+chr(115)+chr(95)+chr(112)+chr(97)+chr(103)+chr(101)]}</span>" if s2[0]==slug else ""}</a></li>'
        for s2 in reversed(ARTS))
    mark = c["mark"]
    page = f'''<!DOCTYPE html>
<html lang="{lang}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(re.sub('<[^>]+>','',html.unescape(u['byline'].format(d=fdate(iso,lang)))) + ' ' + re.sub('<[^>]+>','',title), quote=True)}">
<title>{re.sub('<[^>]+>','',u["title"].format(v=ver,t=title))}</title>
<link rel="alternate" hreflang="{other}" href="{stem}-{other}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{H.CSS}{EXTRA_CSS}</style>

<div class="topbar">
  <span class="mark">{mark}</span>
  <div class="switches">
    <div class="seg" role="group" aria-label="{c["lang_aria"]}">
      <a href="{stem}-en.html" hreflang="en" lang="en"{' aria-current="page"' if lang=="en" else ''}>English</a>
      <a href="{stem}-sv.html" hreflang="sv" lang="sv"{' aria-current="page"' if lang=="sv" else ''}>Svenska</a>
    </div>
    <div class="seg" role="group" aria-label="{c["theme_aria"]}">
      <button id="lt" aria-pressed="false">{c["theme_l"]}</button>
      <button id="dk" aria-pressed="false">{c["theme_d"]}</button>
    </div>
  </div>
</div>

<main>
  <p class="kicker">{u["kicker"].format(v=ver)}</p>
  <h1>{title}</h1>
  <p class="byline">{u["byline"].format(d=fdate(iso,lang))}</p>
  <p class="shots">{u["shots"]}</p>

  <div class="article">
{body}
  </div>

  <h2>{u["all_h"]}</h2>
  <ul class="versions">
{versions}
  </ul>
  <p class="sub" style="margin-top:14px"><a href="hub-{lang}.html">{u["hub"]}</a> &middot; <a href="index.html">{u["manual"]}</a></p>
</main>

<footer>
  <p>{u["foot"]}</p>
</footer>

<script>{H.JS}</script>
</html>
'''
    (OUT / f"{stem}-{lang}.html").write_text(page, encoding="utf-8")
    return len(page)

if __name__ == "__main__":
    only = sys.argv[1:] or [a[0] for a in ARTS]
    for slug, ver, stem, iso in ARTS:
        if slug not in only: continue
        for lang in ("en", "sv"):
            print(stem, lang, build(slug, ver, stem, iso, lang))
    print(len(IMGS), "images")
