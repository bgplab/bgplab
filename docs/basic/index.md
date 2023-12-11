# Deploy BGP in Your Network

The first set of the BGP labs focuses on the basics:

* Configuring BGP sessions and advertising IPv4 and IPv6 prefixes
* Protecting BGP sessions
* Running BGP in networks with more than one BGP router
* Other valuable topics like using BFD or BGP route aggregation.

It's best if you take the labs in this order:

## Simple BGP Deployments {#simple}

In these labs, you'll learn how to:

* [Establish an EBGP session](1-session.md) with an ISP
* [Connect to two upstream providers](2-multihomed.md)
* [Advertise your IPv4 address space](3-originate.md)
* [Configure BGP for IPv6](4-ipv6.md)
* [Redistribute IGP Information Into BGP](5-redistribute.md)

## Protecting BGP Sessions (Optional) {#protect}

You should always protect the control plane of your router and the routing protocols it's running. While it's impossible to achieve perfect results without using access control lists, you should also master the BGP tools at your disposal:

* [Use MD5 passwords and TTL-based session protection](6-protect.md)
* [Use TCP Authentication Option (TCP-AO)](9-ao.md)

## Running BGP in Larger Networks {#ibgp}

If your network has multiple BGP routers, they must exchange BGP information. While it's possible to build a network where each BGP router uses a different autonomous system number (hint: don't), running *Internal BGP* (IBGP) between routers in your network is more common.

* [Establish an IBGP session](../ibgp/1-edge.md) between WAN edge routers
* [Build a Transit Network with IBGP](../ibgp/2-transit.md)
* [Use BGP Route Reflectors](../ibgp/3-rr.md)

## Other Useful Topics {#advanced}

Willing to learn more? Challenge yourself with these advanced topics:

* [Use BFD to Speed Up BGP Convergence](7-bfd.md)
* [BGP route aggregation](8-aggregate.md)
* [Reuse a BGP AS Number Across Multiple Sites](../session/1-allowas_in.md)
