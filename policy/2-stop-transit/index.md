# Filter Transit Routes

In the previous lab exercises you [configured EBGP sessions](../basic/2-multihomed.md) with two routers belonging to upstream ISPs.

![Lab topology](topology-stop-transit.png)

With no additional configuration, BGP routers propagate every route known to them to all neighbors, which means that your device propagates routes between AS 65100 and AS 65101[^EF]. That wouldn't be so bad if the ISP-2 wouldn't prefer customer routes over peer routes. Well, it does, and you became a transit network between ISP-2 and ISP-1.

You don't have to trust me -- log into X2 and execute `sudo vtysh -c 'show ip bgp'` command[^VT]. You'll see that the best paths to AS 65100 (ISP-1) go through AS 65000 (your network).

[^EF]: Devices [strictly compliant with RFC 8212](https://blog.ipspace.net/2023/06/default-ebgp-policy-rfc-8212.html) are an exception -- they won't advertise anything to their EBGP neighbors unless you configured an outbound filter.

[^VT]: **sudo** to make sure you're an admin user, **vtysh** is the name of the FRR CLI shell, and the `-c` argument passes the following argument to **vtysh** so you don't have to type another line.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each autonomous system advertises one loopback address and another IPv4 prefix. Upstream routers (x1, x2) also advertise the default route to your router (rtr).

| Node/ASN | Router ID | BGP RR | Advertised prefixes |
|----------|----------:|--------|--------------------:|
| AS65000 |||
| rtr | 10.0.0.1 |  | 10.0.0.1/32<br>192.168.42.0/24 |
| AS65100 |||
| x1 | 10.0.0.10 |  | 10.0.0.10/32<br>192.168.100.0/24 |
| AS65101 |||
| x2 | 10.0.0.11 |  | 10.0.0.11/32<br>192.168.101.0/24 |

Your device (rtr) has these EBGP neighbors:

| Neighbor | Neighbor IPv4 | Neighbor AS |
|----------|--------------:|------------:|
| x1 | 10.1.0.2 | 65100 |
| x2 | 10.1.0.6 | 65101 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/2-stop-transit`
* Execute **netlab up** ([other options](../2-manual.md))
* Log into your device (RTR) with **netlab connect rtr** and verify IP addresses and BGP configuration.

**Note:** *netlab* will configure IP addressing, EBGP sessions, and BGP prefix advertisements on your router. If you're not using *netlab* just continue with the configuration you made during the [previous exercise](1-weights.md).

## Configuration Tasks

You have to filter BGP prefixes sent to X1 and X2, and advertise only prefixes with an empty AS path -- the prefixes originating in your autonomous system[^FT].

[^FT]: Please note that all BGP implementations I've seen so far apply filters to the contents of the BGP table. Prefixes originated by your router have an empty AS path while they're in the BGP table of your router.

On some BGP implementations (example: Cisco IOS and IOS XE, Cumulus Linux, FRR) you configure outbound AS-path filters in two steps:

* Configure an AS-path access list that matches an empty AS path[^RE].
* Apply the AS-path access list as an outbound filter to all EBGP neighbors.

[^RE]: I don't want you to waste too much time on regular expressions, so here's a hint: you can usually use `^$` to match an empty AS-path.

Some other implementations (example: Arista EOS) might require a more convoluted approach using a *route map* as an intermediate step:

* After configuring the AS-path access list, create a *route map* that permits BGP prefixes matching your AS-path access list.
* Apply that route map as an outbound filter to all EBGP neighbors.

Please note that applying filters to BGP neighbors doesn't necessarily trigger new updates -- you might have to use a command similar to `clear ip bgp * soft out` to tell your router to recalculate and resend BGP prefixes from its BGP table to its neighbors.

## Verification

Examine the BGP table on X1 and X2 to verify that your router advertises only routes from AS 65000. This is the printout you should get on X1:

```
$ sudo vtysh -c 'show ip bgp'
BGP table version is 6, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*  10.0.0.1/32      10.1.0.10                              0 65101 65000 i
*>                  10.1.0.1                               0 65000 i
*> 10.0.0.10/32     0.0.0.0                  0         32768 i
*> 10.0.0.11/32     10.1.0.10                0             0 65101 i
*  192.168.42.0/24  10.1.0.10                              0 65101 65000 ?
*>                  10.1.0.1                               0 65000 ?
*> 192.168.100.0/24 0.0.0.0                  0         32768 i
*> 192.168.101.0/24 10.1.0.10                0             0 65101 i

Displayed  6 routes and 8 total paths
```

**Next**: [Filter prefixes advertised to EBGP neighbors](3-prefix.md)

## Reference Information

You might find the following information useful if you're not using _netlab_ to build the lab:

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
|  | rtr | Ethernet1 | x1 | swp1 |
|  | rtr | Ethernet2 | x2 | swp1 |
|  | x1 | swp2 | x2 | swp2 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  10.0.0.10/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| swp2 | 10.1.0.9/30 |  | x1 -> x2 |
| **x2** |  10.0.0.11/32 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |
| swp2 | 10.1.0.10/30 |  | x2 -> x1 |
