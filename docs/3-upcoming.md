# Upcoming Labs

While we're working on new stuff, you can already enjoy [two dozen](index.md) labs. In case you're curious about what's coming next, here's what we're working on:

* [Using No-Export Community to Filter Transit Routes](challenge/02-no-export.md)
* [BGP Graceful Shutdown](challenge/03-graceful-shutdown.md)
* [Using Bird BGP Daemon as a BGP Route Reflector](challenge/01-bird-rr.md)
* [BGP Route Server in an Internet Exchange Point](session/5-routeserver.md)
* [Use controlled disaggregation to influence inbound traffic flow](policy/b-disaggregate.md)
* [IBGP Load Balancing with BGP Link Bandwidth](lb/3-ibgp.md)
* [IBGP Load Balancing with BGP Additional Paths](lb/4-ibgp-add-path.md)
* [Minimize the Forwarding Table on Provider Edge Routers](challenge/30-reduce-fib.md)

We have plenty of other ideas, including:

## Basic BGP Setup

Optional exercises:
: * Run BGP on servers
  * Multihop EBGP sessions
  * Dynamic BGP neighbors
  * Passive BGP peers

Advanced exercises:
: * Fine-tune BGP Fast External Failover
  * Configure BGP graceful restart
  * Multihop EBGP sessions with servers

## BGP Routing Policies

Advanced exercises:
: * Use BGP route refresh and soft reconfiguration
  * Use outbound route filters (ORF)

## Controlling Inbound Traffic

* Use AS-path prepending together with BGP communities to prevent BGP wedgies
* Use conditional route advertisements to select primary/backup links for the inbound traffic

## BGP in Service Provider Networks

* Build a simple service provider network with IBGP
* Use a hierarchy of route reflectors
* Reduce routing instabilities with BGP route flap dampening
* Implement policy-based routing with BGP

## Use MPLS with BGP 

* Use BGP Labeled Unicast to extend MPLS paths across multiple autonomous systems
