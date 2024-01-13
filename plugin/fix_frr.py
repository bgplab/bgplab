import os

from netsim import __version__
from netsim.utils import log
from box import Box

def init(topology: Box) -> None:
  topology.defaults.devices.frr.clab.node.pop('config_templates')

def post_node_transform(topology: Box) -> None:
  uses_clab = topology.get('provider',None) == 'clab' or topology.nodes.rtr.get('provider',None) == 'clab'
  uses_frr  = topology.nodes.rtr.device == 'frr'
  if not uses_clab or not uses_frr:
    return

  topology.nodes.rtr.clab.binds = []
  topology.nodes.rtr.clab.binds.append('frr-daemons.j2:/etc/frr/daemons')

  if 'message' not in topology:
    topology.message = ''

  topology.message += '''
We already started BGP daemon in the FRR container. You can connect to
your device and start configuring BGP.
'''

  return
