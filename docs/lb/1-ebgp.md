# Load Balancing across External BGP Paths

Modern BGP implementations usually forward traffic across equal-cost external BGP paths (Equal-Cost Multipath or ECMP). Unfortunately, the default definition of the *equal-cost* paths usually includes *most BGP path attributes being equal*, and many implementations provide nerd knobs you can use to fine-tune which BGP path attributes you want to ignore when considering ECMP paths.

In this lab exercise, you'll observe simple EBGP ECMP across parallel paths toward AS 651000 (P1 and P2) and try to configure your router to forward traffic across all paths toward AS 65001 (P1, P2, and P3).

![Lab topology](topology-lb-ebgp.png)

!!! Warning
    ECMP traffic forwarding across multiple autonomous systems is usually not a good idea, as you need to know each autonomous system's internal structure and end-to-end delay. Still, you might have to configure multi-AS ECMP in environments that replaced IGP with EBGP.
    
## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. C2 and P1 advertise an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 |  |
| **AS65001** ||
| c2 | 10.7.5.0 | 10.7.5.0/24 |
| **AS65100** ||
| p1 | 10.0.0.2 | 10.1.3.0/24 |
| p2 | 10.0.0.3 |  |
| **AS65101** ||
| p3 | 10.0.0.4 |  |

Your router has these EBGP neighbors. _netlab_ configures them automatically; if you're using another lab infrastructure, you'll have to configure them manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **rtr** | 10.0.0.1 | 65000 |
| | p1 | 65100 | 10.1.0.1 |
| | p2 | 65100 | 10.1.0.5 |
| | p3 | 65101 | 10.1.0.9 | 

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `lb/1-ebgp`
* Execute **netlab up** ([device requirements](#req))
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

!!! warning
    This lab exercise requires _netlab_ release 1.6.4 or later.

## Configuration Tasks

Most BGP implementations have nerd knobs that change the EBGP load-balancing behavior:

* Configure load balancing across EBGP paths using a command similar to **maximum-paths**. Allow EBGP load balancing across at least four parallel paths.
* Configure your device to ignore AS path contents when searching for equal-cost paths. The command to use could start with **bgp bestpath**.

!!! tip
    Default values differ across vendors; your device might already be doing what we want it to do. If your device's default settings result in EBGP ECMP across multiple autonomous systems, try to find the configuration commands that would disable that behavior.

## Verification

Log into your device and inspect its BGP table. The BGP table should contain two equal-cost paths to 10.1.3.0/24 and three paths with equal AS-path length to 10.7.5.0/24.

Some BGP implementations show the ECMP status of alternate paths in the BGP table printout. For example, this is the printout from an Arista EOS device:

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
 * >Ec    10.1.3.0/24            10.1.0.5              0       -          100     0       65100 i
 *  ec    10.1.3.0/24            10.1.0.1              0       -          100     0       65100 i
 * >Ec    10.7.5.0/24            10.1.0.5              0       -          100     0       65100 65001 i
 *  ec    10.7.5.0/24            10.1.0.1              0       -          100     0       65100 65001 i
 *  ec    10.7.5.0/24            10.1.0.9              0       -          100     0       65101 65001 i
```

If your device does not provide that information, look into the IP routing table. It should contain two entries for 10.1.3.0/24 and three entries for 10.7.5.0/24. For example, these are the BGP entries in the IP routing table on a Cumulus Linux device:

```
rtr# show ip route bgp
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, D - SHARP,
       F - PBR, f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure
B>* 10.1.3.0/24 [20/0] via 10.1.0.1, swp1, weight 1, 00:00:08
  *                    via 10.1.0.5, swp2, weight 1, 00:00:08
B>* 10.7.5.0/24 [20/0] via 10.1.0.1, swp1, weight 1, 00:00:08
  *                    via 10.1.0.5, swp2, weight 1, 00:00:08
  *                    via 10.1.0.9, swp3, weight 1, 00:00:08
```

**Next:** [EBGP Load Balancing with BGP Link Bandwidth](2-dmz-bw.md)

## Reference Information

The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and provider routers.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | p1 | swp1 |
| rtr | Ethernet2 | p2 | swp1 |
| rtr | Ethernet3 | p3 | swp1 |
| p1 | swp2 | p2 | swp2 |
| p2 | swp3 | c2 | swp1 |
| p3 | swp2 | c2 | swp2 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | rtr -> p1 |
| Ethernet2 | 10.1.0.6/30 |  | rtr -> p2 |
| Ethernet3 | 10.1.0.10/30 |  | rtr -> p3 |
| **c2** |  10.7.5.0/24 |  | Loopback |
| swp1 | 10.1.0.17/30 |  | c2 -> p2 |
| swp2 | 10.1.0.21/30 |  | c2 -> p3 |
| **p1** |  10.0.0.2/32 |  | Loopback |
| swp1 | 10.1.0.1/30 |  | p1 -> rtr |
| swp2 | 10.1.0.13/30 |  | p1 -> p2 |
| **p2** |  10.0.0.3/32 |  | Loopback |
| swp1 | 10.1.0.5/30 |  | p2 -> rtr |
| swp2 | 10.1.0.14/30 |  | p2 -> p1 |
| swp3 | 10.1.0.18/30 |  | p2 -> c2 |
| **p3** |  10.0.0.4/32 |  | Loopback |
| swp1 | 10.1.0.9/30 |  | p3 -> rtr |
| swp2 | 10.1.0.22/30 |  | p3 -> c2 |
