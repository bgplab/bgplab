---
title: Labs Overview
---
# Open-Source BGP Configuration Labs

This series of BGP hands-on labs will help you master numerous aspects of EBGP, IBGP, and BGP routing policy configuration on a [platform of your choice](https://netlab.tools/platforms/#platform-routing-support)[^PC], including:

* Arista EOS
* Aruba AOS-CX
* Cisco ASAv, IOSv, IOS XE, IOS XR and Nexus OS
* Cumulus Linux and FRR
* Dell OS10
* Juniper vSRX, vMX and vPTX
* Mikrotik RouterOS
* Nokia SR OS and SR Linux
* Vyatta VyOS

[^PC]: Some assembly required: the virtual machines or containers that we recommend to use as external BGP speakers are easy to download, but you'll have to build a Vagrant box or install a vendor-supplied Vagrant box or Docker container image for most other platforms. See [installation and setup](1-setup.md) for details.

More than a dozen labs are already waiting for you (with more [coming in the near future](3-upcoming.md)), but if this is your first visit to this site, you should start with the [Installation and Setup](1-setup.md) documentation.

## Deploy BGP in Your Network

In the first set of the BGP labs, you'll master these skills:

* [Configure BGP sessions and advertise IPv4 and IPv6 prefixes](basic/index.md#simple)
* [Protect BGP sessions](basic/index.md#protect)
* [Run BGP in networks with more than one BGP router](basic/index.md#ibgp)
* [Manipulate BGP AS numbers or AS paths](basic/index.md#aspath) with nerd knobs like **as-override** and **local-as**
* [Configure advanced BGP features](basic/index.md#advanced) like BFD or BGP route aggregation.

## BGP Routing Policies {#policy}

These lab exercises will help you master the basic tools you can use to build BGP routing policies that will:

* [Filter BGP Updates](policy/index.md#filter)
* [Adjust Outgoing Traffic Flow](policy/index.md#egress)
* [Influence Incoming Traffic Flow](policy/index.md#ingress)

Once you mastered the basics, continue with [more complex routing policies](policy/index.md#complex).

## Challenge Labs

Mastered the fundamentals and the nerd knobs? Want to tickle your gray cells? Try out the challenge labs:

* [Merge Networks Using Different BGP AS Numbers](challenge/20-merge-as.md)
