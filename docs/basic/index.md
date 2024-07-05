# Deploy BGP in Your Network

The first set of the BGP labs focuses on the basics:

* Configuring BGP sessions and advertising IPv4 and IPv6 prefixes
* Protecting BGP sessions
* Running BGP in networks with more than one BGP router
* Other valuable topics like using BFD or BGP route aggregation.

If you use Cumulus Linux or FRR in your labs (either as the customer routers or as the external routers), start with [Configuring Cumulus Linux and FRRouting](0-frrouting.md). Next, take the labs in this order:

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
* [Limit the Number of Accepted BGP Prefixes](b-max-prefix.md)

## Running BGP in Larger Networks {#ibgp}

If your network has multiple BGP routers, they must exchange BGP information. While it's possible to build a network where each BGP router uses a different autonomous system number (hint: don't), running *Internal BGP* (IBGP) between routers in your network is more common. You can practice IBGP in these lab exercises:

* [Establish an IBGP session](../ibgp/1-edge.md) between WAN edge routers
* [Build a Transit Network with IBGP](../ibgp/2-transit.md)
* [Use BGP Route Reflectors](../ibgp/3-rr.md)

Other important aspects of large-scale BGP deployments are scalability and consistency. The following lab exercises will help you grasp those concepts:

* [Use BGP Session Templates](../session/6-templates.md)
* [Use BGP Policy Templates](../session/7-policy.md)
* [Dynamic BGP Peers](../session/9-dynamic.md)

## BGP AS Number and AS Path Manipulations {#aspath}

Even though one should not use the same BGP AS number in multiple networks or more than one BGP AS number on a single device, you'll always stumble upon scenarios that violate the common-sense rules. In these lab exercises, you'll practice how to deal with them:

* [Reuse a BGP AS Number Across Multiple Sites](../session/1-allowas_in.md)
* [Fix AS-Path in Environments Reusing BGP AS Numbers](../session/2-asoverride.md)
* [Use Multiple AS Numbers on the Same Router](../session/3-localas.md)
* [Remove Private BGP AS Numbers from the AS Path](../session/4-removeprivate.md)
* [BGP Route Server in an Internet Exchange Point](../session/5-routeserver.md)

## BGP Load Balancing {#lb}

Modern BGP implementations perform simple EBGP and IBGP equal-cost multipathing[^ECMP] (ECMP) without additional configuration. Still, you might have to fine-tune it to adapt its behavior to your environment. These lab exercises cover the typical scenarios:

* [Load Balancing across External BGP Paths](../lb/1-ebgp.md)
* [EBGP Load Balancing with BGP Link Bandwidth](../lb/2-dmz-bw.md)
* [IBGP Load Balancing with BGP Link Bandwidth](../lb/3-ibgp.md) 
* [IBGP Load Balancing with BGP Additional Paths](../lb/4-ibgp-add-path.md)

[^ECMP]: Sending traffic toward a single destination across multiple equal-cost paths. Packet distribution across paths (load balancing) depends on the device configuration and the implementation details, and might be done per-packet, per-session, or per-destination.

## Other Useful Topics {#advanced}

Willing to learn more? Challenge yourself with these advanced topics:

* [Use BGP Timers and BFD to Speed Up BGP Convergence](7-bfd.md)
* [BGP route aggregation](8-aggregate.md)
* [Advertise Default Route in BGP](c-default-route.md)
* [EBGP Sessions over IPv6 LLA Interfaces](d-interface.md)
* [Running EBGP Across a Firewall](e-ebgp-multihop.md)
* [Passive BGP Sessions](../session/8-passive.md)
