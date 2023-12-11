import os

from box import Box

def init(topology: Box) -> None:
  if 'device' not in topology.get('groups.external') and \
     'device' in topology.get('defaults.groups.external'):
    topology.groups.external.device = topology.defaults.groups.external.device

  return
