# EBGP Load Balancing with BGP Link Bandwidth

In [the previous exercise](1-ebgp.md), you configured Equal-Cost Multipathing (ECMP) between EBGP paths. ECMP results in your router sending approximately the same amount of traffic across all equal-cost links. That approach results in suboptimal performance if the links have different bandwidths, in which case you need *Weighted* ECMP[^SCDW].

[^SCDW]: The costs of the alternate paths are the same, thus ECMP, but the load-balancing algorithm uses unequal weights.

Most BGP implementations support the *[BGP Link Bandwidth Extended Community](https://datatracker.ietf.org/doc/html/draft-ietf-idr-link-bandwidth-07)*, which can influence the load balancing ratios across links with unequal bandwidth.

![Lab topology](topology-lb-dmz-bw.png)

In this lab exercise, you'll ignore the Multi-Exit Discriminator metric the adjacent autonomous system uses to tell you to avoid the slower link and configure the BGP link bandwidth community to send less traffic over it than over the faster link.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each router router advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 10.0.0.1/32 |
| **AS65100** ||
| x1 | 10.0.0.2 | 10.1.3.0/24 |
| x2 | 10.0.0.3 | 10.1.3.0/24 |

Your router has these EBGP neighbors.  _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **rtr** | 10.0.0.1 | 65000 |
| | x1 | 65100 | 10.1.0.2 |
| | x2 | 65100 | 10.1.0.6 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `lb/2-dmz-bw`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

!!! warning
    This lab exercise requires _netlab_ release 1.6.4 or later.

## The Problem

Log into your router and check its BGP table. It should have two paths for the prefix 10.1.3.0/24, but only one of them is used due to its lower MED value:

```
rtr>show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      10.1.3.0/24            10.1.0.6              100     -          100     0       65100 i
 *        10.1.3.0/24            10.1.0.2              200     -          100     0       65100 i
```

You would like to use both links toward AS 65100, preferably in a 2:1 ratio.

## Configuration Tasks

To implement unequal-cost multipathing, you have to:

* Configure ECMP load balancing for EBGP paths (see the [Load Balancing across External BGP Paths](1-ebgp.md) exercise for more details).
* Make both paths toward 10.1.3.0/24 equal from the BGP path selection perspective. Use an inbound route map to remove the MED attribute from incoming updates or set MED in all incoming updates to the same value. Alternatively, some platforms allow you to tweak the BGP route selection algorithm to ignore MED values.
* Set the BGP link bandwidth extended community on incoming BGP updates received from AS 65100 to influence the unequal-cost multipathing load-balancing ratio. That community is usually set in an inbound route map; some platforms allow you to set the default value per BGP neighbor.
* Enable BGP UCMP and configure your router to use the BGP link bandwidth community to calculate the relative amount of traffic sent over each link.

!!! tip
    If you're not familiar with BGP route maps, do the [Use MED to Influence Incoming Traffic Flow](../policy/6-med.md) and [Attach BGP Communities to Outgoing BGP Updates](../policy/8-community-attach.md) exercises first.

!!! Warning
    You might have to use a command similar to `clear ip bgp * soft in` to tell your router to ask its neighbors to resend their BGP updates after changing the inbound route maps.

## Verification

Check the BGP table to verify that:

* All paths to the 10.1.3.0/24 prefix have the same MED value
* Your router uses all those paths as ECMP/UCMP paths.

This is the printout you should get on Arista EOS:

```
rtr#show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >Ec    10.1.3.0/24            10.1.0.2              100     -          100     0       65100 i
 *  ec    10.1.3.0/24            10.1.0.6              100     -          100     0       65100 i
```

Inspect the BGP information for the 10.1.3.0/24 prefix to verify that the BGP link bandwidth community is attached to individual paths. This is how Arista EOS displays that information:

```
rtr#show ip bgp 10.1.3.0/24
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.1.3.0/24
 Paths: 2 available
  65100
    10.1.0.2 from 10.1.0.2 (10.0.0.2)
      Origin IGP, metric 100, localpref 100, IGP metric 0, weight 0, tag 0
      Received 00:33:58 ago, valid, external, ECMP head, ECMP, UCMP, best, ECMP contributor
      Extended Community: Link-Bandwidth-AS:65100:250.0 MBps
      Rx SAFI: Unicast
  65100
    10.1.0.6 from 10.1.0.6 (10.0.0.3)
      Origin IGP, metric 100, localpref 100, IGP metric 0, weight 0, tag 0
      Received 00:33:58 ago, valid, external, ECMP, UCMP, ECMP contributor
      Extended Community: Link-Bandwidth-AS:65100:125.0 MBps
      Rx SAFI: Unicast
```

Check the UCMP weights in the IP routing table. While this information might be challenging to get on some platforms, Arista EOS makes it very explicit:

```
rtr#show ip route 10.1.3.0/24
...
 B E      10.1.3.0/24 [200/100]
           via 10.1.0.2, Ethernet1, weight 2/3
           via 10.1.0.6, Ethernet2, weight 1/3
```

**Next:** [IBGP Load Balancing with BGP Link Bandwidth](3-ibgp.md)

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer router.
* This lab does not include automated validation.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | x1 | swp1 |
| rtr | Ethernet2 | x2 | swp1 |
| x1 | swp2 | x2 | swp2 |

!!! note
    You don't have to use the X1-X2 link, but you'll have to adjust the initial device configurations for X1 and X2 if you decide not to use it.

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  10.0.0.2/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| swp2 | 10.1.0.9/30 |  | x1 -> x2 |
| **x2** |  10.0.0.3/32 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |
| swp2 | 10.1.0.10/30 |  | x2 -> x1 |
