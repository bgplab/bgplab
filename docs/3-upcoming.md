# Upcoming Labs

While we're working on new stuff, you can already enjoy [two dozen](index.md) labs. In case you're curious about what's coming next, here's what we're working on:

* [Using Bird BGP Daemon as a BGP Route Reflector](challenge/01-bird-rr.md)
* [Implement Anycast Services with BGP](challenge/02-anycast.md) 
* [EBGP-Only Data Center Design](challenge/05-ebgp-dc.md)
* [Multihop EBGP peering in a high-availability firewall scenario](challenge/22-bgp-ha-protocol.md)
* [Firewall-on-a-stick scenario with two VRFs in the directly attached router](challenge/21-loopback-vrf.md).

We have plenty of other ideas, including:

## Basic BGP Setup

Advanced exercises:
: * Configure BGP graceful restart

## Controlling Inbound Traffic

* Use conditional route advertisements to select primary/backup links for the inbound traffic

## BGP in Service Provider Networks

* Use a hierarchy of route reflectors
* Reduce routing instabilities with BGP route flap dampening
* Implement policy-based routing with BGP
* Remote-triggered black hole
* External bogon feed
* Centralized route collection service (like bgp.tools)
* Using RPKI for route validation (with Routinator as the source of RPKI information)

See [this LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7211620163396263936/) for more details.

## Advanced Scenarios

* Peering across a low-end router using a default route

See [this blog post](https://blog.ipspace.net/2024/06/ebgp-multihop-use-cases.html) for more details.

## Use MPLS with BGP 

* Use BGP Labeled Unicast to extend MPLS paths across multiple autonomous systems
