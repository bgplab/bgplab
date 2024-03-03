import os

from netsim.utils import log
from netsim.augment import devices
from box import Box

"""
Pretend that all devices know how to deal with IPv4 unnumbered interfaces and IPv6 LLA BGP sessions
"""
def pre_transform(topology: Box) -> None:
  for name,ndata in topology.nodes.items():       # First, save current IPv4 unnumbered status
    features = devices.get_device_features(ndata,topology.defaults)
    ndata._has_ipv4_unnumbered = features.initial.ipv4.unnumbered

  for name,ndata in topology.nodes.items():       # Next, set all the flags needed to keep netlab happy
    if name in topology.groups.external:          # Skip external devices, they really have to support
      continue                                    # ... the required features or they won't be configured

    features = devices.get_device_features(ndata,topology.defaults)
    features.initial.ipv4.unnumbered = True
    features.bgp.ipv6_lla = True                  # We can fake BGP IPv6 LLA/RFC 8950 support
    features.bgp.rfc8950 = True                   # ... as we won't configure EBGP sessions on customer devices

def post_transform(topology: Box) -> None:
  for name,ndata in topology.nodes.items():       # Final fixup for customer devices
    if name in topology.groups.external.members:  # Skip external devices in this loop
      continue

    for intf in ndata.interfaces:                 # Iterate over customer router's interfaces
      intf.pop('ipv6',None)                       # Disable IPv6 (the user has to figure out how to enable it)
      if ndata._has_ipv4_unnumbered:              # The device has IPv4 unnumbered, nothing to do
        continue
      if intf.get('ipv4',False) is True:          # ... and remove all references to IPv4 unnumbered
        intf.pop('ipv4',None)

  for name,ndata in topology.nodes.items():       # Final fixup for external devices
    if name not in topology.groups.external.members:
      continue                                    # Skip customer devices in this loop

    for ngb in ndata.bgp.neighbors:               # Iterate over BGP neighbors
      if ngb.get('ipv4',None):                    # Make all EBGP sessions unnumbered
        ngb.ipv4 = True
        ngb.ipv4_rfc8950 = True

        # Copy interface name into BGP neighbor data and enable IPv6 on the interface
        #
        ngb.local_if = ndata.interfaces[ngb.ifindex - 1].ifname
        ndata.interfaces[ngb.ifindex-1].ipv6 = True
