#!/bin/bash
# Generate resume PDF from HTML using Chrome headless

CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
DIR="$(cd "$(dirname "$0")" && pwd)"

INPUT="$DIR/igor-geyn-data-scientist-resume.html"
OUTPUT="$DIR/Igor-Geyn-Data-Scientist-Resume.pdf"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$OUTPUT" --no-margins "file:///$INPUT"

echo "Generated: $OUTPUT"
