#!/usr/bin/env python3
#
# Check that all lab topology files have a 'version' attribute with a value
# of at least 2.0.0 (using Python version comparison rules from packaging).
#
import os
import sys
import fnmatch
import pathlib
import yaml

MIN_VERSION = '2.0.0'

def check_file(fpath: str) -> list:
  errors = []
  try:
    content = pathlib.Path(fpath).read_text()
    # topology files may start with a comment before the YAML document marker
    data = yaml.safe_load(content)
  except Exception as e:
    errors.append(f'{fpath}: failed to parse YAML: {e}')
    return errors

  if not isinstance(data, dict):
    errors.append(f'{fpath}: topology is not a YAML mapping')
    return errors

  if 'version' not in data:
    errors.append(f'{fpath}: missing "version" attribute')
    return errors

  version_str = str(data['version'])
  try:
    from packaging.version import Version
    if Version(version_str) < Version(MIN_VERSION):
      errors.append(
        f'{fpath}: version {version_str!r} is less than required {MIN_VERSION}')
  except Exception as e:
    errors.append(f'{fpath}: invalid version value {version_str!r}: {e}')

  return errors

def find_topology_files(root: str) -> list:
  results = []
  for dirpath, dirs, files in os.walk(root):
    # Skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fname in fnmatch.filter(files, 'topology.yml'):
      results.append(os.path.join(dirpath, fname))
  return sorted(results)

def main() -> None:
  if len(sys.argv) > 1:
    files = sys.argv[1:]
  else:
    files = find_topology_files('.')

  all_errors = []
  for fpath in files:
    all_errors.extend(check_file(fpath))

  if all_errors:
    for err in all_errors:
      print(err, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
  main()
