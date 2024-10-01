import os

from netsim import __version__
from netsim.utils import log
from box import Box

"""
See the plugin/fix_frr.py for details
"""
def post_node_transform(topology: Box) -> None:
  rtr = topology.nodes.core
  uses_clab = topology.get('provider',None) == 'clab' or topology.nodes.rtr.get('provider',None) == 'clab'
  uses_frr  = rtr.device == 'frr'
  if not uses_clab or not uses_frr:
    return

  rtr.clab.pop('config_templates',None)
  rtr.clab.binds = []
  rtr.clab.binds.append('frr-daemons.j2:/etc/frr/daemons')

  if 'message' not in topology:
    topology.message = ''

  topology.message += '''
Note: we started BGP daemons in all FRR containers.
'''

  return
