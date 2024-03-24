---
title: Labs by BGP Attributes and Technologies
---
# Labs Sorted by BGP Attributes and Technologies

This page contains the alphabetical list of BGP attributes and technologies and the labs you can use to practice them:

Address families
: * [Configure BGP for IPv6](basic/4-ipv6.md)
  * [EBGP Sessions over IPv6 LLA Interfaces](basic/d-interface.md)

Advertising IP prefixes
: * [Advertise your IPv4 address space](basic/3-originate.md)
  * [Configure BGP for IPv6](basic/4-ipv6.md)
  * [Redistribute IGP Information Into BGP](basic/5-redistribute.md)
  * [BGP route aggregation](basic/8-aggregate.md)
  * [Advertise Default Route in BGP](basic/c-default-route.md)

AS and AS-path manipulation
: * [Use AS-Path Prepending to Influence Incoming Traffic Flow](policy/7-prepend.md)
  * [Reuse a BGP AS Number Across Multiple Sites](session/1-allowas_in.md) (**allowas-in**)
  * [Fix AS-Path in Environments Reusing BGP AS Numbers](session/2-asoverride.md) (**as-override**)
  * [Use Multiple AS Numbers on the Same Router](session/3-localas.md) (**local-as**)
  * [Remove Private BGP AS Numbers from the AS Path](session/4-removeprivate.md) (**remove-private-as**)

AS-path filters
: * [Prevent route leaking between upstream providers](policy/2-stop-transit.md) with an AS-path filter
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).
  * [Stop the Propagation of Configuration Errors](challenge/04-block-fat-fingers.md) (challenge lab)

BFD (Bidirectional Forwarding Detection)
: * [Use BFD to Speed Up BGP Convergence](basic/7-bfd.md)

Communities
: * [Attach BGP Communities to Outgoing BGP Updates](policy/8-community-attach.md)
  * [Use BGP Communities in Routing Policies](policy/9-community-use.md)
  * [Using No-Export Community to Filter Transit Routes](challenge/02-no-export.md) (coming soon)
  * [BGP Graceful Shutdown](challenge/03-graceful-shutdown.md) (coming soon)

Default route
: * [Advertise Default Route in BGP](basic/c-default-route.md)
  * [Minimize the Forwarding Table on BGP Routers](challenge/30-reduce-fib.md)

EBGP sessions
: * [Establish an EBGP session](basic/1-session.md) with an ISP
  * [Connect to two upstream providers](basic/2-multihomed.md)
  * [EBGP Sessions over IPv6 LLA Interfaces](basic/d-interface.md)
  * [Load Balancing across External BGP Paths](lb/1-ebgp.md)

Forwarding Table
: * [Minimize the Forwarding Table on BGP Routers](challenge/30-reduce-fib.md)

GTSM (Generic TTL Security Mechanism)
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

IBGP sessions
: * [Establish an IBGP session](ibgp/1-edge.md) between WAN edge routers
  * [Build a Transit Network with IBGP](ibgp/2-transit.md)
  * [Use BGP Route Reflectors](ibgp/3-rr.md)
  * [Use BGP Session Templates](session/6-templates.md)

Load balancing
: * [Load Balancing across External BGP Paths](lb/1-ebgp.md)

LOCAL_PREF (Local Preference)
: * [Implement a consistent AS-wide routing policy](policy/5-local-preference.md) with BGP local preference.
  * [Use BGP Communities in Routing Policies](policy/9-community-use.md)
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).
  * [BGP Graceful Shutdown](challenge/03-graceful-shutdown.md) (coming soon)

MD5 passwords
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

MULTI_EXIT_DISC (Multi-Exit Discriminator, MED)
: * [Use MED to Influence Incoming Traffic Flow](policy/6-med.md)

Prefix filters
: * [Filter prefixes advertised by your autonomous system](policy/3-prefix.md) with a prefix list
  * [Minimize the size of your BGP table](policy/4-reduce.md) with inbound filters
  * [Use the backup link to reach the adjacent autonomous system](policy/a-locpref-route-map.md).
  * [Limit the Number of Accepted BGP Prefixes](basic/b-max-prefix.md)
  * [Stop the Propagation of Configuration Errors](challenge/04-block-fat-fingers.md) (challenge lab)

Route reflectors
: * [Use BGP Route Reflectors](ibgp/3-rr.md)

Scalability
: * [Use BGP Session Templates](session/6-templates.md)
  * [Use BGP Policy Templates](session/7-policy.md)

TCP-AO
: [Use TCP Authentication Option (TCP-AO)](basic/9-ao.md)

TTL security
: * [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)

Weights
: * [Use BGP weights](policy/1-weights.md) to prefer one of the upstream providers
