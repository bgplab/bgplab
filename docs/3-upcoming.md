# Upcoming Labs

While we're working on new stuff you can already enjoy [over a half dozen](index.md) labs. In case you're curious about what's coming next, here are a few ideas:

## Basic BGP Setup

* Run BGP with IPv6
* (Optional) Protect a BGP session with MD5 password, TCP-AO password, and TTL check
* (Advanced) Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses
* (Advanced) Run IPv4 and IPv6 over the same BGP session
* Redistribute IGP information into BGP
* Use BGP summarization to minimize the number of BGP advertisements

## Simple BGP Routing Policies

* Perform simple load balancing across parallel links and across upstream providers

## BGP in Enterprise Networks

* Use IBGP with multiple WAN edge routers
* Use BGP local preference to prefer one of the upstream providers
* Use more complex BGP local preference setup to prefer direct connectivity with customers of upstream ISPs
* Use MED to influence route selection in an upstream ISP
* Use AS-path prepending to influence route selection across multiple upstream ISPs

## Controlling Inbound Traffic

* Use BGP communities to influence route selection in upstream ISPs

## BGP in Service Provider Networks

* Build a simple service provider network with IBGP
* Use BGP route reflectors to reduce the number of IBGP sessions
* Use a hierarchy of route reflectors
* Build a transit autonomous system using BGP communities to change routing policies

## Use MPLS with BGP 

* Use MPLS to build a BGP-free core
* Use SR-MPLS to minimize the number of control-plane protocols
