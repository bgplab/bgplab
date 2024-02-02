# BGP Policy Templates

Finishing at least some of the [BGP routing policies](../policy/index.md) exercises probably made you realize how many nerd knobs one can attach to a BGP neighbor. Now imagine applying that set of settings to dozens of neighbors you have at an Internet Exchange Point (or to hundreds of customer connections) while making sure the changes in your policy are consistently applied to every neighbor.

While network automation is the obvious answer to the above challenge, you might find *BGP policy templates* (or *BGP peer groups*) helpful. They allow you to group all relevant BGP settings into a single object and apply them as a group to a BGP neighbor. That's what you'll practice in this lab exercise.

![Lab topology](topology-policy-template.png)

!!! Tip
    This lab exercise uses AS-path filters, prefix filters, and BGP communities. Before starting this one, complete the [routing policies](../policy/index.md) lab exercises.
    
## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each router advertises one or more IPv4 prefixes.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 192.168.42.0/24<br>10.0.0.1/32 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.1/24<br>10.0.0.10/32 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.1/24<br>10.0.0.11/32 |

Your router has these EBGP neighbors.  _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to manually configure EBGP neighbors and advertised prefixes.

| Node | Neighbor | Neighbor AS | Neighbor IPv4 |
|------|----------|------------:|--------------:|
| **rtr** | x1 | 65100 | 10.1.0.2 |
|  | x2 | 65101 | 10.1.0.6 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `session/7-policy`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with the **netlab connect rtr** command and verify that the IP addresses and the EBGP sessions are properly configured.

## The Problem

The neighboring autonomous systems advertise too specific prefixes to your router, and your current configuration is no better. This is the current BGP table of your router as displayed on an Arista cEOS container:

```
rtr>show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      10.0.0.10/32           10.1.0.2              0       -          100     0       65100 i
 * >      10.0.0.11/32           10.1.0.6              0       -          100     0       65101 i
 * >      192.168.42.0/24        -                     -       -          -       0       ?
 * >      192.168.100.0/24       10.1.0.2              0       -          100     0       65100 i
 * >      192.168.101.0/24       10.1.0.6              0       -          100     0       65101 i
```

You'll have to deploy input and output filters to remove the unwanted prefixes, and you'll have to apply them to all misbehaving neighbors -- an ideal use case for BGP policy templates.

## Configuration Steps

You'll have to configure the BGP route filters before getting to the crux of this exercise. That shouldn't be a problem: you already did that in the [Filter Advertised Prefixes](../policy/3-prefix.md) and [Minimize the Size of Your BGP Table](../policy/4-reduce.md) lab exercises.

To make things more interesting:

* Attach BGP community 65000:200 to BGP prefixes received from X1 and X2
* Attach BGP community 65000:300 to local prefixes.[^TRM]

!!! tip
    You did something similar in the [Attach BGP Communities to Outgoing BGP Updates](../policy/8-community-attach.md) lab exercise.

[^TRM]: Those communities could be used in other autonomous systems to separate *peer* routes from *transit* routes.

Once you have configured the necessary route filters:

* Create a BGP *policy template* (some implementations might call them *peer groups*).
* Attach the route filters to the policy template.
* Attach the policy template to all EBGP neighbors.
* Resend the BGP updates to the EBGP neighbors with soft inbound and outbound resets of the EBGP sessions.

!!! tip
    Some BGP implementations (for example, Cisco IOS) have *session templates* that control the parameters of a BGP session (source interface, MD5 password) and *policy templates* that control the processing of inbound- and outbound BGP updates. You usually apply *session templates* to BGP neighbors at the routing protocol level and *policy templates* at the address family level.
    
    Other BGP implementations (for example, Arista EOS) have just the BGP *‌peer groups*. You can use them to apply *‌session* and *‌policy* parameters to BGP neighbors, often at the routing protocol level. Sometimes, you must apply the same peer groups at the address family level to attach the routing filters to BGP neighbors.

## Verification

* Inspect the BGP table on your router. You should see the /24 prefixes from X1 and X2 but not their /32 prefixes.

```
rtr>show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      192.168.42.0/24        -                     -       -          -       0       ?
 * >      192.168.100.0/24       10.1.0.2              0       -          100     0       65100 i
 * >      192.168.101.0/24       10.1.0.6              0       -          100     0       65101 i
```

* Inspect an individual prefix received from X1 or X2. It should have the BGP community 65000:200.

```
rtr>show ip bgp 192.168.100.0
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 192.168.100.0/24
 Paths: 1 available
  65100
    10.1.0.2 from 10.1.0.2 (10.0.0.10)
      Origin IGP, metric 0, localpref 100, IGP metric 0, weight 0, tag 0
      Received 00:27:02 ago, valid, external, best
      Community: 65000:200
      Rx SAFI: Unicast
```

* Inspect the BGP table on X1. You should see the /24 prefixes from RTR and X2 but not their /32 prefixes.

```
$ netlab connect x1 -q --show ip bgp | grep Network -A 100
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.10/32     0.0.0.0                  0         32768 i
*> 192.168.42.0/24  10.1.0.1                               0 65000 ?
*> 192.168.100.0/24 0.0.0.0                  0         32768 i
*> 192.168.101.0/24 10.1.0.1                               0 65000 65101 i

Displayed  4 routes and 4 total paths
```

* Inspect the prefix `192.168.101.0/24` (advertised by X2) on X1. It should have the BGP community 65000:200.

```
BGP routing table entry for 192.168.101.0/24
Paths: (1 available, best #1, table default)
  Advertised to non peer-group peers:
  10.1.0.1
  65000 65101
    10.1.0.1 from 10.1.0.1 (10.0.0.1)
      Origin IGP, valid, external, bestpath-from-AS 65000, best (First path received)
      Community: 65000:200
      Last update: Fri Feb  2 09:17:58 2024
```

* Inspect the prefix `192.168.42.0/24` (advertised by RTR) on X1. It should have the BGP community 65000:300.

```
$ netlab connect x1 -q --show ip bgp 192.168.42.0/24
BGP routing table entry for 192.168.42.0/24
Paths: (1 available, best #1, table default)
  Advertised to non peer-group peers:
  10.1.0.1
  65000
    10.1.0.1 from 10.1.0.1 (10.0.0.1)
      Origin incomplete, valid, external, bestpath-from-AS 65000, best (First path received)
      Community: 65000:300
      Last update: Fri Feb  2 09:17:58 2024
```

* On X2, repeat the tests you did on X1.

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and provider routers.
* Git repository contains external router initial device configurations for Cumulus Linux.
<!--
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on X1 and X2. Automated lab validation requires _netlab_ release 1.7.0 or higher.
-->

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | x1 | swp1 |
| rtr | Ethernet2 | x2 | swp1 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  10.0.0.10/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| **x2** |  10.0.0.11/32 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |
