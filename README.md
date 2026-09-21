# RoboCam Field Manual

🔗 **Read it online → <https://jlivingstonsg.github.io/proghouse2/>**

A bilingual (English / Swedish) reference for the **RoboCam** Android app — first-person
control of LEGO Mindstorms EV3, LEGO SPIKE Prime and Arduino / Raspberry Pi / PC robots
from a phone camera and any browser.

- **Part I** — the original RoboCam by Alexey (ПрогХаус), compiled and translated from the
  tutorials at <http://proghouse.ru/tags/robocam>.
- **Part II** — *RoboCam54*, an independent private build by M.Sc. Magnus that adds LEGO
  SPIKE Prime, a Huawei 360° USB camera with a pan/tilt viewer, a Google Cardboard VR
  viewer and a Clear Cache button. Documented here with the original author's consent;
  its source code is not released.

## Development

Most pages are generated from data in `tools/` — see [`tools/README.md`](tools/README.md) for
how to change a translation or a screenshot. `make check` runs the consistency checks that
GitHub Actions also runs on every push.

## Hosting

The site is served by GitHub Pages from the `main` branch (root folder). It is plain static
files with no build step on GitHub's side: generate locally (see Development), commit the
results and push; Pages redeploys within a minute.

## Pages

- `index.html` — the full bilingual field manual (built from `robocam.html` by `build-index.sh`).
- `hub-en.html` / `hub-sv.html` — standalone English and Swedish translations of the
  ProgHouse RoboCam hub page (<http://proghouse.ru/tags/robocam>): where to get the app plus
  the five original tutorials.
- `v1-0-*.html`, `v1-1-*.html`, `v1-2-*.html`, `v1-3-1-*.html`, `v1-4-2-*.html`
  (`-en` / `-sv`) — full translated copies of the five tutorials, one per RoboCam version
  (1.0, 1.1, 1.2, 1.3.1, 1.4.2). Screenshots are self-hosted: `img/en/` and `img/sv/` hold
  retouched copies with the interface text translated into English and Swedish; images that
  contain no Russian text (photos, 3D renders) are shared from `img/`.
- `files/` — the author's downloads referenced by the tutorials, hosted here: the two RoboCam
  APKs (release 1.4.5: regular and RenderScript), the EV3 Explorer build guide (PDF), the
  ready-made RoboCam settings (XML), the Selenokhod EV3 helper program, the Arduino Explorer
  sketch and the two 3D-printable holder parts (STL).

Every page links to the original hub (`proghouse.ru/tags/robocam`) exactly once, in its
footer; all other links between these pages stay on this site.

Unofficial reference, not affiliated with ПрогХаус.
