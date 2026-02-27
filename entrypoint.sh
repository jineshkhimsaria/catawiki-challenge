#!/bin/bash
set -e

PYTEST_ARGS="tests/ -v -s --browser=${BROWSER:-chrome} --html=reports/report.html --self-contained-html"

if [ -n "$TAGS" ]; then
    PYTEST_ARGS="$PYTEST_ARGS -m \"$TAGS\""
fi

echo "============================================"
echo "  Catawiki Selenium Test Suite"
echo "============================================"
echo "  Browser:  ${BROWSER:-chrome}"
echo "  Base URL: ${BASE_URL:-https://www.catawiki.com}"
echo "  Tags:     ${TAGS:-all}"
echo "============================================"

eval pytest $PYTEST_ARGS
