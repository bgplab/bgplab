# Upcoming Labs

While we're working on new stuff you can already enjoy [over a half dozen](index.md) labs. In case you're curious about what's coming next, here are a few ideas:

## Basic BGP Setup

* Redistribute IGP information into BGP
* Use BGP summarization to minimize the number of BGP advertisements

**Optional exercises:**

* Protect a BGP session with MD5 password, TCP-AO password, and TTL check
* Use session templates and BGP peer groups
* Improve convergence speed with BFD

**Advanced exercises:**

* Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses
* Run IPv4 and IPv6 over the same BGP session
* Fine-tune BGP Fast External Failover
* Configure BGP graceful restart

## Simple BGP Routing Policies

* Perform simple load balancing across parallel links and across upstream providers
* Use BGP link bandwidth to influence the load balancing weights

**Advanced exercises:**

* Use BGP route refresh and soft reconfiguration
* Use outbound route filters (ORF)

## BGP in Enterprise Networks

* Use IBGP with multiple WAN edge routers
* Use BGP local preference to prefer one of the upstream providers
* Use more complex BGP local preference setup to prefer direct connectivity with customers of upstream ISPs
* Use MED to influence route selection in an upstream ISP
* Use AS-path prepending to influence route selection across multiple upstream ISPs

## Controlling Inbound Traffic

* Use BGP communities to influence route selection in upstream ISPs
* Use controlled disaggregation to influence inbound traffic flow
* Use conditional route advertisements to select primary/backup links for the inbound traffic

## BGP in Service Provider Networks

* Build a simple service provider network with IBGP
* Use BGP route reflectors to reduce the number of IBGP sessions
* Use a hierarchy of route reflectors
* Build a transit autonomous system using BGP communities to change routing policies
* Reduce routing instabilities with BGP route flap dampening
* Implement policy-based routing with BGP

## Use MPLS with BGP 

* Use MPLS to build a BGP-free core
* Use SR-MPLS to minimize the number of control-plane protocols
* Use BGP Labeled Unicast to extend MPLS paths across multiple autonomous systems

