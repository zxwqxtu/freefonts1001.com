#!/usr/bin/env python3
"""
Daily wrapper for FreeFonts1001 story generator.
Runs the generator only if the most recent [date].html file is older than 3 days.
Otherwise exits silently.

This script is called daily by launchd, but only generates a new story
when 3 days have elapsed since the last one.
"""
import os
import sys
import glob
import time
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
GENERATOR_SCRIPT = os.path.join(SCRIPT_DIR, 'font_story_generator.py')

def get_most_recent_story_date():
    """Find the most recent YYYY-MM-DD.html file and return its date."""
    pattern = os.path.join(PROJECT_DIR, '????-??-??.html')
    files = glob.glob(pattern)
    if not files:
        return None
    # Extract dates from filenames and find the most recent
    dates = []
    for f in files:
        basename = os.path.basename(f)
        # Match YYYY-MM-DD.html
        import re
        m = re.match(r'(\d{4}-\d{2}-\d{2})\.html$', basename)
        if m:
            try:
                d = datetime.strptime(m.group(1), '%Y-%m-%d')
                dates.append((d, f))
            except ValueError:
                pass
    if not dates:
        return None
    dates.sort(key=lambda x: x[0], reverse=True)
    return dates[0][0]  # Return the most recent date

def main():
    now = datetime.now()
    last_date = get_most_recent_story_date()
    
    if last_date is None:
        # No previous story, run generator
        print(f"[WRAPPER] No previous story found, running generator...")
        run_generator()
        return
    
    days_since = (now.date() - last_date.date()).days
    print(f"[WRAPPER] Last story: {last_date.date()}, {days_since} days ago")
    
    if days_since >= 3:
        print(f"[WRAPPER] 3+ days elapsed, running generator...")
        run_generator()
    else:
        print(f"[WRAPPER] Only {days_since} days elapsed, skipping (next run in {3 - days_since} days)")

def run_generator():
    import subprocess
    result = subprocess.run(
        [sys.executable, GENERATOR_SCRIPT],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
