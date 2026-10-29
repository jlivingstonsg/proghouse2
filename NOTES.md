# Notes

Working notes for the RoboCam site, so a new session can pick up where the last one stopped.
See `README.md` and `tools/README.md` for how the site is built.

## Who and what

- Owner: **M.Sc. Magnus Ivarsson** (Sweden). M.Sc. in Engineering Physics, Lund University (LTH).
  National master of 3D Tetris since 1989; on the BlockOut II world ranking as **MagI**; made the
  online BlockOut II port at https://blockout.nu/.
  Has a parachute (skydiving) licence and a hang gliding licence, and has had two wings (2026-10-29).
- From https://gamereality.se/ (Magnus's own site, read 2026-10-29): civilingenjör i teknisk fysik, LTH, graduated
  2005; main interests telerobotics and particle physics; founder of GameReality (remote-controlled camera robot
  game; Facebook page facebook.com/gamereality1); tutors maths/physics via Superprof; licensed in 2021 to use the
  BlockOut name (gamepuzzles.com); paintball tank driven from Australia 2005; IPSO Challenge 2014 nominee
  (Chicago); Draknästet TV8 6 Apr 2015 (all five investors, 2.5 MSEK); KDUW.biz radio with Sandy Carter (IBM)
  28 Apr 2016; Serendipity Challenge Visby June 2016; Creative Business Cup 2016; telerobotics for the
  "Ariel Fashion Shoot" project. His site still says BlockOut rank 28 — rank 15 is the newer figure.
- Magnus's vision (2026-10-29, now on the About pages under "My vision"): a game like Isotopium
  (https://www.patreon.com/isotopium/about) but with omni robots and 360° camera views; virtual game where
  gamers build robots and win tournaments → winners' robots built for real and put in his real arena; rent
  out owners' robots when idle and split the profit; people can buy/build their own robot for the arenas;
  robots big enough to hunt real people on paintball / laser-tag arenas, remote-controlled from other countries.
- Deliberately left OFF the About pages (private): his child, the LADOK/bullying note, the diploma document,
  the CV link. Isotopium is now linked only as the comparison in "My vision", at Magnus's request.
- The app formerly called **RoboCam54** is now **RoboCam Pro** on Google Play:
  https://play.google.com/store/apps/details?id=com.robocam.robocam54
  The package id `com.robocam.robocam54` cannot change — keep it as is.
- Live site: https://jlivingstonsg.github.io/proghouse2/ (GitHub Pages from `main`, root folder).

## Links used on the About pages

- LinkedIn: https://www.linkedin.com/in/m-sc-magnus-ivarsson/
- Facebook: https://www.facebook.com/magnus.ivarsson.5682
- YouTube: https://www.youtube.com/@GameReality
- RoboCam video playlist: https://www.youtube.com/watch?v=TZ4ujKcy87o&list=PLi0zyNfBMXA8SMBR8jWbhCJ7RWjkjBnN_
- BlockOut II: https://blockout.net/blockout2/ — world ranking:
  https://blockout.net/blockout2/worldranking/index.php?setupid=458
- Privacy policy: https://jlivingstonsg.github.io/robocam-privacy/
- GitHub: https://github.com/jlivingstonsg

## How Magnus likes changes done

1. Make the edit. Every page is bilingual — change English **and** Swedish.
2. Generated pages: `hub-*.html` come from `tools/gen_hub.py`, `v1-*.html` from `tools/gen_articles.py`
   (`make pages`). `index.html` comes from `robocam.html` (`./build-index.sh`). Never hand-edit those.
   `about-en.html` / `about-sv.html` are hand-written.
3. Run `make check` (must pass; every page must link to proghouse.ru/tags/robocam exactly once).
4. Show the change right away in the Codespace preview instead of waiting for GitHub Pages:
   `python3 -m http.server 8000` in the repo, then open
   `https://$CODESPACE_NAME-8000.$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN/<page>` with
   `timeout 20 "$BROWSER" <url>` (the browser helper can hang without the timeout).
5. Wait for "commit and push" before committing. Commit only the files that changed (not `tools/__pycache__`).
6. Keep `TODO.md` and this file updated **as we talk** (Magnus asked for this on 2026-10-29), and commit
   them together with the site change.

## Decisions and preferences

- The app is called **RoboCam Pro** on the site; "RoboCam54" is no longer used (package id stays).
- Name: "M.Sc. Magnus Ivarsson" in English; Swedish text still says "teknologie magister" (open, see TODO).
- So far the About pages link only to Magnus's own things and Alexey's video is only in the manual
  (Claude's default, not confirmed by Magnus — see TODO).
- Every page except the main page (`index.html`) has a Back button (top left); Magnus asked on 2026-10-29
  to remove it from the main page. Back right after switching EN/SV goes to the other language version
  (normal browser behaviour; Magnus has not asked to change it).
- "RoboCam" in the top bar scrolls to the top on every page, including the main page.
- The "tab robot picture" Magnus asked for is the **browser-tab icon**: `favicon.ico` (robot = phone between two
  tank tracks), taken from the RoboCam web client (`app/src/main/assets/web/def/favicon.ico` in the public repo
  jlivingstonsg/RoboCam_latest; github.com/jlivingstonsg/RoboCam54 is not reachable from the Codespace).

## History

- 2026-10-29: announced RoboCam Pro on Google Play; renamed RoboCam54 → RoboCam Pro everywhere;
  full name M.Sc. Magnus Ivarsson; new About pages (bio, LinkedIn, Facebook, YouTube, BlockOut II rank);
  video playlist box at the top of the manual; Back button top-left on every page; clicking "RoboCam"
  in the top bar scrolls to the top on every page; this TODO/NOTES/CLAUDE.md setup and auto-start of Claude.
- 2026-10-29: added Alexey's setup video (https://www.youtube.com/watch?v=KQgNk-JWrVY, in Russian) to the
  "See it in action" box at the top of the manual.
- 2026-10-29: Magnus asked that TODO.md / NOTES.md be updated continuously during sessions; CLAUDE.md now
  says so.
- 2026-10-29: removed the Back button from the main page (`robocam.html` / `index.html`) only.
- 2026-10-29: added the RoboCam robot `favicon.ico` as the browser-tab icon on every page (via build-index.sh,
  gen_hub.py, gen_articles.py and the About pages).
- 2026-10-29: About pages: added parachute and hang gliding licences and the two wings.
- 2026-10-29: About pages: added GameReality and telerobotics section (2005–2016 highlights), BlockOut
  licence, Superprof tutoring, and GameReality website + Facebook cards — all from gamereality.se.
- 2026-10-29: About pages: added "My vision" section (Isotopium-style game, omni robots, 360° views,
  virtual tournaments → real robots, rentals, bring-your-own, robots hunting players on paintball/laser-tag arenas).
