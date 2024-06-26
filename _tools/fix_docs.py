#!/usr/bin/env python3
#
import os
import argparse
import subprocess

def parse_cli() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description='Migrate symbolic links')
  parser.add_argument('root', action='store',help='Root directory')
  return parser.parse_args()

def main() -> None:
  args = parse_cli()
  for root,dirs,files in os.walk(args.root):
    for fname in files:
      fpath = os.path.join(root,fname)
      if not os.path.islink(fpath):
        continue
      
      spath = os.path.abspath(os.path.join(os.path.dirname(fpath),os.readlink(fpath)))
      spath = os.path.relpath(spath)
#      os.remove(fpath)
#      os.rename(spath,fpath)
      print(f'moving {spath} -> {fpath}')
      subprocess.run(["git","rm",fpath])
      subprocess.run(["git","mv",spath,fpath])

main()