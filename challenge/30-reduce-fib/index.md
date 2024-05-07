# Minimize the Forwarding Table on BGP Routers

The global Internet BGP routing table has close to a million entries, and even though most of them would be reachable from the same small set of exit points from your network, you still have to store them in the forwarding tables of your routers, making your devices more expensive than necessary.

A more innovative design would use default routing toward the network core and store only the locally significant routes in the forwarding tables of the routers facing the end customers. You would still have to use expensive gear for the core routers and devices peering with upstream Service Providers, but you could use more optimized equipment on the customer-facing devices.

![Lab topology](topology-reduce-fib.png)

Many modern BGP implementations provide filters between the BGP table and the main IP routing table or between the IP routing table and the forwarding table. In this exercise, you will use that functionality to remove the routes the upstream Service Providers advertised from the forwarding table on a Provider Edge router.

!!! Expert
    This is an expert-level challenge lab -- you are on your own. Good luck and Godspeed!

## Existing Routing Protocol Configuration

The routers in your lab use the following BGP AS numbers. Each customer router advertises an IPv4 prefix; upstream routers advertise numerous prefixes.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65001** ||
| ce1 | 10.17.1.1 | 10.17.1.0/24 |
| **AS65002** ||
| ce2 | 10.22.2.1 | 10.22.2.0/24 |
| **AS65003** ||
| ce3 | 10.15.3.1 | 10.15.3.0/24 |
| **AS65100** ||
| c1 | 10.0.0.1 |  |
| pe1 | 10.0.0.2 |  |
| **AS65200** ||
| xa | 10.0.0.3 | 172.18.3.0/24<br>172.18.12.0/22<br>172.18.32.0/21<br>192.168.200.0/22 |
| **AS65201** ||
| xb | 10.0.0.4 | 172.19.7.0/24<br>172.20.32.0/22<br>172.19.40.0/21<br>192.168.77.0/24 |

Your routers run OSPF on the intra-AS link and have the following BGP neighbors. _netlab_ configures OSPF and BGP on your devices automatically; you'll have to configure them manually if you're using another lab infrastructure.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **c1** | 10.0.0.1 | 65100 |
| | pe1 | 65100 | 10.0.0.2 |
| | ce2 | 65002 | 10.1.0.14 |
| | xa | 65200 | 10.1.0.18 |
| | xb | 65201 | 10.1.0.22 |
| **pe1** | 10.0.0.2 | 65100 |
| | c1 | 65100 | 10.0.0.1 |
| | ce1 | 65001 | 10.1.0.1 |
| | ce3 | 65003 | 10.1.0.5 |

## Device Requirements

While you can use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and provider routers, not all devices supported BGP-to-RIB filters:

* Cumulus Linux and FRR work as expected, but the FRR containers don't use the BGP default route. They don't have a management VRF and have a static default route configured by the virtualization system in the global routing table.
* While Arista EOS documentation claims Arista EOS supports this feature, I couldn't make it work.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `challenge/30-reduce-fib`
* Execute **netlab up**
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

!!! tip
    The Git repository contains external router initial device configurations for Cumulus Linux.

## The Problem

Log into PE1 and inspect its BGP table and routing table. Its routing table contains all BGP prefixes received from the upstream ISPs.

```
pe1# show ip route bgp
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, D - SHARP,
       F - PBR, f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure
  *                     via 10.1.0.9, swp3, weight 1, 00:00:11
B>* 10.15.3.0/24 [20/0] via 10.1.0.5, swp2, weight 1, 00:00:11
B>* 10.17.1.0/24 [20/0] via 10.1.0.1, swp1, weight 1, 00:00:11
B>  10.22.2.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                        via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.18.3.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                         via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.18.12.0/22 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                          via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.18.32.0/21 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                          via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.19.7.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                         via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.19.40.0/21 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                          via 10.1.0.9, swp3, weight 1, 00:00:11
B>  172.20.32.0/22 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                          via 10.1.0.9, swp3, weight 1, 00:00:11
B>  192.168.77.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                           via 10.1.0.9, swp3, weight 1, 00:00:11
B>  192.168.200.0/22 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
  *                            via 10.1.0.9, swp3, weight 1, 00:00:11
```

## Configuration Guidelines

* On the PE router, use the filter between the BGP table and the main routing table to remove routes advertised by AS 65200 and AS 65201 (the upstream providers) from the forwarding table. Alternatively, you could remove all BGP routes with C1 as the next hop from the forwarding table.
* After you remove those routes from the forwarding table, your customers can no longer reach upstream destinations (because they are not in the PE router FIB) even though the PE router is still advertising them. Use [BGP default routing](../basic/c-default-route.md) to give the PE router a default exit point through C1. However, you should not advertise that default to the customers.

## Verification

Log into the lab routers and verify that:

* The routing table on PE1 no longer contains prefixes from AS 65200 or AS 65201:

```
pe1# show ip route bgp
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, D - SHARP,
       F - PBR, f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure
B>  0.0.0.0/0 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:03
  *                     via 10.1.0.9, swp3, weight 1, 00:00:03
B>* 10.15.3.0/24 [20/0] via 10.1.0.5, swp2, weight 1, 00:00:03
B>* 10.17.1.0/24 [20/0] via 10.1.0.1, swp1, weight 1, 00:00:03
B>  10.22.2.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:03
  *                        via 10.1.0.9, swp3, weight 1, 00:00:03
```

* The BGP table on CE1 contains all prefixes from AS 65200 and AS 65201 but not the default route.

```
ce1# show ip bgp
BGP table version is 12, local router ID is 10.17.1.1, vrf id 0
Default local pref 100, local AS 65001
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.15.3.0/24     10.1.0.2                               0 65100 65003 i
*> 10.17.1.0/24     0.0.0.0                  0         32768 i
*> 10.22.2.0/24     10.1.0.2                               0 65100 65002 i
*> 172.18.3.0/24    10.1.0.2                               0 65100 65200 i
*> 172.18.12.0/22   10.1.0.2                               0 65100 65200 i
*> 172.18.32.0/21   10.1.0.2                               0 65100 65200 i
*> 172.19.7.0/24    10.1.0.2                               0 65100 65201 i
*> 172.19.40.0/21   10.1.0.2                               0 65100 65201 i
*> 172.20.32.0/22   10.1.0.2                               0 65100 65201 i
*> 192.168.77.0/24  10.1.0.2                               0 65100 65201 i
*> 192.168.200.0/22 10.1.0.2                               0 65100 65200 i
```

* CE1 can ping `172.18.3.1`, a destination in AS 65200[^OD]:

[^OD]: That's the only destination you can ping in the upstream autonomous systems.

```
ce1(bash)#ping -I 10.17.1.1 172.18.3.1
PING 172.18.3.1 (172.18.3.1) from 10.17.1.1 : 56(84) bytes of data.
64 bytes from 172.18.3.1: icmp_seq=1 ttl=62 time=0.089 ms
64 bytes from 172.18.3.1: icmp_seq=2 ttl=62 time=0.052 ms
64 bytes from 172.18.3.1: icmp_seq=3 ttl=62 time=0.058 ms
64 bytes from 172.18.3.1: icmp_seq=4 ttl=62 time=0.074 ms
^C
```
