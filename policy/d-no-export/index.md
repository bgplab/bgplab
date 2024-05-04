# Using No-Export Community to Filter Transit Routes

[RFC 1997](https://www.rfc-editor.org/rfc/rfc1997.html) defined several well-known BGP communities recognized by almost all BGP implementations. One of them is the NO_EXPORT community, defined as:

> All routes received carrying a communities attribute containing this value MUST NOT be advertised outside a BGP confederation boundary (a stand-alone autonomous system that is not part of a confederation should be considered a confederation itself).

Forgetting the weird wording, the NO_EXPORT community attached to a BGP prefix means "_do not advertise this one over EBGP sessions_" -- seemingly an ideal solution to our *[do not leak transit routes](2-stop-transit.md)* challenge. You'll practice that scenario in this lab exercise.

![Lab topology](topology-no-export.png)

!!! Tip
    Do this lab exercise after completing the [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md) one.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. X1 and X2 advertise an IPv4 prefix each.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| c1 | 10.0.0.1 |  |
| c2 | 10.0.0.2 |  |
| **AS65100** ||
| x1 | 10.0.0.10 | 10.42.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 10.43.101.0/24 |

Your routers run OSPF in area 0. They have these EBGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **c1** | 10.0.0.1 | 65000 |
| | c2 | 65000 | 10.0.0.2 |
| | x1 | 65100 | 10.1.0.2 |
| **c2** | 10.0.0.2 | 65000 |
| | c1 | 65000 | 10.0.0.1 |
| | x2 | 65101 | 10.1.0.6 |

_netlab_ configures your routers when you start the lab; if you're using some other lab infrastructure, you'll have to configure them manually.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/d-no-export`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your routers with **netlab connect** and verify they are properly configured.

## The Problem

Assuming your routers don't use default EBGP route filters compliant with RFC 8212[^DF], they will leak prefixes between AS 65100 and AS 65101. Check the BGP table on X1 to see whether it contains the prefix advertised by X2.

[^DF]: To make this lab exercise useful, configure a *permit all* EBGP route policy if your devices comply with RFC 8212. 

```
$ netlab connect x1 --show ip bgp
Connecting to container clab-noexport-x1, executing sudo vtysh -c "show ip bgp"
BGP table version is 4, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.1/32      10.1.0.1                               0 65000 i
*> 10.0.0.2/32      10.1.0.1                               0 65000 i
*> 10.42.100.0/24   0.0.0.0                  0         32768 i
*> 10.43.101.0/24   10.1.0.1                               0 65000 65101 i

Displayed  4 routes and 4 total paths
```

## Configuration Tasks

All modern BGP implementations should support the NO_EXPORT BGP community. We'll use that community to stop the route leaks in the customer network.

* If needed, configure propagation of standard BGP communities between C1 and C2.
* On C1 and C2, use a route map to add the NO_EXPORT community to all incoming EBGP updates. You did something similar in the [Attach BGP Communities to Outgoing BGP Updates](../policy/8-community-attach.md) lab exercise.

## Verification

Check the BGP prefix 10.42.100.0/24 (advertised by X1) on C1. It should have the BGP community NO_EXPORT:

```
c1#show ip bgp 10.42.100.0
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.42.100.0/24
 Paths: 1 available
  65100
    10.1.0.2 from 10.1.0.2 (10.0.0.10)
      Origin IGP, metric 0, localpref 100, IGP metric 0, weight 0, tag 0
      Received 00:02:21 ago, valid, external, best
      Community: no-export
      Rx SAFI: Unicast
```

Check the same prefix on C2. The NO_EXPORT community should still be attached to the BGP prefix:

```
c2#show ip bgp 10.42.100.0
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for 10.42.100.0/24
 Paths: 1 available
  65100
    10.0.0.1 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, IGP metric 20, weight 0, tag 0
      Received 00:01:55 ago, valid, internal, best
      Community: no-export
      Rx SAFI: Unicast
```

Check the routes C2 advertises to X2 to verify it no longer advertises the prefix from AS 65100:

```
c2#show ip bgp neighbor 10.1.0.6 advertised-routes
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast, q - Queued for advertisement
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            10.1.0.5              -       -          -       -       65000 i
 * >      10.0.0.2/32            10.1.0.5              -       -          -       -       65000 i
```

Check the BGP table on X2. It should not contain the BGP prefix advertised by X1:

```
$ netlab connect x2 --show ip bgp
Connecting to container clab-noexport-x2, executing sudo vtysh -c "show ip bgp"
BGP table version is 5, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.1/32      10.1.0.5                               0 65000 i
*> 10.0.0.2/32      10.1.0.5                               0 65000 i
*> 10.43.101.0/24   0.0.0.0                  0         32768 i

Displayed  3 routes and 3 total paths
```

**Next:** 

* [Use BGP Communities in Routing Policies](9-community-use.md)

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and external routers.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
| Link to AS 65100 | c1 | Ethernet1 | x1 | swp1 |
| Unused link | c1 | Ethernet2 | x2 | swp1 |
| Unused link | x1 | swp2 | x2 | swp2 |
| Unused link | c2 | Ethernet1 | x1 | swp3 |
| Link to AS 65101 | c2 | Ethernet2 | x2 | swp3 |
| Customer internal link | c1 | Ethernet3 | c2 | Ethernet3 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **c1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | Link to AS 65100 |
| Ethernet2 |  |  | Unused link |
| Ethernet3 | 172.16.0.1/24 |  | Customer internal link |
| **c2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 |  |  | Unused link |
| Ethernet2 | 10.1.0.5/30 |  | Link to AS 65101 |
| Ethernet3 | 172.16.0.2/24 |  | Customer internal link |
| **x1** |  10.42.100.1/24 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | Link to AS 65100 |
| swp2 |  |  | Unused link |
| swp3 |  |  | Unused link |
| **x2** |  10.43.101.1/24 |  | Loopback |
| swp1 |  |  | Unused link |
| swp2 |  |  | Unused link |
| swp3 | 10.1.0.6/30 |  | Link to AS 65101 |

