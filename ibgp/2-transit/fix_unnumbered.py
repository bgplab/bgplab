import os

from netsim.utils import log
from netsim.augment import devices
from box import Box

def pre_link_transform(topology: Box) -> None:
  w_header = True

  x_dev_list: set = set()

  for link in topology.links:
    if link.get('prefix.ipv4',False) is not True:           # Not an unnumbered link, move on
      continue

    for intf in link.interfaces:
      ndata = topology.nodes[intf.node]
      features = devices.get_device_features(ndata,topology.defaults)
      if features.initial.ipv4.unnumbered and \
         isinstance(features.ospf,Box) and \
         features.ospf.unnumbered:                          # Does the device support OSPF unnumbered?
        continue

      x_dev_list.add(ndata.device)
      link.pop('prefix',None)

  if not x_dev_list:
    return

  topology.message += f'''
WARNING
===============================================================================
Device(s) in your lab ({' '.join(list(x_dev_list))}) do not support unnumbered OSPF interfaces or
OSPF running over such interfaces. Lab links have been changed to regular IPv4
subnets. That change will impact lab addressing and some of printouts.
'''
