import os

from box import Box

def post_transform(topology: Box) -> None:
  n_list = topology.get('nodes.x2.bgp.neighbors',[])
  if not n_list:
    return
  
  for ngb in n_list:
    if ngb.name == 'rtr':
      ngb['as'] = 65007
