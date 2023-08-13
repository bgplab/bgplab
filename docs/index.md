---
title: Labs Overview
---
# ipSpace.net BGP Configuration Labs

The following series of hands-on labs will help you master numerous aspects of EBGP, IBGP, and BGP routing policy configuration on a platform of your choice[^PC].

[^PC]: Some assembly required: the Cumulus Linux VMs/containers that are used for external BGP speakers are easy to download, but you'll have to build a Vagrant box or install a vendor-supplied Vagrant box or Docker container image for most other platforms. See [installation and setup](1-setup.md) for details.

You can already do the following labs with over a dozen labs coming in the future (see the list of [upcoming labs](3-upcoming.md)).

## Basic BGP Setup

* [Establish an EBGP session](basic/1-session.md) with an ISP
* [Connect to two upstream providers](basic/2-multihomed.md)
* [Advertise your IPv4 address space](basic/3-originate.md)

## Simple BGP Routing Policies

* [Use BGP weights](policy/1-weights.md) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](policy/2-stop-transit.md) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](policy/3-prefix.md) with a prefix list
* [Minimize the size of your BGP table](policy/4-reduce.md) with inbound filters
