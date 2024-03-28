import os

from netsim import __version__
from netsim.utils import log
from netsim.augment.devices import get_provider
from box import Box

"""
The lab exercise does not start MPLS or LDP on the customer devices because we
want the user to start MPLS configuration from scratch.

That approach does not work for FRR containers because you cannot restart FRR
after modifying /etc/frr/daemons -- restating FRR kills the top-level container
process.

This plugin is a fix for the FRR container initialization: if an FRR device is
using clab provider, the clab binds are replaced with a mapping of FRR daemons
into a local file. The modified FRR daemons file starts BGP, OSPFv2 and OSPFv3,
and LDP.

Finally, the plugin adds "we already started FRR daemons for you" message to the
topology message to tell the user what's going on.
"""
def post_node_transform(topology: Box) -> None:
  frr_found = False
  for n_name, n_data in topology.nodes.items():
    if n_data.device != 'frr':
      continue

    if get_provider(n_data,topology.defaults) != 'clab':
      continue

    n_data.clab.pop('config_templates',None)
    n_data.clab.binds = []
    n_data.clab.binds.append('frr-daemons:/etc/frr/daemons')
    frr_found = True

  if not frr_found:
    return

  if 'message' not in topology:
    topology.message = ''

  topology.message += '''
Note: we already started all the prerequisite daemons in the FRR containers.
'''

  return
