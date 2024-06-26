# Resolve BGP Wedgies

In the [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md) exercise, you've learned how to use BGP communities to tell Internet Service Providers to reduce BGP local preference on their end because you want to use a connection as a backup link.

Even that's not enough in larger environments, as the global BGP routing system might have more than one stable state, and it might be hard to push the system from the current stable state into the one you prefer. [RFC 4264](https://datatracker.ietf.org/doc/html/rfc4264) lovingly calls the unintended stable BGP states *BGP Wedgies*; you'll explore- and fix them in this lab exercise that uses a pretty standard two-tier ISP topology:

![Lab topology](topology-wedgies.png)

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. C1, P1, and P2 advertise an IPv4 prefix.

## BGP AS Numbers

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| c1 | 10.0.0.1 | 192.168.42.0/24 |
| **AS65101** ||
| u1 | 10.0.0.4 |  |
| **AS65102** ||
| u2 | 10.0.0.5 |  |
| **AS65207** ||
| p1 | 172.17.207.1 | 172.17.207.0/24 |
| **AS65304** ||
| p2 | 172.23.4.1 | 172.23.4.0/24 |

Your router has these EBGP neighbors.  _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **c1** | 10.0.0.1 | 65000 |
| | p1 | 65207 | 10.1.0.2 |
| | p2 | 65304 | 10.1.0.6 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/e-wedgies`
* Execute **netlab up** ([device requirements](#req))
* Log into your router (RTR) with **netlab connect c1** and verify that the IP addresses and the EBGP sessions are properly configured.

!!! warning
    The `netlab connect --show` command used in the verification section was introduced in _netlab_ release 1.7.0. Automated lab validation requires _netlab_ release 1.8.3.

## The Problem

Without additional BGP policy configuration, the P2 (upstream ISP) router prefers the direct connection to reach the customer prefix 192.168.42.0/24:

```
$ netlab connect -q p2 --show ip bgp
BGP table version is 6, local router ID is 172.23.4.1, vrf id 0
Default local pref 100, local AS 65304
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.1/32      10.1.0.5                      200      0 65000 i
*> 172.17.207.0/24  10.1.0.14                              0 65102 65101 65207 i
*> 172.23.4.0/24    0.0.0.0                  0         32768 i
*> 192.168.42.0/24  10.1.0.5                      200      0 65000 ?
```

You could try using the AS path prepending to make P2 prefer the alternate path (going through U2, U1, and P1) with a longer AS path, but that wouldn't work. P2 always prefers customer paths over upstream paths and sets a high local preference for paths received from its customers. If you inspect the BGP information for the customer prefix on P2, you'll notice that the local preference is higher than the default 100.

```
$ netlab connect -q p2 --show ip bgp 192.168.42.0
BGP routing table entry for 192.168.42.0/24
Paths: (1 available, best #1, table default)
  Advertised to non peer-group peers:
  10.1.0.5 u2(10.1.0.14)
  65000
    10.1.0.5 from 10.1.0.5 (10.0.0.1)
      Origin incomplete, localpref 200, valid, external, bestpath-from-AS 65000, best (First path received)
      Last update: Mon Jun 24 11:35:05 2024
```

Fortunately, the P2 ISP implemented a BGP community scheme (described in the [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md) lab exercise) that allows you to tell P2 to lower the local preference of your prefix to 50 by attaching BGP community 65304:100 to BGP paths sent in EBGP updates to P2.

## Change BGP Local Preference on P2

* Attach the BGP community 65304:100 to all EBGP updates sent from C1 to P2 using the configuration mechanisms you mastered in the [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md) lab exercise.
* Execute **show ip bgp** (or similar) command on P2 to confirm the change in BGP local preference. You can also [use the **netlab validate** command](#validate).

## Setting BGP Community Is Not Enough

Even after P2 lowers the local preference of the 192.168.42.0/24 prefix, it does not receive an alternate path (via P1, U1, and U2) because U2 prefers the path through P2 due to its shorter AS path; we're dealing with a BGP wedgie.

You can verify that with the **show ip bgp 192.168.42.0/24** (or similar) command executed on U2 (you can also [use the **netlab validate** command](#validate)):

```
$ netlab connect -q u2 --show ip bgp 192.168.42.0
BGP routing table entry for 192.168.42.0/24
Paths: (2 available, best #2, table default)
  Advertised to non peer-group peers:
  p2(10.1.0.13) u1(10.1.0.17)
  65101 65207 65000
    10.1.0.17 from u1(10.1.0.17) (10.0.0.4)
      Origin incomplete, valid, external, bestpath-from-AS 65101
      Last update: Mon Jun 24 11:35:01 2024
  65304 65000
    10.1.0.13 from p2(10.1.0.13) (172.23.4.1)
      Origin incomplete, valid, external, bestpath-from-AS 65304, best (AS Path)
      Community: 65304:100
      Last update: Mon Jun 24 11:54:14 2024
```

Even though you can observe the BGP community 65304:100 attached to the BGP path for 192.168.42.0/24 on U2, U2 does not recognize the community, ignores it, and uses AS-path length as the path selection criterion.

Let's see if we're dealing with a true BGP wedgie:

* Clear the BGP session between C1 and P2. P2 will send an "_I lost the prefix_" update to U2. U2 will select an alternate route and send it to P2. When P2 receives the route from the customer, it will already have an alternate route with a better local preference. The traffic from P2 to C1 will go over U2, U1, and P1.
* Clear the BGP session between C1 and P1. P1 will send an "_I lost the prefix_" update to U1, U1 will propagate it to U2, and U2 will send it to P2. P2 will have a single path to 192.168.42.0/24 left and will advertise it to U2, flipping the routing system back into the undesired stable state.

## Increase the AS Path Length

In real life, you could figure out what BGP community to use to influence the BGP best path selection process on U2; we'll use a brute-force approach and prepend a few AS numbers to the AS path C1 advertises to P2.

Prepend at least three copies of your AS number (65000) to the EBGP updates C1 sends to P2. Use the configuration mechanisms you mastered in the [Use AS-Path Prepending to Influence Incoming Traffic Flow](7-prepend.md) lab exercise.

## Verification {#validate}

You can use the **netlab validate** command if you've installed *netlab* release 1.8.3 or later and use Cumulus Linux, FRR, or Arista EOS on the external routers. The validation tests check:

* The state of the EBGP session between C1 and P1/P2
* Whether C1 advertises its prefix to P1/P2 and whether that gets propagated to U1/U2.
* The community attached to the EBGP updates C1 sends to P2.
* Whether the next hop of the best path toward 192.168.42.0/24 on U2 points to U1.

![](policy-wedgies-validate.png)

If the **netlab validate** command fails or you're using another network operating system on the ISP routers:

* Check the BGP prefix advertised by C1 on P2 with a command similar to **show ip bgp 192.168.42.0/24**. The prefix advertised by C1 should have a long AS path, BGP community 65304:100, and local preference set to 50.

```
$ netlab connect -q p2 --show ip bgp 192.168.42.0
BGP routing table entry for 192.168.42.0/24
Paths: (2 available, best #1, table default)
  Advertised to non peer-group peers:
  10.1.0.5 u2(10.1.0.14)
  65102 65101 65207 65000
    10.1.0.14 from u2(10.1.0.14) (10.0.0.5)
      Origin incomplete, valid, external, bestpath-from-AS 65102, best (Local Pref)
      Last update: Mon Jun 24 11:59:55 2024
  65000 65000 65000 65000 65000 65000 65000 65000
    10.1.0.5 from 10.1.0.5 (10.0.0.1)
      Origin incomplete, localpref 50, valid, external, bestpath-from-AS 65000
      Community: 65304:100
      Last update: Mon Jun 24 11:59:55 2024
```

* Check the same prefix on U2. There should be a single BGP path for that prefix in the U2 BGP table, and it should be advertised by U1:

```
$ netlab connect -q u2 --show ip bgp 192.168.42.0
BGP routing table entry for 192.168.42.0/24
Paths: (1 available, best #1, table default)
  Advertised to non peer-group peers:
  p2(10.1.0.13) u1(10.1.0.17)
  65101 65207 65000
    10.1.0.17 from u1(10.1.0.17) (10.0.0.4)
      Origin incomplete, valid, external, bestpath-from-AS 65101, best (First path received)
      Last update: Mon Jun 24 11:35:00 2024
```

**Next:** 

* [Use Disaggregated Prefixes to Select the Primary Link](../policy/b-disaggregate.md)

## Reference Information

The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for C1, P1, U1, and U2.
* P2 requires additional configuration that sets BGP local preference based on BGP communities. The lab exercise includes configuration templates for Arista EOS, Cumulus Linux, and FRR. If you decide to use any other device for P2, you'll have to configure it manually.
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on P1, P2, U1, and U2. Automated lab validation requires _netlab_ release 1.8.3 or higher.
* Git repository contains initial device configurations for Cumulus Linux.

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
| Primary uplink | c1 | Ethernet1 | p1 | swp1 |
| Backup uplink | c1 | Ethernet2 | p2 | swp1 |
| P1 uplink | p1 | swp2 | u1 | swp1 |
| P2 uplink | p2 | swp2 | u2 | swp1 |
| Upstream peering link | u1 | swp2 | u2 | swp2 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **c1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | Primary uplink |
| Ethernet2 | 10.1.0.5/30 |  | Backup uplink |
| **p1** |  172.17.207.1/24 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | Primary uplink |
| swp2 | 10.1.0.9/30 |  | P1 uplink |
| **p2** |  172.23.4.1/24 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | Backup uplink |
| swp2 | 10.1.0.13/30 |  | P2 uplink |
| **u1** |  10.0.0.4/32 |  | Loopback |
| swp1 | 10.1.0.10/30 |  | P1 uplink |
| swp2 | 10.1.0.17/30 |  | Upstream peering link |
| **u2** |  10.0.0.5/32 |  | Loopback |
| swp1 | 10.1.0.14/30 |  | P2 uplink |
| swp2 | 10.1.0.18/30 |  | Upstream peering link |
