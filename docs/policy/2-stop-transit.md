# Filter Transit Routes

In the previous lab exercises, you [configured EBGP sessions](../basic/2-multihomed.md) with two routers belonging to upstream ISPs.

![Lab topology](topology-stop-transit.png)

With no additional configuration, BGP routers propagate every route known to them to all neighbors, which means that your device propagates routes between AS 65100 and AS 65101[^EF]. That wouldn't be so bad if the ISP-2 wouldn't prefer customer routes over peer routes. Well, it does, and you became a transit network between ISP-2 and ISP-1.

You don't have to trust me. After starting the lab, log into X2. If you're running Cumulus Linux, execute `netlab connect x2 --show ip bgp` ([more details](../basic/0-frrouting.md#vtysh)) or an equivalent command for the device you use as the external router. You'll see that the best paths to AS 65100 (ISP-1) use next hop 10.1.0.5 and go through AS 65000 (your network).

```
$ netlab connect x2 --show ip bgp
Connecting to container clab-no_transit-x2, executing sudo vtysh -c "show ip bgp"
Use vtysh to connect to FRR daemon

BGP table version is 9, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 0.0.0.0/0        10.1.0.5                      200      0 65000 65100 i
*  192.168.42.0/24  10.1.0.9                               0 65100 65000 ?
*>                  10.1.0.5                      200      0 65000 ?
*  192.168.100.0/24 10.1.0.9                 0             0 65100 i
*>                  10.1.0.5                      200      0 65000 65100 i
*> 192.168.101.0/24 0.0.0.0                  0         32768 i

Displayed  4 routes and 6 total paths
```

!!! Tip
    Did you notice that the Internet Service Provider (X2) accepted the default route from its customer? That's a serious security breach and should never happen in a real-life network, but I wouldn't be too sure about that...

[^EF]: Devices [strictly compliant with RFC 8212](https://blog.ipspace.net/2023/06/default-ebgp-policy-rfc-8212.html) are an exception -- they won't advertise anything to their EBGP neighbors unless you configured an outbound filter.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each autonomous system advertises an IPv4 prefix. Upstream routers (x1, x2) also advertise the default route to your router (rtr).

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 192.168.42.0/24 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.0/24 |

Your router has these EBGP neighbors. _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually. You can also use the configuration you made in the [previous exercise](1-weights.md).

| Neighbor | Neighbor IPv4 | Neighbor AS |
|----------|--------------:|------------:|
| x1 | 10.1.0.2 | 65100 |
| x2 | 10.1.0.6 | 65101 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/2-stop-transit`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your device (RTR) with **netlab connect rtr** and verify IP addresses and BGP configuration.

**Note:** *netlab* will configure IP addressing, EBGP sessions, and BGP prefix advertisements on your router. If you're not using *netlab*, continue with the configuration you made during the [previous exercise](1-weights.md).

## Configuration Tasks

You must filter BGP prefixes sent to X1 and X2 and advertise only prefixes with an empty AS path -- the prefixes originating in your autonomous system[^FT].

[^FT]: Please note that all BGP implementations I've seen so far apply filters to the contents of the BGP table. Prefixes originated by your router have an empty AS path while in your router's BGP table.

On some BGP implementations (for example, Cisco IOS and IOS XE, Cumulus Linux, FRR), you configure outbound AS-path filters in two steps:

* Configure an AS-path access list that matches an empty AS path[^RE].
* Apply the AS-path access list as an outbound filter to all EBGP neighbors.

[^RE]: I don't want you to waste too much time on regular expressions, so here's a hint: you can usually use `^$` to match an empty AS-path.

Some other implementations (for example, Arista EOS) might require a more convoluted approach using a *route map* as an intermediate step:

* After configuring the AS-path access list, create a *route map* that permits BGP prefixes matching your AS-path access list.
* Apply that route map as an outbound filter to all EBGP neighbors.

!!! Warning
    Applying filters to BGP neighbors doesn't necessarily trigger new updates -- you might have to use a command similar to `clear ip bgp * soft out` to tell your router to recalculate and resend BGP prefixes from its BGP table to its neighbors.

## Verification

You can use the **netlab validate** command if you've installed *netlab* release 1.8.3 or later and use Cumulus Linux, FRR, or Arista EOS on X1 and X2. The validation tests check:

* The state of the EBGP session between RTR and X1/X2.
* Whether RTR advertises the expected IPv4 prefix (192.168.42.0/24).
* Whether RTR propagates BGP prefixes between X1 and X2 (it should not). This is the printout you could get when trying to validate an incomplete solution:

![](policy-stop-transit-validate.png)

You can also examine the BGP table on X1 and X2 to verify that RTR advertises only routes from AS 65000. This is the printout you should get on X2:

```
$ netlab connect x2 --show ip bgp
Connecting to container clab-no_transit-x2, executing sudo vtysh -c "show ip bgp"
Use vtysh to connect to FRR daemon

BGP table version is 11, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*  192.168.42.0/24  10.1.0.9                               0 65100 65000 ?
*>                  10.1.0.5                      200      0 65000 ?
*> 192.168.100.0/24 10.1.0.9                 0             0 65100 i
*> 192.168.101.0/24 0.0.0.0                  0         32768 i

Displayed  3 routes and 4 total paths
```

**Next**: [Filter prefixes advertised to EBGP neighbors](3-prefix.md)

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
