# Upcoming Labs

While we're working on new stuff, you can already enjoy [two dozen](index.md) labs. In case you're curious about what's coming next, here are a few ideas:

## Basic BGP Setup

Optional exercises:
: * Use session templates and BGP peer groups

Advanced exercises:
: * Change the BGP AS number presented to the BGP neighbor (**local-as** functionality)
  * Disable AS path check on incoming updates (**allowas-in** functionality)
  * Remove private AS numbers from the AS path
  * Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses
  * Run IPv4 and IPv6 over the same BGP session
  * Fine-tune BGP Fast External Failover
  * Configure BGP graceful restart

## Simple BGP Routing Policies

* Perform simple load balancing across parallel links and upstream providers
* Use BGP link bandwidth to influence the load-balancing weights

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

## Use MPLS with BGP 

* Use MPLS to build a BGP-free core
* Use SR-MPLS to minimize the number of control-plane protocols
* Use BGP Labeled Unicast to extend MPLS paths across multiple autonomous systems

