#!/usr/bin/env python3
"""Sync the engineering course's lectures from its deck repo (Marp slides, kept separately).

    python3 tools/sync_engineering.py                     # deck repo cloned next to this one, ../ros2-course
    python3 tools/sync_engineering.py PATH/TO/DECK_REPO

For every slides/lecture-*.md in the deck repo whose PDF exists: copies the PDF to
slides/engineering/ and rewrites the "engineering" course's "lectures" in courses.json from
the deck's cover — '# Lecture N — Title', '## subtitle', '**Topics:** …'. Nothing else in
courses.json changes (videos are added by hand) and nothing is deleted.
"""
import json
import re
import shutil
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SLUG = 'engineering'


def covers(decks, course_title):
    for md in sorted((decks / 'slides').glob('lecture-*.md')):
        pdf = md.with_suffix('.pdf')
        if not pdf.exists():
            continue
        text = re.sub(r'<!--.*?-->', '', md.read_text(), flags=re.S)
        title = re.search(r'^# (.+)$', text, re.M).group(1).strip()
        sub = re.search(r'^## (.+)$', text, re.M)
        topics = re.search(r'^\*\*Topics:\*\*\s*(.+)$', text, re.M)
        num, name = re.match(r'Lecture (\d+)\s*[—–-]\s*(.+)', title).groups()
        lec = {'num': int(num), 'title': name}
        sub = sub.group(1).strip() if sub else ''
        if sub and sub != course_title:   # early decks repeat the course name as their subtitle
            lec['sub'] = sub
        if topics:
            lec['topics'] = topics.group(1).strip()
        lec['pdf'] = pdf.name
        yield lec, pdf


def main():
    decks = Path(sys.argv[1]) if len(sys.argv) > 1 else SITE.parent / 'ros2-course'
    path = SITE / 'courses.json'
    courses = json.loads(path.read_text())
    course = next(c for c in courses if c['slug'] == SLUG)

    dest = SITE / 'slides' / SLUG
    dest.mkdir(parents=True, exist_ok=True)
    course['lectures'] = []
    for lec, pdf in covers(decks, course['title']):
        shutil.copy2(pdf, dest / pdf.name)
        course['lectures'].append(lec)

    path.write_text(json.dumps(courses, indent=2, ensure_ascii=False) + '\n')
    nums = ', '.join(str(lec['num']) for lec in course['lectures'])
    print(f'"{course["title"]}": lectures {nums} from {decks}')


if __name__ == '__main__':
    main()
