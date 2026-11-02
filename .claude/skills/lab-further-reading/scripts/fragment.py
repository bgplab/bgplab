#!/usr/bin/env python3
"""Build a text-fragment URL and optionally count phrase occurrences in a saved page.

Usage: fragment.py URL "phrase" [saved-page.html]
"""
import html
import re
import sys
from urllib.parse import quote


def fragment(url: str, phrase: str) -> str:
  # '-' is a text-fragment delimiter and must be percent-encoded
  return url.split('#')[0] + '#:~:text=' + quote(phrase, safe='').replace('-', '%2D')


def page_text(path: str) -> str:
  s = open(path, encoding='utf-8', errors='replace').read()
  s = re.sub(r'(?s)<(script|style).*?</\1>', ' ', s)
  return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))


def main() -> None:
  if len(sys.argv) not in (3, 4):
    sys.exit(__doc__)
  url, phrase = sys.argv[1], sys.argv[2]
  print(fragment(url, phrase))
  if len(sys.argv) == 4:
    count = page_text(sys.argv[3]).count(phrase)
    print(f'occurrences: {count}', file=sys.stderr)
    if count != 1:
      sys.exit(1)


if __name__ == '__main__':
  main()
