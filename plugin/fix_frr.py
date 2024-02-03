import os

from netsim import __version__
from netsim.utils import log
from box import Box

"""
The initial lab exercises do not use BGP configuration module on the customer
device because we want the user to start BGP configuration from scratch.

That approach does not work for FRR containers because you cannot restart FRR
after modifying /etc/frr/daemons -- restating FRR kills the top-level container
process. Cumulus Linux does not have the same problem as it runs a different
init process.

This plugin is a fix for the FRR container initialization: if the user is using
clab as primary or secondary provider and the RTR device is a FRR container, the
clab binds are replaced with a mapping of FRR daemons into a local file. The
modifier FRR daemons file starts BGP, OSPFv2 and OSPFv3 (so we have a generic
solution in case we need it somewhere else).

Finally, the plugin adds "we already started BGP daemon for you" message to the
topology message to tell the user what's going on.
"""
def post_node_transform(topology: Box) -> None:
  uses_clab = topology.get('provider',None) == 'clab' or topology.nodes.rtr.get('provider',None) == 'clab'
  uses_frr  = topology.nodes.rtr.device == 'frr'
  if not uses_clab or not uses_frr:
    return

  rtr = topology.nodes.rtr

  rtr.clab.pop('config_templates',None)
  rtr.clab.binds = []
  rtr.clab.binds.append('frr-daemons.j2:/etc/frr/daemons')

  if 'message' not in topology:
    topology.message = ''

  topology.message += '''
We already started BGP daemon in the FRR container. You can connect to
your device and start configuring BGP.
'''

  return
