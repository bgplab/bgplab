---
title: Labs by BGP Attributes and Technologies
---
# Labs Sorted by BGP Attributes and Technologies

This page contains the alphabetical list of BGP attributes and technologies, and the labs you can use to practice them:

Address families
: * [Configure BGP for IPv6](basic/4-ipv6.md)

Advertising IP prefixes
: * [Advertise your IPv4 address space](basic/3-originate.md)
  * [Configure BGP for IPv6](basic/4-ipv6.md)
  * [Redistribute IGP Information Into BGP](basic/5-redistribute.md)
  * [BGP route aggregation](basic/8-aggregate.md)

AS and AS-path manipulation
: * [Use AS-Path Prepending to Influence Incoming Traffic Flow](policy/7-prepend.md)
  * [Reuse a BGP AS Number Across Multiple Sites](session/1-allowas_in.md)
  * [Fix AS-Path in Environments Reusing BGP AS Numbers](session/2-asoverride.md)

AS-path filters
: * [Prevent route leaking between upstream providers](policy/2-stop-transit.md) with an AS-path filter
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).

BFD (Bidirectional Forwarding Detection)
: * [Use BFD to Speed Up BGP Convergence](basic/7-bfd.md)

Communities
: * [Attach BGP Communities to Outgoing BGP Updates](policy/8-community-attach.md)
: * [Use BGP Communities in Routing Policies](policy/9-community-use.md)

EBGP sessions
: * [Establish an EBGP session](basic/1-session.md) with an ISP
  * [Connect to two upstream providers](basic/2-multihomed.md)

GTSM (Generic TTL Security Mechanism)
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

IBGP sessions
: * [Establish an IBGP session](ibgp/1-edge.md) between WAN edge routers
  * [Build a Transit Network with IBGP](ibgp/2-transit.md)
  * [Use BGP Route Reflectors](ibgp/3-rr.md)

LOCAL_PREF (Local Preference)
: * [Implement a consistent AS-wide routing policy](policy/5-local-preference.md) with BGP local preference.
  * [Use BGP Communities in Routing Policies](policy/9-community-use.md)
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).

MD5 passwords
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

MULTI_EXIT_DISC (Multi-Exit Discriminator, MED)
: * [Use MED to Influence Incoming Traffic Flow](policy/6-med.md)

Prefix filters
: * [Filter prefixes advertised by your autonomous system](policy/3-prefix.md) with a prefix list
  * [Minimize the size of your BGP table](policy/4-reduce.md) with inbound filters
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).

Route reflectors
: * [Use BGP Route Reflectors](ibgp/3-rr.md)

TCP-AO
: [Use TCP Authentication Option (TCP-AO)](basic/9-ao.md)

TTL security
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

Weights
: * [Use BGP weights](policy/1-weights.md) to prefer one of the upstream providers
