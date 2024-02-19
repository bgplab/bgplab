# ipSpace.net BGP Configuration Labs

This repository contains _netlab_ topology files for a series of hands-on labs that will help you master numerous aspects of EBGP,  IBGP, and BGP routing policy configuration on a platform of your choice[^PC]. The labs cover:

**Basic BGP Setup**

* [Configuring and monitoring routing daemons on Cumulus Linux and FRRouting](basic/0-frrouting)
* [Establish a BGP session](basic/1-session)
* [Connect to two upstream providers](basic/2-multihomed)
* [Advertise your IP prefixes](basic/3-originate)
* [Configure BGP for IPv6](basic/4-ipv6)
* [Redistribute IGP Information Into BGP](basic/5-redistribute)

**Protecting BGP Sessions**

* [Protect EBGP sessions](basic/6-protect) with MD5 passwords and TTL protection (GTSM)
* Protect BGP sessions with [TCP Authentication Option (TCP-AO)](basic/9-ao)
* [Limit the Number of Accepted BGP Prefixes](basic/b-max-prefix)

**Running BGP in Larger Networks**

* [Establish an IBGP session](ibgp/1-edge) between WAN edge routers
* [Build a Transit Network with IBGP](ibgp/2-transit)
* [Use BGP Route Reflectors](ibgp/3-rr)
* [Use BGP Session Templates](session/6-templates)
* [Use BGP Policy Templates](session/7-policy)

**Simple BGP Routing Policies**

* [Use BGP weights](policy/1-weights) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](policy/2-stop-transit) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](policy/3-prefix) with a prefix list
* [Minimize the size of your BGP table](policy/4-reduce) with inbound filters
* [Implement a consistent AS-wide routing policy](policy/5-local-preference) with BGP local preference.
* [Use MED to Influence Incoming Traffic Flow](policy/6-med)
* [Use AS-Path Prepending to Influence Incoming Traffic Flow](policy/7-prepend)
* [Attach BGP Communities to Outgoing BGP Updates](policy/8-community-attach)

**Complex BGP Routing Policies**

* [Use BGP Communities in Routing Policies](policy/9-community-use)
* [Using BGP Local Preference in a Complex Routing Policy](policy/a-locpref-route-map)
* [Use BGP Policy Templates](session/7-policy)

**Advanced Topics**

* [Use BFD to Speed Up BGP Convergence](basic/7-bfd)
* [BGP route aggregation](basic/8-aggregate)
* [Reuse a BGP AS Number Across Multiple Sites](session/1-allowas_in)
* [Fix AS-Path in Environments Reusing BGP AS Numbers](session/2-asoverride)
* [Use Multiple AS Numbers on the Same Router](session/3-localas)
* [Remove Private BGP AS Numbers from the AS Path](session/4-removeprivate)
* [Advertise Default Route in BGP](basic/c-default-route)

See [lab documentation](https://bgplab.github.io/bgplab/) for more details and the complete list of planned labs.

[^PC]: Some assembly required: while the Cumulus Linux VMs/containers used for external BGP speakers are easy to download, you'll have to build a Vagrant box or install a Docker container image for your platform.