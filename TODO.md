# TODO

Open items for the RoboCam site. Tick them off (or delete them) as they get done.

## Waiting on a decision from Magnus

- [ ] **"National master" wording** on the About pages: keep "national master of 3D Tetris since 1989",
      or change to "Swedish champion in 3D Tetris since 1989" ("svensk mästare")?
- [ ] **Swedish degree title**: the Swedish text uses "teknologie magister Magnus Ivarsson", but an LTH
      engineering physics degree is normally "civilingenjör". Switch to "civilingenjör Magnus Ivarsson"?
- [ ] **Contact email** on the About pages: add one or not? (Not added; don't add without asking.)
- [ ] **GitHub card** on the About pages links to github.com/jlivingstonsg — confirm it should stay.
- [ ] **Setup video on the About pages too?** Alexey's setup video (KQgNk-JWrVY) is only in the manual's
      "See it in action" box; it was left off the About pages because it is Alexey's, not Magnus's.

## Content to add when the information is available

- [ ] **"Tap robot" picture** from github.com/jlivingstonsg/RoboCam54 (probably private) — Magnus wants it on
      the site (2026-10-29). Blocked: this Codespace's GitHub token can only see proghouse2, so the repo
      returns 404. Needs Magnus to upload the picture into the Codespace (e.g. drag into `img/`) or give
      access. Still to decide: which page and where (probably Part II of the manual).
- [ ] Add the **public Google Play release date** of RoboCam Pro to the development timeline in
      `robocam.html` (Part II). Only the closed-test dates (2026-09-19 – 09-20) are listed now.
- [ ] Optionally add "formerly RoboCam54" once in Part II, so the package id `com.robocam.robocam54`
      makes sense to readers.
- [ ] Update the **BlockOut II rank** on the About pages when it changes (MagI was rank 15,
      score 141,045, checked 2026-10-29).

## Housekeeping

- [ ] Add a `.gitignore` with `__pycache__/` (running `make check` leaves `tools/__pycache__/` untracked).
