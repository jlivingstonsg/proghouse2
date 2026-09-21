import html, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent   # repository root
STEM = {"131-robocam-local-controls":"v1-4-2","128-robocam-arduino":"v1-3-1","102-robocam-keyboard":"v1-2","97-robocam-settings":"v1-1","92-robocam":"v1-0"}
PLAY = "https://play.google.com/store/apps/details?id=ru.proghouse.robocam"
APKP = "https://apkpure.com/robocam/ru.proghouse.robocam"
HUB  = "http://proghouse.ru/tags/robocam"

# (slug, version, ru title, {lang: (title, summary)})
ARTICLES = [
 ("131-robocam-local-controls", "v1.4.2",
  "Превращаем смартфон в пульт управления роботом с приложением RoboCam",
  {"en": ("Turning a smartphone into a robot remote control with RoboCam",
          "In all the earlier RoboCam articles I described how to use it to control a robot in first person. But sometimes first-person control isn't needed &mdash; you only want to turn the smartphone into a remote control. The latest version of RoboCam adds exactly that."),
   "sv": ("Förvandla en smartphone till fjärrkontroll för roboten med RoboCam",
          "I alla tidigare artiklar om RoboCam beskrev jag hur man styr en robot i förstaperson. Men ibland behövs inte förstapersonsstyrning &mdash; man vill bara göra telefonen till en fjärrkontroll. Den senaste versionen av RoboCam har just den möjligheten.")}),
 ("128-robocam-arduino", "v1.3.1",
  "Делаем управление Arduino-роботом от первого лица",
  {"en": ("Building first-person control for an Arduino robot",
          "The latest version of RoboCam can control not only EV3 robots but also robots built on platforms such as Arduino, Raspberry Pi and similar, where you can work directly with the data received and sent over Bluetooth. Now you can process RoboCam's commands however you like."),
   "sv": ("Bygg förstapersonsstyrning för en Arduino-robot",
          "Den senaste versionen av RoboCam kan styra inte bara EV3-robotar utan även robotar byggda på plattformar som Arduino, Raspberry Pi och liknande, där man kan arbeta direkt med data som tas emot och skickas via Bluetooth. Nu kan du hantera RoboCams kommandon precis som du vill.")}),
 ("102-robocam-keyboard", "v1.2",
  "RoboCam – управляем роботом от первого лица с клавиатуры компьютера",
  {"en": ("RoboCam &ndash; controlling a robot in first person from a computer keyboard",
          "The new version of RoboCam adds support for a physical keyboard, so you can now control a LEGO Mindstorms EV3 robot in first person from a desktop computer or laptop. In this article I describe how to set up RoboCam to use the new feature, and what else is new in this version."),
   "sv": ("RoboCam &ndash; styr roboten i förstaperson med datorns tangentbord",
          "Den nya versionen av RoboCam har stöd för ett fysiskt tangentbord, så nu kan du styra en LEGO Mindstorms EV3-robot i förstaperson från en stationär dator eller bärbar dator. I den här artikeln beskriver jag hur du ställer in RoboCam för att använda den nya funktionen, och vad mer som är nytt i versionen.")}),
 ("97-robocam-settings", "v1.1",
  "Импорт, экспорт, копирование и отправка настроек роботов в приложении RoboCam",
  {"en": ("Importing, exporting, copying and sending robot settings in RoboCam",
          "The previous RoboCam article described how to control an EV3 robot in first person. But robots and mechanisms are built in many ways and each needs its own control layout. If you have developed a new robot, how do you share your settings with others, move them to another smartphone, or simply copy them? There is a solution: the new version of RoboCam adds import, export, copy and send of robot settings."),
   "sv": ("Importera, exportera, kopiera och skicka robotinställningar i RoboCam",
          "I den förra artikeln om RoboCam beskrevs hur man styr en EV3-robot i förstaperson. Men robotar och mekanismer kan se olika ut och var och en behöver sin egen styrning. Om du har utvecklat en ny robot uppstår frågan hur du delar dina inställningar med andra, för över dem till en annan telefon eller helt enkelt kopierar dem. Det finns en lösning: i den nya versionen av RoboCam har funktionerna import, export, kopiering och sändning av robotinställningar lagts till.")}),
 ("92-robocam", "v1.0",
  "Управление роботом LEGO Mindstorms EV3 от первого лица",
  {"en": ("Controlling a LEGO Mindstorms EV3 robot in first person",
          "A robot built from the LEGO Mindstorms EV3 kit is easy to control remotely in first person. For this you additionally need two smartphones, with the RoboCam app installed on one of them. Let's get to know RoboCam in more detail and learn how to use it."),
   "sv": ("Styr en LEGO Mindstorms EV3-robot i förstaperson",
          "En robot byggd av LEGO Mindstorms EV3-satsen kan enkelt fjärrstyras i förstaperson. Du behöver då två smartphones till, med appen RoboCam installerad på den ena. Låt oss lära känna RoboCam närmare och lära oss använda den.")}),
]

T = {
 "en": dict(
   lang="en", other="sv", other_file="hub-sv.html", other_label="Svenska", this_label="English",
   title="RoboCam articles from ProgHouse (English)",
   desc="English translation of the ProgHouse RoboCam hub: the app, downloads and the five original tutorials on controlling LEGO EV3 and Arduino robots in first person.",
   mark="Robo<b>Cam</b> · ProgHouse articles",
   kicker="Translated hub page · proghouse.ru/tags/robocam",
   h1="RoboCam articles from ProgHouse",
   intro=f'This page collects articles on using and configuring the Android app RoboCam, which lets you control LEGO Mindstorms EV3 robots in first person. You can install the app from <a href="{PLAY}">Google Play</a>, or download the APK and install it manually: the <a href="files/robocam-withoutrenderscript-release-1.4.5.apk" download>regular version of RoboCam</a> or the <a href="files/robocam-withrenderscript-release-1.4.5.apk" download>version that uses RenderScript</a> (for some older smartphones). There is also an <a href="{APKP}">APKPure</a> mirror.',
   dl_h="Get the app", dl_play="Google Play", dl_play_sub="Official listing",
   dl_std="Regular version", dl_std_sub="APK, release 1.4.5 &middot; hosted here",
   dl_rs="RenderScript version", dl_rs_sub="APK for some older smartphones &middot; hosted here",
   dl_apk="APKPure mirror", dl_apk_sub="Third-party mirror of the Play Store release",
   art_h="The tutorials", art_sub="Newest first, as on the original page. Each card links to a full translation; the Russian original title is shown for reference.",
   read="Read the translated article",
   manual_h="Want more than the summaries?",
   manual='The <a href="index.html">RoboCam Field Manual</a> is a full English/Swedish reference compiled and translated from these articles, with the app&rsquo;s screens, settings and protocol explained in detail.',
   foot='Translation of the public hub page <a href="'+HUB+'">proghouse.ru/tags/robocam</a> (ПрогХаус) by Alexey; RoboCam and the linked articles are the work of their author. Unofficial reference, not affiliated with ПрогХаус.',
   back="Field Manual", theme_l="Light", theme_d="Dark", lang_aria="Language", theme_aria="Theme"),
 "sv": dict(
   lang="sv", other="en", other_file="hub-en.html", other_label="English", this_label="Svenska",
   title="RoboCam-artiklar från ProgHouse (svenska)",
   desc="Svensk översättning av ProgHouses RoboCam-samlingssida: appen, nedladdningar och de fem originalhandledningarna om förstapersonsstyrning av LEGO EV3- och Arduino-robotar.",
   mark="Robo<b>Cam</b> · ProgHouse-artiklar",
   kicker="Översatt samlingssida · proghouse.ru/tags/robocam",
   h1="RoboCam-artiklar från ProgHouse",
   intro=f'Den här sidan samlar artiklar om hur man använder och ställer in Android-appen RoboCam, som låter dig styra LEGO Mindstorms EV3-robotar i förstaperson. Du kan installera appen från <a href="{PLAY}">Google Play</a>, eller ladda ner APK-filen och installera den manuellt: den <a href="files/robocam-withoutrenderscript-release-1.4.5.apk" download>vanliga versionen av RoboCam</a> eller <a href="files/robocam-withrenderscript-release-1.4.5.apk" download>versionen som använder RenderScript</a> (för vissa äldre telefoner). Det finns också en <a href="{APKP}">APKPure</a>-spegling.',
   dl_h="Skaffa appen", dl_play="Google Play", dl_play_sub="Officiell sida",
   dl_std="Vanlig version", dl_std_sub="APK, utgåva 1.4.5 &middot; finns här",
   dl_rs="RenderScript-version", dl_rs_sub="APK för vissa äldre telefoner &middot; finns här",
   dl_apk="APKPure-spegling", dl_apk_sub="Tredjepartsspegling av Play Store-utgåvan",
   art_h="Handledningarna", art_sub="Nyast först, som på originalsidan. Varje kort länkar till en fullständig översättning; originalets ryska rubrik visas som referens.",
   read="Läs den översatta artikeln",
   manual_h="Vill du ha mer än sammanfattningarna?",
   manual='<a href="index.html">RoboCam Field Manual</a> är en fullständig referens på engelska/svenska, sammanställd och översatt från dessa artiklar, med appens skärmar, inställningar och protokoll förklarade i detalj.',
   foot='Översättning av den offentliga samlingssidan <a href="'+HUB+'">proghouse.ru/tags/robocam</a> (ПрогХаус) av Alexej; RoboCam och de länkade artiklarna är upphovspersonens verk. Inofficiell referens, inte knuten till ПрогХаус.',
   back="Field Manual", theme_l="Ljust", theme_d="Mörkt", lang_aria="Språk", theme_aria="Tema"),
}

CSS = """
  :root{--ground:#f2f2ee;--surface:#ffffff;--surface-2:#faf9f5;--ink:#1b1d21;--ink-soft:#494c53;--ink-faint:#7b7e86;--border:#dcdcd4;--border-strong:#c3c3b9;--accent-line:#d84924;--accent-ink:#ad3a1c;--server:#2f9e6b;--connect:#8a4fc9;--shadow:0 1px 2px rgba(30,28,22,.05),0 8px 28px -18px rgba(30,28,22,.25)}
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#141619;--surface:#1c1f24;--surface-2:#21252b;--ink:#e9e8e3;--ink-soft:#b2b4ba;--ink-faint:#83868d;--border:#31353c;--border-strong:#434952;--accent-line:#ef6a41;--accent-ink:#f7936f;--server:#43b981;--connect:#ab7ae0;--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -18px rgba(0,0,0,.6)}}
  :root[data-theme="dark"]{--ground:#141619;--surface:#1c1f24;--surface-2:#21252b;--ink:#e9e8e3;--ink-soft:#b2b4ba;--ink-faint:#83868d;--border:#31353c;--border-strong:#434952;--accent-line:#ef6a41;--accent-ink:#f7936f;--server:#43b981;--connect:#ab7ae0;--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -18px rgba(0,0,0,.6)}
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--ground);color:var(--ink);font-family:"IBM Plex Sans","Segoe UI",Roboto,system-ui,sans-serif;font-size:16px;line-height:1.62;-webkit-font-smoothing:antialiased}
  a{color:var(--accent-ink)}
  .topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:10px clamp(16px,4vw,40px);background:color-mix(in srgb,var(--ground) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
  .topbar .mark{font-weight:600;letter-spacing:.06em;font-size:.82rem;text-transform:uppercase;color:var(--ink-soft)}
  .topbar .mark b{color:var(--accent-line)}
  .switches{display:flex;gap:8px;flex-wrap:wrap}
  .seg{display:inline-flex;border:1px solid var(--border-strong);border-radius:7px;overflow:hidden}
  .seg a,.seg button{font:inherit;font-size:.8rem;font-weight:500;padding:5px 11px;border:0;background:var(--surface);color:var(--ink-soft);cursor:pointer;line-height:1.2;text-decoration:none}
  .seg>*+*{border-left:1px solid var(--border)}
  .seg [aria-pressed="true"],.seg [aria-current="page"]{background:var(--ink);color:var(--ground)}
  #lt[aria-pressed="true"]{background:#e7a53a;color:#3a2905}
  #dk[aria-pressed="true"]{background:#4a48ab;color:#edecff}
  .seg a:focus-visible,.seg button:focus-visible{outline:2px solid var(--accent-line);outline-offset:-2px}
  main{max-width:860px;margin:0 auto;padding:34px clamp(16px,4vw,40px) 40px}
  .kicker{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent-ink);margin:0 0 14px}
  h1{font-size:clamp(2rem,5vw,2.9rem);line-height:1.06;margin:0 0 18px;font-weight:700;letter-spacing:-.02em;text-wrap:balance}
  h2{font-size:1.35rem;margin:38px 0 6px;letter-spacing:-.01em}
  .lead{font-size:1.08rem;color:var(--ink-soft);max-width:66ch;margin:0}
  .sub{color:var(--ink-faint);font-size:.92rem;margin:0 0 16px}
  .dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:22px 0 0}
  .dl a{display:block;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;box-shadow:var(--shadow)}
  .dl a:hover{border-color:var(--accent-line)}
  .dl b{display:block;font-weight:600}
  .dl span{display:block;font-size:.82rem;color:var(--ink-faint);margin-top:2px}
  .dl a.play b{color:var(--server)}
  .cards{display:grid;gap:12px;margin:0;padding:0;list-style:none}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
  .card h3{font-size:1.06rem;line-height:1.3;margin:0 0 6px;font-weight:600}
  .card p{margin:0 0 10px;color:var(--ink-soft);font-size:.96rem}
  .card .meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:.85rem}
  .ver{font-family:"IBM Plex Mono",monospace;font-size:.74rem;padding:1px 8px;border-radius:999px;border:1px solid var(--connect);color:var(--connect);background:color-mix(in srgb,var(--connect) 12%,transparent)}
  .ru{color:var(--ink-faint);font-style:italic}
  .note{border:1px solid var(--border);border-left:3px solid var(--accent-line);background:var(--surface-2);border-radius:8px;padding:14px 16px;margin:34px 0 0;font-size:.95rem}
  footer{max-width:860px;margin:0 auto;padding:24px clamp(16px,4vw,40px) 60px;border-top:1px solid var(--border);color:var(--ink-faint);font-size:.85rem}
  footer a{color:var(--ink-soft)}
  :focus-visible{outline:2px solid var(--accent-line);outline-offset:2px;border-radius:3px}
"""

JS = """
(function(){
  var root=document.documentElement,TKEY="robocam-theme",LKEY="robocam-lang";
  function setTheme(t){
    if(t==="light"||t==="dark"){root.setAttribute("data-theme",t);}
    else{root.removeAttribute("data-theme");t="system";}
    document.getElementById("lt").setAttribute("aria-pressed",String(t==="light"));
    document.getElementById("dk").setAttribute("aria-pressed",String(t==="dark"));
    try{localStorage.setItem(TKEY,t);}catch(e){}
  }
  var t="system";try{t=localStorage.getItem(TKEY)||"system";}catch(e){}
  setTheme(t);
  document.getElementById("lt").onclick=function(){setTheme(root.getAttribute("data-theme")==="light"?"system":"light");};
  document.getElementById("dk").onclick=function(){setTheme(root.getAttribute("data-theme")==="dark"?"system":"dark");};
  // keep the main manual's language in step with the page the reader picked
  try{localStorage.setItem(LKEY,root.getAttribute("lang"));}catch(e){}
})();
"""

def page(c):
    cards = "\n".join(
      f'''      <li class="card">
        <h3>{a[3][c["lang"]][0]}</h3>
        <p>{a[3][c["lang"]][1]}</p>
        <div class="meta"><span class="ver">{a[1]}</span><a href="{STEM[a[0]]}-{c["lang"]}.html">{c["read"]}</a> <span class="ru" lang="ru">{html.escape(a[2])}</span></div>
      </li>''' for a in ARTICLES)
    return f'''<!DOCTYPE html>
<html lang="{c["lang"]}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{c["desc"]}">
<title>{c["title"]}</title>
<link rel="alternate" hreflang="{c["other"]}" href="{c["other_file"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style>

<div class="topbar">
  <span class="mark">{c["mark"]}</span>
  <div class="switches">
    <div class="seg" role="group" aria-label="{c["lang_aria"]}">
      <a href="hub-en.html" hreflang="en" lang="en"{' aria-current="page"' if c["lang"]=="en" else ''}>English</a>
      <a href="hub-sv.html" hreflang="sv" lang="sv"{' aria-current="page"' if c["lang"]=="sv" else ''}>Svenska</a>
    </div>
    <div class="seg" role="group" aria-label="{c["theme_aria"]}">
      <button id="lt" aria-pressed="false">{c["theme_l"]}</button>
      <button id="dk" aria-pressed="false">{c["theme_d"]}</button>
    </div>
  </div>
</div>

<main>
  <p class="kicker">{c["kicker"]}</p>
  <h1>{c["h1"]}</h1>
  <p class="lead">{c["intro"]}</p>

  <h2>{c["dl_h"]}</h2>
  <div class="dl">
    <a class="play" href="{PLAY}"><b>{c["dl_play"]}</b><span>{c["dl_play_sub"]}</span></a>
    <a href="files/robocam-withoutrenderscript-release-1.4.5.apk" download><b>{c["dl_std"]}</b><span>{c["dl_std_sub"]}</span></a>
    <a href="files/robocam-withrenderscript-release-1.4.5.apk" download><b>{c["dl_rs"]}</b><span>{c["dl_rs_sub"]}</span></a>
    <a href="{APKP}"><b>{c["dl_apk"]}</b><span>{c["dl_apk_sub"]}</span></a>
  </div>

  <h2>{c["art_h"]}</h2>
  <p class="sub">{c["art_sub"]}</p>
  <ul class="cards">
{cards}
  </ul>

  <div class="note">
    <strong>{c["manual_h"]}</strong> {c["manual"]}
  </div>
</main>

<footer>
  <p>{c["foot"]} &middot; <a href="index.html">{c["back"]}</a> &middot; <a href="{c["other_file"]}" hreflang="{c["other"]}">{c["other_label"]}</a></p>
</footer>

<script>{JS}</script>
</html>
'''

if __name__=="__main__":
  for k in ("en","sv"):
    p = OUT / f"hub-{k}.html"
    p.write_text(page(T[k]), encoding="utf-8")
    print(p, p.stat().st_size)
