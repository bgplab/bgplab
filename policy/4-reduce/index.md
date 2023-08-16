# Minimize the Size of Your BGP Table

In the previous lab exercises you establish EBGP sessions with two upstream Service Providers, accepted all routes they were willing to send you, and let your router do its magic selecting the best BGP routes (either based on AS-path length or [weights](1-weights.md)).

That might not be a good idea if you bought cost-optimized hardware that can do packet forwarding at ludicrous speeds but only for a few tens of thousands of routes while your neighbors send you the full Internet BGP table (over 930.000 routes in August 2023).

In this lab exercise you'll use inbound filters to reduce the amount of information inserted in the BGP table (and subsequently routing table) of your device.

![Lab topology](topology-stop-transit.png)

Your link to ISP-1 is much faster than the link to ISP-2, so you have to use ISP-1 for most of the outbound traffic. As X1 advertises a default route to you, you don't have to accept any other routing information from it.

It would be a shame to let the link to ISP-2 remain idle while the link to ISP-1 is operational. Let's send the traffic for AS 65101 directly over the link to X2 -- that means you have to accept prefixes originated in AS 65101 from X2.

Finally, you'll need a default route even if the link to ISP-1 goes down. You should therefore accept the default route from ISP-2 as well, but make it less preferred than the one received from ISP-1.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each autonomous system advertises one loopback address and another IPv4 prefix. Upstream routers (x1, x2) also advertise the default route to your router (rtr).

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 10.0.0.1/32<br>192.168.42.0/24 |
| **AS65100** ||
| x1 | 10.0.0.10 | 10.0.0.10/32<br>192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 10.0.0.11/32<br>192.168.101.0/24 |

Your router has these EBGP neighbors. _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Neighbor | Neighbor IPv4 | Neighbor AS |
|----------|--------------:|------------:|
| x1 | 10.1.0.2 | 65100 |
| x2 | 10.1.0.6 | 65101 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/4-reduce`
* Execute **netlab up** ([other options](../external/index.md))
* Log into your device (RTR) with **netlab connect rtr** and verify IP addresses and BGP configuration.

**Note:** *netlab* will configure IP addressing, EBGP sessions, and BGP prefix advertisements on your router. If you're not using *netlab* just continue with the configuration you made during the [previous exercise](3-prefix.md).

## Configuration Tasks

* Configure a *prefix list* that will accept just the default route and apply it as an inbound filter on the EBGP session with X1. You did something very similar in the _[Filter Advertised Prefixes](3-prefix.md)_ exercise, so you should be familiar with the process.
* The inbound filter for X2 is a bit more complex: you have to accept a prefix if it originates in AS 65101 or if it's the default route. You already implemented [prefix filters](3-prefix.md) and [AS-path based filters](2-stop-transit.md), now you have to combine them. Implementing such a condition usually requires a more complex routing policy; many BGP implementations call it a *route map*. 

**Hint**: You'll have to get fluent with regular expressions if you want to become a master of BGP routing policies, but let's do things one step at a time -- the regular expression `65101$` matches prefixes originating in AS 65101.

* Finally, you have to make routes received from X1 preferred over routes received from X2. You did exactly that in the _[Select Preferred EBGP Peer with Weights](1-weights.md)_ exercise, so you're good to go.

!!! Warning
    Applying routing policy parameters to BGP neighbors doesn't necessarily change the BGP table as the new parameters might be evaluated only on new incoming updates -- you might have to use a command similar to `clear ip bgp * soft in` to tell your router to ask its neighbors to resend their BGP updates.

## Verification

Examine the BGP table on your device. It should contain:

* IP prefixes your device is originating;
* Two IP prefixes originated by X2
* Two paths for the default route; the path advertised by X1 should be the best path.

If you're using Arista EOS, you should get this printout:

```
rtr#sh ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      0.0.0.0/0              10.1.0.2              0       -          100     200     65100 i
 *        0.0.0.0/0              10.1.0.6              0       -          100     100     65101 i
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      10.0.0.11/32           10.1.0.6              0       -          100     100     65101 i
 * >      192.168.42.0/24        -                     -       -          -       0       ?
 * >      192.168.101.0/24       10.1.0.6              0       -          100     100     65101 i
```

## Reference Information

You might find the following information useful if you're not using _netlab_ to build the lab:

### Lab Wiring

This lab uses a subset of the [4-router lab topology](../external/4-router.md):

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | x1 | swp1 |
| rtr | Ethernet2 | x2 | swp1 |
| x1 | swp2 | x2 | swp2 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  10.0.0.10/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| swp2 | 10.1.0.9/30 |  | x1 -> x2 |
| **x2** |  10.0.0.11/32 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |
| swp2 | 10.1.0.10/30 |  | x2 -> x1 |
