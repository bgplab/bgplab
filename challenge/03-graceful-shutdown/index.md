# BGP Graceful Shutdown

Imagine you have to perform maintenance of the primary uplink of your mission-critical site. You could shut down the link (or power off the router) and wait for a few minutes for the global Internet to adapt to the change[^ES], or you could do the right thing and try to shift the traffic to the backup link before shutting down the primary one.

Shifting the traffic away from a link scheduled for maintenance has two components:

* Telling everyone in your autonomous system not to use the affected link, usually by setting the [BGP local preference](../policy/5-local-preference.md) of all prefixes received over that link to zero.
* Telling the upstream provider not to use the link. [RFC 8326](https://www.rfc-editor.org/rfc/rfc8326.html) defines the recommended tool for the job: the GRACEFUL_SHUTDOWN community.

In this lab exercise, you'll implement the configuration changes needed to support the BGP Graceful Shutdown functionality on a customer and a provider router and test the graceful shutdown procedure.

![Lab topology](topology-graceful-shutdown.png)

[^ES]: While enjoying listening to the sounds of a million alerts and the screaming VP of Marketing.

!!! Expert
    We expect you to have completed most of the foundational labs and know what you're doing. The lab instructions contain only high-level guidelines.

## Existing Router Configurations

The routers in your lab use the following BGP AS numbers. Each router advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| c1 | 10.0.0.1 | 10.0.0.1/32 |
| c2 | 10.0.0.2 | 10.0.0.2/32 |
| **AS65100** ||
| x1 | 10.0.0.10 | 10.0.0.10/32 |
| x2 | 10.0.0.11 | 10.0.0.11/32 |

The routers you're configuring have these BGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **c1** | 10.0.0.1 | 65000 |
| | c2 | 65000 | 10.0.0.2 |
| | x1 | 65100 | 10.1.0.14 |
| **x1** | 10.0.0.10 | 65100 |
| | x2 | 65100 | 10.0.0.11 |
| | c1 | 65000 | 10.1.0.13 |

The routers you're configuring run OSPF in the backbone area with the other routers in the same autonomous system:

| Router | OSPF<br>Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| c1 | Loopback | 10.0.0.1/32 | |
|  | Ethernet1 | 10.1.0.1/30 | c2 |
| c2 | Loopback | 10.0.0.2/32 | |
|  | swp1 | 10.1.0.2/30 | c1 |
| x1 | Loopback | 10.0.0.10/32 | |
|  | Ethernet2 | 10.1.0.9/30 | x2 |
| x2 | Loopback | 10.0.0.11/32 | |
|  | swp3 | 10.1.0.10/30 | x1 |

_netlab_ automatically configures all lab devices; if you're using another lab infrastructure, you'll have to manually configure C1 and X1.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `challenge/03-graceful-shutdown`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your routers with **netlab connect** and verify that their IP addresses and routing protocols are properly configured.

## The Problem

Log into C1 and X1 and check their BGP tables. Assuming your devices use the default local preference value of 100, they should not use any inter-AS routes propagated by C2 or X2. This is the printout you would get on C1 running Arista EOS:

```
$ netlab connect c1 --show ip bgp
Connecting to clab-gshut-c1 using SSH port 22, executing show ip bgp
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
 * >      10.0.0.2/32            10.0.0.2              0       -          100     0       i
 * >      10.0.0.10/32           10.1.0.14             0       -          100     0       65100 i
 * >      10.0.0.11/32           10.1.0.14             0       -          100     0       65100 i
```

On the other hand, C2 and X2 prefer IBGP routes advertised by C1 and X1. This is the printout you would get on C2 running Cumulus Linux:

```
$ netlab connect c2 --show ip bgp
Connecting to container clab-gshut-c2, executing sudo vtysh -c "show ip bgp"
BGP table version is 6, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*>i10.0.0.1/32      10.0.0.1                      100      0 i
*> 10.0.0.2/32      0.0.0.0                  0         32768 i
*  10.0.0.10/32     10.1.0.6                       50      0 65100 i
*>i                 10.0.0.1                      100      0 65100 i
*>i10.0.0.11/32     10.0.0.1                      100      0 65100 i
*                   10.1.0.6                 0     50      0 65100 i

Displayed  4 routes and 6 total paths
```

Shutting down the C1-X1 link would cause a lab-wide outage until the BGP session between C1 and X1 is brought down and the routers update their BGP tables. As you're not using [BFD or reduced BGP timers](../basic/7-bfd.md), it could take up to three minutes for the network to converge.

## Configuration Tasks

[RFC 8326](https://www.rfc-editor.org/rfc/rfc8326.html) defines the Graceful Shutdown BGP community that you can use to drain traffic from a link before it's brought down for maintenance. The routers using the procedures from that RFC should set BGP Local Preference of prefixes carrying the GRACEFUL_SHUTDOWN community to *a low value*

Some vendors (for example, Arista) recognize the GRACEFUL_SHUTDOWN community without extra configuration and set BGP Local Preference to zero. On other devices, you have to create:

* Configure a route map on X1 that matches the GRACEFUL_SHUTDOWN community and sets BGP Local Preference as low as possible.
* Apply the route map to all EBGP sessions.

Before starting the maintenance process, the customer router (C1) has to:

* Set the GRACEFUL_SHUTDOWN community on all EBGP updates
* Set the local preference on all incoming EBGP updates to as low as possible. 

Some vendors (for example, Arista) implemented *BGP maintenance mode* that performs those tasks automatically. On other devices, you have to:

* Configure an outbound route map that sets the GRACEFUL_SHUTDOWN community
* Configure an inbound route map that sets the BGP local preference to zero
* Before shutting down the C1-X1 link, apply both route maps to the EBGP session with X1.

!!! tip
    You'll find more details in these lab exercises:
    
    *  [Attach BGP Communities to Outgoing BGP Updates](../policy/8-community-attach.md) lab exercise.
    * [Select Preferred Uplink with BGP Local Preference](../policy/5-local-preference.md)
    * [Use BGP Communities in Routing Policies](../policy/9-community-use.md)

## Verification

After configuring and applying route maps on C1 and X1, the BGP table on C1 should contain routes advertised by X1 (with local preference set to a very low value) and those advertised by C2 (with higher local preference). C1 should prefer the routes to AS 65100 advertised by C2:

```
c1>show ip bgp
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
 * >      10.0.0.2/32            10.0.0.2              0       -          100     0       i
 * >      10.0.0.10/32           10.0.0.2              0       -          50      0       65100 i
 *        10.0.0.10/32           10.1.0.14             0       -          0       0       65100 i
 * >      10.0.0.11/32           10.0.0.2              0       -          50      0       65100 i
 *        10.0.0.11/32           10.1.0.14             0       -          0       0       65100 i
```

Similarly, X1 should prefer routes to AS 65100 advertised by X2:

```
x1>show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.10, local AS number 65100
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            10.0.0.11             0       -          50      0       65000 i
 *        10.0.0.1/32            10.1.0.13             0       -          0       0       65000 i
 * >      10.0.0.2/32            10.0.0.11             0       -          50      0       65000 i
 *        10.0.0.2/32            10.1.0.13             0       -          0       0       65000 i
 * >      10.0.0.10/32           -                     -       -          -       0       i
 * >      10.0.0.11/32           10.0.0.11             0       -          100     0       i
```

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP and OSPF configuration module](https://netlab.tools/platforms/#platform-routing-support) for the C1 and X1.
* Use devices [supported by the _netlab_ **bgp.policy** plugin](https://netlab.tools/plugins/bgp.policy/#platform-support) for C2 and X2.
* Git repository contains external router initial device configurations for Cumulus Linux.
<!--
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on X1 and X2. Automated lab validation requires _netlab_ release 1.7.0 or higher.
-->

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
| Intra-customer link | c1 | Ethernet1 | c2 | swp1 |
| Unused link | c1 | Ethernet2 | x2 | swp1 |
| C2 uplink | c2 | swp2 | x2 | swp2 |
| Unused link | x1 | Ethernet1 | c2 | swp3 |
| Intra-ISP link | x1 | Ethernet2 | x2 | swp3 |
| C1 uplink | c1 | Ethernet3 | x1 | Ethernet3 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **c1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | Intra-customer link |
| Ethernet2 |  |  | Unused link |
| Ethernet3 | 10.1.0.13/30 |  | C1 uplink |
| **c2** |  10.0.0.2/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | Intra-customer link |
| swp2 | 10.1.0.5/30 |  | C2 uplink |
| swp3 |  |  | Unused link |
| **x1** |  10.0.0.10/32 |  | Loopback |
| Ethernet1 |  |  | Unused link |
| Ethernet2 | 10.1.0.9/30 |  | Intra-ISP link |
| Ethernet3 | 10.1.0.14/30 |  | C1 uplink |
| **x2** |  10.0.0.11/32 |  | Loopback |
| swp1 |  |  | Unused link |
| swp2 | 10.1.0.6/30 |  | C2 uplink |
| swp3 | 10.1.0.10/30 |  | Intra-ISP link |
