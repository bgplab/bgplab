from box import Box
import netsim.utils.log as log

def post_transform(topology: Box) -> None:
  for ndata in topology.nodes.values():
    if not 'bgp' in ndata:
      continue

    ndata.bgp.pop('rr',None)
