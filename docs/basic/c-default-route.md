# Advertise Default Route in BGP

In environments without a reliable link-layer failure detection mechanism, you might rely on a routing protocol (and BFD) to detect link failures. BGP is often used as a routing protocol between Service Providers and their customers (or between data center fabric switches and servers) because it has sufficient security mechanisms to make it safe to use with untrusted devices.

However, it might not make sense to advertise the whole Internet routing table to every customer running BGP; it's often good enough to advertise local prefixes and the default route, and that's what you'll do in this lab exercise.

![Lab topology](topology-default-route.png)
    
## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. X1 and R2 advertise an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| r1 | 10.0.0.1 |  |
| r2 | 10.0.0.2 | 192.168.42.0/24 |
| **AS65100** ||
| x1 | 10.0.0.10 | 172.16.37.0/24 |

Your router has these BGP neighbors and runs OSPF in area 0 with R2.  _netlab_ configures BGP and OSPF automatically; if you're using some other lab infrastructure, you'll have to configure them manually.

| Node | Neighbor | Neighbor AS | Neighbor IPv4 |
|------|----------|------------:|--------------:|
| **r1** | r2 | 65000 | 10.0.0.2 |
|  | x1 | 65100 | 10.1.0.2 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `basic/c-default-route`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with **netlab connect r1** and verify that the IP addresses and the EBGP sessions are properly configured.

## The Problem

R1 sends its whole BGP table to the customer router (X1). Within this lab, that's just a single BGP prefix, but it could be close to a million prefixes on the public Internet.

```
$ netlab connect x1 --show ip bgp
Connecting to clab-default-x1 using SSH port 22, executing show ip bgp
BGP routing table information for VRF default
Router identifier 172.16.37.1, local AS number 65100
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      172.16.37.0/24         -                     -       -          -       0       i
 * >      192.168.42.0/24        10.1.0.1              0       -          100     0       65000 i
```

While it's relatively easy to filter the outbound BGP updates on R1 and send nothing to X1, that would break connectivity as X1 would have no usable routing information. Before filtering BGP updates, R1 should advertise the default route to X1.

## Configuration Tasks

* Configure R1 to advertise the default route to X1 using a command similar to **neighbor default-originate**.

!!! Tip
    * Usually, you have to configure the default route advertisement within the address-family configuration.
    * When configured to do so, some BGP implementations unconditionally advertise the default route to BGP neighbors. Other implementations might advertise the default route only if the default route is present in the local BGP table. You might have to use the **default-originate always** configuration command with such implementations, as R1 does not have a default route.
    
* Use an outbound filter on R1 to stop the propagation of any other information to X1. You'll find more details in the [Filter Advertised Prefixes](../policy/3-prefix.md) lab exercise.

## Verification

You can use the **netlab validate** command if you've installed *netlab* release 1.8.3 or later and use Cumulus Linux, FRR, or Arista EOS on the external routers. The validation tests check:

* The state of the EBGP sessions between R1 and X1 and between R1 and R2
* Whether R1 sends the default route to X1
* Whether R1 sends any other prefixes to X1
* Whether R1 propagates the X1 prefix to R2

For example, this is the result you'd get if you configured the default route origination on R1 but not the outbound route filters.

![](basic-default-validate.png)

If the **netlab validate** command fails or you're using another network operating system on your devices, inspect the BGP table on X1 -- it should contain the local prefix and the default route.

```
$ netlab connect x1 --show ip bgp
Connecting to container clab-default-x1, executing sudo vtysh -c "show ip bgp"
BGP table version is 3, local router ID is 172.16.37.1, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 0.0.0.0/0        10.1.0.1                               0 65000 ?
*> 172.16.37.0/24   0.0.0.0                  0         32768 i

Displayed  2 routes and 2 total paths
```

You should also check the BGP table on R2 -- it should contain the local prefix (`172.16.37.0/24`) and the prefix advertised by X1 (`192.168.42.0/24`).

```
$ netlab connect r2 --show ip bgp
Connecting to container clab-default-r2, executing sudo vtysh -c "show ip bgp"
BGP table version is 2, local router ID is 192.168.42.1, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*>i172.16.37.0/24   10.0.0.1                 0    100      0 65100 i
*> 192.168.42.0/24  0.0.0.0                  0         32768 i

Displayed  2 routes and 2 total paths
```

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP and OSPF configuration modules](https://netlab.tools/platforms/#platform-routing-support).
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on X1 and R2.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
| Link with the customer | r1 | Ethernet1 | x1 | swp1 |
| Intra-ISP link | r1 | Ethernet2 | r2 | swp1 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **r1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | Link with the customer |
| Ethernet2 | 10.1.0.5/30 |  | Intra-ISP link |
| **r2** |  192.168.42.1/24 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | Intra-ISP link |
| **x1** |  172.16.37.1/24 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | Link with the customer |
