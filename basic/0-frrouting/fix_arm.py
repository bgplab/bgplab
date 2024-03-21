import os

from netsim import __version__
from netsim.utils import log
from netsim.augment.devices import get_provider
from netsim.cli.external_commands import run_command
from box import Box

"""
The lab exercise uses Cumulus Linux because we can restart the FRR daemons.
Unfortunately, the CL Docker image is not available on Apple silicon, so we have
to change the device type if running on ARM.
"""

def init(topology: Box) -> None:
  arch = run_command('uname -m', check_result=True, return_stdout=True)
  if not isinstance(arch,str):
    return
  
  if 'aarch64' not in arch:
    return
  
  topology.defaults.device = 'frr'
  topology.message = ""
  add_message(topology,"""
You're running the lab on ARM hardware. Changing device type to FRR.
""")
  return

"""
This lab exercises does not use BGP configuration module because we want the
user to start BGP configuration from scratch. That approach does not work for
FRR containers because you cannot restart FRR after modifying /etc/frr/daemons
-- restating FRR kills the top-level container process.

The post_node_transform fixes the FRR container initialization: if the user is
using clab as the node provider, and the node is FRR, the clab binds are
replaced with a mapping of FRR daemons into a local file. The modifier FRR
daemons file starts BGP, OSPFv2 and OSPFv3 (so we have a generic solution in
case we need it somewhere else).

Finally, the plugin adds "we already started BGP daemon for you" message to the
topology message to tell the user what's going on.
"""
def post_node_transform(topology: Box) -> None:
  change_binds = False

  for n_name, n_data in topology.nodes.items():
    if n_data.device != 'frr':
      continue

    if get_provider(n_data,topology.defaults) != 'clab':
      continue

    n_data.clab.pop('config_templates',None)
    n_data.clab.binds = []
    n_data.clab.binds.append('frr-daemons.j2:/etc/frr/daemons')
    change_binds = True

  if not change_binds:
    return

  add_message(topology,'''
We already started BGP daemon in the FRR container. You can connect to
your device with the 'netlab connect' command and start configuring BGP.
''')

"""
Add a notification to the lab startup message
"""
def add_message(topology: Box, msg: str) -> None:
  if 'message' not in topology:
    topology.message = ''

  topology.message += msg
