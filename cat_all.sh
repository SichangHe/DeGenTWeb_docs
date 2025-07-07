#!/usr/bin/env bash
for f in *.md; do
    if [ "$f" != "development.md" ]; then
        cat "$f"
    fi
done
