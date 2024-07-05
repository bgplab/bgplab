# IBGP Load Balancing with BGP Link Bandwidth

In the [previous lab exercise](2-dmz-bw.md), you used the BGP Link Bandwidth extended community to implement unequal-cost load balancing across multiple links connected to the same router. In this exercise, you'll use the same approach but extend it across your autonomous system — routers receiving external routes over IBGP should perform unequal-cost multipathing (UCMP) toward external destinations based on the BGP Link Bandwidth extended community attached to BGP paths.

![Lab topology](topology-lb-ibgp-dmz-bw.png)

## Existing Router Configuration

The routers in your lab use the following BGP AS numbers. X1 and X2 advertise a shared IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| core | 10.0.0.1 |  |
| we1 | 10.0.0.2 |  |
| we2 | 10.0.0.3 |  |
| **AS65100** ||
| x1 | 10.0.0.4 | 10.1.3.0/24 |
| x2 | 10.0.0.5 | 10.1.3.0/24 |

Your routers are running OSPF in the backbone area. They have these BGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **core** | 10.0.0.1 | 65000 |
| | we1 | 65000 | 10.0.0.2 |
| | we2 | 65000 | 10.0.0.3 |
| **we1** | 10.0.0.2 | 65000 |
| | core | 65000 | 10.0.0.1 |
| | we2 | 65000 | 10.0.0.3 |
| | x1 | 65100 | 10.1.0.10 |
| | x1 | 65100 | 10.1.0.14 |
| **we2** | 10.0.0.3 | 65000 |
| | core | 65000 | 10.0.0.1 |
| | we1 | 65000 | 10.0.0.2 |
| | x2 | 65100 | 10.1.0.18 |

 _netlab_ automatically configures IP addresses and routing protocols; if you're using some other lab infrastructure, you'll have to configure your devices manually.
 
## Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and provider routers.
* Git repository contains external router initial device configurations for Cumulus Linux.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `lb/3-ibgp`
* Execute **netlab up** ([device requirements](#req))
* Log into your routers and verify that the IP addresses and the EBGP sessions are properly configured.

!!! warning
    This lab exercise requires _netlab_ release 1.6.4 or later.

## The Problem

Log into the Core router and check its BGP table. It should have two paths for the 10.1.3.0/24 prefix.

```
core#show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >Ec    10.1.3.0/24            10.0.0.2              0       -          100     0       65100 i
 *  ec    10.1.3.0/24            10.0.0.3              0       -          100     0       65100 i
```

Configuring IBGP load balancing on the Core router will send half of the outgoing traffic for the 10.1.3.0/24 prefix each way. That's undesirable, as the WE1-X1 path has significantly more bandwidth than the WE2-X2 path.

## Configuration Tasks

The simplest way to change the load balancing ratio on the Core router is to use the BGP Link Bandwidth extended community:

* Attach the BGP Link Bandwidth community to EBGP paths on WE1 and WE2[^ULB]. The bandwidth on the WE1-X1 links is 10Gbps, and the WE2-X2 link has 4 Gbps.
* Configure UCMP load balancing on the Core router
* Configure propagation of extended communities between WE1, WE2, and Core routers[^NCP]. On some devices, you'll also have to configure the propagation of the BGP Link Bandwidth community.
* If possible, aggregate the bandwidth on WE1 -- it should advertise a single prefix with BGP Link Bandwidth set to 20 Gbps[^NLB].

!!! tip
    You practiced the first two tasks in the [EBGP Load Balancing with BGP Link Bandwidth](2-dmz-bw.md) exercise and the third one in the [Attach BGP Communities to Outgoing BGP Updates](../policy/8-community-attach.md) exercise.

[^ULB]: If possible, set the interface bandwidth on the Wan Edge routers and use a command that copies the interface bandwidth into the BGP Link Bandwidth community.

[^NCP]: Without this step, the Core router would not receive the BGP Link Bandwidth community WE1 and WE2 attached to the EBGP prefixes.

[^NLB]: You might have to configure EBGP load balancing on WE1; some implementations advertise only the *usable* bandwidth for a prefix, not the theoretical *aggregate* bandwidth.

## Verification

Log into the Core router and inspect the BGP prefix 10.1.3.0. The paths advertised by WE1 and WE2 should have the BGP Link Bandwidth community. The value advertised by WE1 should be set to 10 or 20 Gbps[^BOB] (try to get it to 20 Gbps); the value advertised by WE2 should be 4 Gbps.

[^BOB]: Some platforms display the BGP Link Bandwidth community in bytes per second. Multiply that value by eight to get the bps value.

```
core>show ip bgp 10.1.3.0/24
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.1.3.0/24
 Paths: 2 available
  65100
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric 0, localpref 100, IGP metric 20, weight 0, tag 0
      Received 00:01:26 ago, valid, internal, ECMP head, ECMP, UCMP, best, ECMP contributor
      Extended Community: Link-Bandwidth-AS:65000:500.0 MBps
      Rx SAFI: Unicast
  65100
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, IGP metric 20, weight 0, tag 0
      Received 00:00:27 ago, valid, internal, ECMP, UCMP, ECMP contributor
      Extended Community: Link-Bandwidth-AS:65000:2.5 GBps
      Rx SAFI: Unicast
```

Check the prefix 10.1.3.0/24 in the IP routing table. The load balancing ratio displayed by the Core router depends on its implementation details, but you should observe an unequal traffic distribution. This is what you could get on an Arista cEOS container:

```
core#show ip route 10.1.3.0
...

 B I      10.1.3.0/24 [200/0]
           via 10.1.0.2, Ethernet1, weight 3/4
           via 10.1.0.6, Ethernet2, weight 1/4
```

**Next:** [IBGP Load Balancing with BGP Additional Paths](4-ibgp-add-path.md)

## Reference Information

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| core | Ethernet1 | we1 | Ethernet1 |
| core | Ethernet2 | we2 | Ethernet1 |
| we1 | Ethernet2 | x1 | swp1 |
| we1 | Ethernet3 | x1 | swp2 |
| we2 | Ethernet2 | x2 | swp1 |
| x1 | swp3 | x2 | swp2 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **core** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | core -> we1 |
| Ethernet2 | 10.1.0.5/30 |  | core -> we2 |
| **we1** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | we1 -> core |
| Ethernet2 | 10.1.0.9/30 |  | we1 -> x1 |
| Ethernet3 | 10.1.0.13/30 |  | we1 -> x1 |
| **we2** |  10.0.0.3/32 |  | Loopback |
| Ethernet1 | 10.1.0.6/30 |  | we2 -> core |
| Ethernet2 | 10.1.0.17/30 |  | we2 -> x2 |
| **x1** |  10.0.0.4/32 |  | Loopback |
| swp1 | 10.1.0.10/30 |  | x1 -> we1 |
| swp2 | 10.1.0.14/30 |  | x1 -> we1 |
| swp3 | 10.1.0.21/30 |  | x1 -> x2 |
| **x2** |  10.0.0.5/32 |  | Loopback |
| swp1 | 10.1.0.18/30 |  | x2 -> we2 |
| swp2 | 10.1.0.22/30 |  | x2 -> x1 |
