---
title: Overview
---
# ipSpace.net BGP Configuration Labs

The following series of hands-on labs will help you master numerous aspects of EBGP, IBGP, and BGP routing policy configuration on a platform of your choice[^PC].

You can already do the following labs:

### Basic BGP Setup

* [Establish a BGP session](basic/1-session.md)
* [Connect to two upstream providers](basic/2-multihomed.md)
* [Advertise your IPv4 address space](basic/3-originate.md)

### Simple End-User BGP Routing Policies

* [Use BGP weights](policy/1-weights.md) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](policy/2-stop-transit.md) with AS-path filters

## Upcoming Labs

**Basic BGP Setup**

* (Optional) Protect a BGP session with MD5 password, TCP-AO password, and TTL check
* (Advanced) Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses

**Simple End-User BGP Routing Policies**

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

[^PC]: Some assembly required: while the Cumulus Linux VMs/containers that are used for external BGP speakers are easy to download, you'll have to build a Vagrant box or install a Docker container image for your platform. 