---
title: Labs Overview
---
# ipSpace.net BGP Configuration Labs

The following series of hands-on labs will help you master numerous aspects of EBGP, IBGP, and BGP routing policy configuration on a platform of your choice[^PC].

[^PC]: Some assembly required: the Cumulus Linux VMs/containers that are used for external BGP speakers are easy to download, but you'll have to build a Vagrant box or install a vendor-supplied Vagrant box or Docker container image for most other platforms. See [installation and setup](1-setup.md) for details.

You can already do the following labs with tons of labs coming in the future (see the list of [upcoming labs](3-upcoming.md)). However, you should probably read the [Installation and Setup](1-setup.md) documentation first.

## Getting Started

The first set of the BGP labs focuses on the basics:

* Establishing BGP sessions
* Advertising IPv4 and IPv6 prefixes
* Building networks with more than one BGP-speaking router
* Protecting BGP sessions
* Other useful topics like using BFD or BGP route aggregation.

It's best if you take the labs in this order:

### Setting Up BGP

* [Establish an EBGP session](basic/1-session.md) with an ISP
* [Connect to two upstream providers](basic/2-multihomed.md)
* [Advertise your IPv4 address space](basic/3-originate.md)
* [Configure BGP for IPv6](basic/4-ipv6.md)
* [Redistribute IGP Information Into BGP](basic/5-redistribute.md)

### Protecting BGP Sessions (Optional)

* [Use MD5 passwords and TTL-based session protection](basic/6-protect.md)
* [Use TCP Authentication Option (TCP-AO)](basic/9-ao.md)

### Running BGP in Larger Networks

* [Establish an IBGP session](ibgp/1-edge.md) between WAN edge routers

### Other Useful Topics

* [Use BFD to Speed Up BGP Convergence](basic/7-bfd.md)
* [BGP route aggregation](basic/8-aggregate.md)

## Simple BGP Routing Policies

The second set of lab exercises helps you master simple BGP routing policies including:

* [Use BGP weights](policy/1-weights.md) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](policy/2-stop-transit.md) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](policy/3-prefix.md) with a prefix list
* [Minimize the size of your BGP table](policy/4-reduce.md) with inbound filters