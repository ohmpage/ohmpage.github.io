#!/usr/bin/env python3
"""Import BibTeX entries as Hugo publication pages.

Requires: pip install "bibtexparser<2"

Usage:
  python scripts/import_pubs.py bib/mypubs.bib
  python scripts/import_pubs.py bib/mypubs.bib --overwrite
"""

import argparse
import re
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

SITE_AUTHOR = "Paul Ohm"
DEFAULT_PUB_DIR = "content/pub"


def key_to_slug(key):
    """CamelCase BibTeX key -> hyphenated-lowercase directory name.

    Examples: DataAnalysisRules -> data-analysis-rules, VanBuren -> van-buren
    """
    s = re.sub(r'([a-z])([A-Z])', r'\1-\2', key)
    return s.lower()


def parse_authors(author_str):
    """Split 'First Last and First Last' into a list of names."""
    if not author_str:
        return []
    return [a.strip() for a in author_str.split(' and ') if a.strip()]


def yaml_scalar(value):
    """Quote a YAML string value if it contains characters that need quoting."""
    s = str(value)
    if any(c in s for c in ':#{}[],&*!|>\'"@`'):
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return s


def write_index_md(path, entry, coauthors):
    title = entry.get('title', '').strip()
    year = entry.get('year', '').strip()
    date = f"{year}-01-01" if year else '1970-01-01'
    entrytype = entry.get('ENTRYTYPE', 'article').lower()
    pubtype = 'book' if entrytype == 'book' else 'article'
    yearadorn = entry.get('yearadorn', '').strip()
    link = entry.get('url', '').strip()

    lines = ['---']
    lines.append(f'title: {yaml_scalar(title)}')
    lines.append(f"date: '{date}'")
    lines.append(f'pubtype: {pubtype}')

    if pubtype == 'book':
        publisher = entry.get('publisher', '').strip()
        if publisher:
            lines.append(f'publisher: {yaml_scalar(publisher)}')
    else:
        publication = entry.get('journal', '').strip()
        volume = entry.get('volume', '').strip()
        pages = entry.get('pages', '').strip()
        if publication:
            lines.append(f'publication: {yaml_scalar(publication)}')
        if volume:
            lines.append(f"volume: '{volume}'")
        if pages:
            lines.append(f"pages: '{pages}'")

    if year:
        lines.append(f"year: '{year}'")
    if yearadorn:
        lines.append(f"yearadorn: '{yearadorn}'")
    if link:
        lines.append(f'link: {yaml_scalar(link)}')
    if coauthors:
        lines.append('coauthors:')
        for ca in coauthors:
            lines.append(f'- {yaml_scalar(ca)}')
    lines.append('draft: false')
    lines.append('---')

    path.write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Import BibTeX entries as Hugo publication pages.'
    )
    parser.add_argument('bibfile', help='Path to .bib file')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing entries')
    parser.add_argument('--pub-dir', default=DEFAULT_PUB_DIR,
                        help=f'Hugo content directory for pubs (default: {DEFAULT_PUB_DIR})')
    args = parser.parse_args()

    bp = BibTexParser(common_strings=True)
    bp.customization = convert_to_unicode

    with open(args.bibfile) as f:
        bib = bibtexparser.load(f, bp)

    pub_dir = Path(args.pub_dir)
    pub_dir.mkdir(parents=True, exist_ok=True)

    created = updated = skipped = 0

    for entry in bib.entries:
        key = entry['ID']
        slug = key_to_slug(key)
        entry_dir = pub_dir / slug
        existed = entry_dir.exists()

        if existed and not args.overwrite:
            print(f"  skip  {slug}")
            skipped += 1
            continue

        entry_dir.mkdir(exist_ok=True)
        all_authors = parse_authors(entry.get('author', ''))
        coauthors = [a for a in all_authors if a != SITE_AUTHOR]
        write_index_md(entry_dir / 'index.md', entry, coauthors)

        if existed:
            print(f"update  {slug}")
            updated += 1
        else:
            print(f"create  {slug}")
            created += 1

    print(f"\n{created} created, {updated} updated, {skipped} skipped")


if __name__ == '__main__':
    main()
