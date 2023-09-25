# ipSpace.net BGP Configuration Labs

This repository contains _netlab_ topology files for a series of hands-on labs will help you master numerous aspects of EBGP,  IBGP, and BGP routing policy configuration on a platform of your choice[^PC]. The labs cover:

**Basic BGP Setup**

* [Establish a BGP session](basic/1-session)
* [Connect to two upstream providers](basic/2-multihomed)
* [Advertise your IP prefixes](basic/3-originate)
* [Protect EBGP sessions](basic/6-protect)
* [Configure BGP for IPv6](basic/4-ipv6)
* [Redistribute IGP Information Into BGP](basic/5-redistribute)
* [Use BFD to Speed Up BGP Convergence](basic/7-bfd)

**Simple End-User Setup**

* [Use BGP weights](policy/1-weights) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](policy/2-stop-transit) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](policy/3-prefix) with a prefix list
* [Minimize the size of your BGP table](policy/4-reduce) with inbound filters

See [lab documentation](https://ipspace.github.io/bgplab/) for the full list of planned labs.
<!--
**Basic BGP Setup**

* (Advanced) Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses

**Simple End-User Setup**

* Minimize the size of your BGP table with inbound filters
* Redistribute IGP information into BGP and use BGP summarization to minimize the number of BGP advertisements
* Perform simple load balancing across parallel links and across upstream provider

**Multiprotocol BGP**

* Run BGP with IPv6
* (Advanced) Run IPv4 and IPv6 over the same BGP session

**Simple Transit Network Setup**

* Use IBGP to transport BGP information across your network
* Use BGP route reflectors to reduce the number of IBGP sessions
* (Advanced) Use a hierarchy of route reflectors

**Networks with Multiple BGP Speakers**

* Use multiple WAN edge routers to connect to upstream ISPs
* Use BGP local preference to prefer one of the upstream providers
* Use more complex BGP local preference setup to prefer direct connectivity with customers of upstream ISPs
* Use MED to influence route selection in an upstream ISP
* Use AS-path prepending to influence route selection across multiple upstream ISPs

**Complex BGP Route Policies**

* Use BGP communities to influence route selection in upstream ISPs
* Build a transit autonomous system using BGP communities to change routing policies
-->

[^PC]: Some assembly required: while the Cumulus Linux VMs/containers that are used for external BGP speakers are easy to download, you'll have to build a Vagrant box or install a Docker container image for your platform. 