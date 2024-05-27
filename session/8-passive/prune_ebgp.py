import os

from box import Box

"""
netlab generates a full mesh of EBGP sessions between lab devices. This
plugin prunes all inter-ISP EBGP sessions, leaving just the sessions
with the route server.
"""
def post_transform(topology: Box) -> None:
  for n_name, n_data in topology.nodes.items():
    if 'rs' in n_name:
      continue

    n_data.bgp.neighbors = [ ngb for ngb in n_data.bgp.neighbors if 'rs' in ngb.name ]
