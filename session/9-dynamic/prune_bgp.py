import os

from box import Box

"""
The BGP sessions on the hub router must use dynamic BGP neighbors. Remove BGP
neighbors from the hub router data model.
"""
def post_transform(topology: Box) -> None:
  topology.nodes.hub.bgp.neighbors = []
