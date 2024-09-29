# Filter Advertised Prefixes

In the previous lab exercise, you [filtered prefixes advertised by your router based on the AS-path contents](2-stop-transit.md). That's the absolute minimum you should do, but it's not always enough. Every other blue moon, a network operator manages to mess up two-way redistribution and advertises hundreds of thousands of prefixes as belonging to their autonomous system. You should, therefore, filter the prefixes advertised to EBGP neighbors to ensure you advertise only the address space assigned to you.

In our simple lab topology, your device advertises a /24 prefix (that we'll assume is assigned to you) and a loopback (/32) prefix that should not be visible elsewhere.

![Lab topology](topology-prefix-filter.png)

You don't have to trust me -- after starting the lab, execute the `netlab connect --show ip bgp 65000$` command ([more details](../basic/0-frrouting.md#vtysh)) or an equivalent command for the device you use as the external router. You'll see that your autonomous system advertises two prefixes; this is what I got in my lab:

```
BGP table version is 6, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*  10.0.0.1/32      10.1.0.10                              0 65101 65000 i
*>                  10.1.0.1                               0 65000 i
*  192.168.42.0/24  10.1.0.10                              0 65101 65000 ?
*>                  10.1.0.1                               0 65000 ?
```

!!! tip
    You could also use a command similar to **show ip bgp show ip bgp neighbors _neighbor-ip_ advertised-routes** if it's available on your device to check what you're advertising to an individual neighbor.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each autonomous system advertises one loopback address and another IPv4 prefix. Upstream routers (x1, x2) also advertise the default route to your router (rtr).

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 192.168.42.0/24<br>10.0.0.1/32 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.0/24 |

Your router has these EBGP neighbors. _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Neighbor | Neighbor IPv4 | Neighbor AS |
|----------|--------------:|------------:|
| x1 | 10.1.0.2 | 65100 |
| x2 | 10.1.0.6 | 65101 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/3-prefix`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your device (RTR) with **netlab connect rtr** and verify IP addresses and BGP configuration.

**Note:** *netlab* will configure IP addressing, EBGP sessions, and BGP prefix advertisements on your router. If you're not using *netlab*, continue with the configuration you made during the [previous exercise](2-stop-transit.md).

## Configuration Tasks

You must filter BGP prefixes sent to X1 and X2 and advertise only the 192.168.42.0/24 prefix. Most BGP implementations support *prefix lists* that match IP prefixes and subnet masks; you should match both to ensure you're not advertising more specific prefixes to your EBGP neighbors.

On some BGP implementations (for example, Cisco IOS and IOS XE, Cumulus Linux, FRR, Arista EOS), you can apply a *prefix list* as an inbound or outbound filter on a BGP neighbor. 

Some other implementations (for example, Arista EOS) might require a more convoluted approach using a *route map* as an intermediate step:

* After configuring the *prefix list*, create a *route map* that permits BGP prefixes matching your *prefix list*.
* Apply that route map as an outbound filter to all EBGP neighbors.

!!! Warning
    Applying filters to BGP neighbors doesn't necessarily trigger new updates -- you might have to use a command similar to `clear ip bgp * soft out` to tell your router to recalculate and resend BGP prefixes from its BGP table to its neighbors.

## Verification

You can use the **netlab validate** command if you've installed *netlab* release 1.8.3 or later and use Cumulus Linux, FRR, or Arista EOS on X1 and X2. The validation tests check:

* The state of the EBGP session between RTR and X1/X2.
* Whether RTR advertises the expected IPv4 prefix (192.168.42.0/24).
* Whether RTR advertises its loopback IPv4 prefix (it should not). This is the printout you could get when trying to validate an incomplete solution:

![](policy-prefix-validate.png)

You can also examine the BGP table on X1 and X2 to verify that your router advertises only a single IPv4 prefix. This is the printout you should get on X1:

```
$ netlab connect --show ip bgp neighbor 10.1.0.1 routes
BGP table version is 8, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 192.168.42.0/24  10.1.0.1                               0 65000 ?
```

You can also check routes advertised to a neighbor on your device if it supports a command similar to **show ip bgp show ip bgp neighbors _neighbor-ip_ advertised-routes**. This is how the printout looks on Arista EOS:

```
rtr>show ip bgp neighbors 10.1.0.2 advertised-routes
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast, q - Queued for advertisement
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      192.168.42.0/24        10.1.0.1              -       -          -       -       65000 ?
```
 
**Next**: [Reduce the size of your BGP table](4-reduce.md) with inbound filters

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Customer router: use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support).
* External routers need support for [default route origination](https://netlab.tools/plugins/bgp.session/#platform-support) and [change of BGP local preference](https://netlab.tools/plugins/bgp.policy/#platform-support). If you want to use an unsupported device as an external router, remove the **bgp.originate** and **bgp.locpref** attributes from the lab topology.
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on external routers. Automated lab validation requires _netlab_ release 1.8.3 or higher.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

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
| **x1** |  192.168.100.1/24 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| swp2 | 10.1.0.9/30 |  | x1 -> x2 |
| **x2** |  192.168.101.1/24 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |
| swp2 | 10.1.0.10/30 |  | x2 -> x1 |
