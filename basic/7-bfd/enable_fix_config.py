import os

from netsim.utils import log
from box import Box

"""
Enable extra config for devices that need minor tweaks to be set up just right

Initial use case: BGP hello timers on FRR/CL
"""

def post_transform(topology: Box) -> None:
  fix_directory = 'fix-config'

  for ndata in topology.nodes.values():
    fix_file = f'{ os.path.dirname(__file__) }/{ fix_directory }/{ ndata.name }.{ ndata.device }.j2'
    if os.path.exists(fix_file):
      ndata.config = ndata.config or []
      ndata.config.append(fix_directory)
