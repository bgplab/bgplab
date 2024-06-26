#!/usr/bin/env python3
#
import os
import sys
import re
import fnmatch
import pathlib

def main() -> None:
  for root,dirs,files in os.walk("."):
    root = os.path.relpath(root)
    if '/' not in root:
      continue
    for fname in fnmatch.filter(files,'README.md'):
      fpath = os.path.join(root,fname)
      mdtext = pathlib.Path(fpath).read_text()
      newtext = re.sub('\(https://bgplabs.net/(?P<lnk>.*?)/\)','(../../docs/\g<lnk>.md)',mdtext)

      if newtext != mdtext:
        pathlib.Path(fpath).write_text(newtext)
        print(f'Fixed {fpath}')

main()