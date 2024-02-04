# Upcoming Labs

While we're working on new stuff, you can already enjoy [two dozen](index.md) labs. In case you're curious about what's coming next, here's what we're working on:

* [Using No-Export Community to Filter Transit Routes](challenge/02-no-export.md)
* [BGP Graceful Shutdown](challenge/03-graceful-shutdown.md)
* [Using Bird BGP Daemon as a BGP Route Reflector](challenge/01-bird-rr.md)
* [BGP Route Server in an Internet Exchange Point](session/5-routeserver.md)

We have plenty of other ideas, including:

## Basic BGP Setup

Optional exercises:
: * Run BGP on servers

Advanced exercises:
: * Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses
  * Run IPv4 and IPv6 over the same BGP session
  * Fine-tune BGP Fast External Failover
  * Configure BGP graceful restart

## Simple BGP Routing Policies

* Perform simple load balancing across parallel links and upstream providers
* Use BGP DMZ bandwidth to influence the load-balancing weights

Advanced exercises:
: * Use BGP route refresh and soft reconfiguration
  * Use outbound route filters (ORF)

## Controlling Inbound Traffic

* Use AS-path prepending together with BGP communities to prevent BGP wedgies
* Use controlled disaggregation to influence inbound traffic flow
* Use conditional route advertisements to select primary/backup links for the inbound traffic

## BGP in Service Provider Networks

* Build a simple service provider network with IBGP
* Use a hierarchy of route reflectors
* Reduce routing instabilities with BGP route flap dampening
* Implement policy-based routing with BGP
* Use a BGP route server

## Use MPLS with BGP 

* Use MPLS to build a BGP-free core
* Use SR-MPLS to minimize the number of control-plane protocols
* Use BGP Labeled Unicast to extend MPLS paths across multiple autonomous systems

