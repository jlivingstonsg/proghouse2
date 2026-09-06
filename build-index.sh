#!/usr/bin/env bash
# Wrap the Artifact-authored robocam.html into a standalone page for GitHub Pages.
set -euo pipefail
cd "$(dirname "$0")"
{
  echo '<!DOCTYPE html>'
  echo '<html lang="en">'
  echo '<meta charset="utf-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1">'
  echo '<meta name="description" content="Bilingual EN/SV field manual for the RoboCam Android app — first-person control of LEGO EV3, SPIKE Prime and Arduino robots.">'
  cat robocam.html
  echo '</html>'
} > index.html
echo "index.html rebuilt ($(wc -c < index.html) bytes)"
