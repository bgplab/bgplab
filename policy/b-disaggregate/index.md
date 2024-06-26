# Use Disaggregated Prefixes to Select the Primary Link

Previous lab exercises in the *[‌Influencing Incoming (Ingress) Traffic Flow](index.md#ingress)* part of the *[BGP Routing Policies](index.md)* section described various mechanisms you can use to try to influence the inbound traffic flow. None of these tools work when dealing with "suboptimal" ISPs; in those rare moments, you'll have to use a bigger hammer.

Unfortunately, one scenario often used in the global Internet is prefix disaggregation: a customer owning address space larger than the minimum prefix size accepted in the public Internet can advertise the summary prefix over the backup link and two more specific prefixes over the primary link. That's what you'll practice in this lab exercise.

![Lab topology](topology-disaggregate.png)

!!! Warning
    Prefix disaggregation should be the tool of last resort as it pollutes the routing tables throughout the Internet. Do not use it unless all the other tools have failed.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each router router advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 172.16.4.0/22 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.0/24 |

Your router has these EBGP neighbors.  _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **rtr** | 10.0.0.1 | 65000 |
| | x1 | 65100 | 10.1.0.2 |
| | x2 | 65101 | 10.1.0.6 |


## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/b-disaggregate`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

## The Problem

You would like to use the link between RTR and X2 as a backup link; X2 should send the traffic toward 172.16.4.0/22 via X1. 

Unfortunately, the X2 ISP does not offer flexible BGP routing policies like BGP communities. It uses BGP local preference to prefer customer routes over peer routes; there's nothing you can do to change that.

Don't believe me? Execute **show ip bgp 172.16.4.0/22** (or a similar command) on X2 to inspect the alternate paths for your prefix; the best path points to the RTR-X2 link. Using [AS-path prepending](7-prepend.md) won't change that (you might want to check that claim before proceeding):

```
$ netlab connect -q x2 --show ip bgp 172.16.4.0/22
BGP routing table entry for 172.16.4.0/22
Paths: (2 available, best #2, table default)
  Advertised to non peer-group peers:
  10.1.0.5 x1(10.1.0.9)
  65100 65000
    10.1.0.9 from x1(10.1.0.9) (10.0.0.10)
      Origin incomplete, valid, external, bestpath-from-AS 65100
      Last update: Tue Jun 25 17:12:20 2024
  65000
    10.1.0.5 from 10.1.0.5 (10.0.0.1)
      Origin incomplete, localpref 200, valid, external, bestpath-from-AS 65000, best (Local Pref)
      Last update: Tue Jun 25 17:12:25 2024
```

The only way to force X2 to use the path through X1 is to advertise two prefixes (172.16.4.0/23 and 172.16.6.0/23) to X1 while advertising just the summary prefix (172.16.4.0/22) to X2.

## Advertise Disaggregated Prefixes

You mastered all the tools you need to solve this challenge in the previous lab exercises:

* Start advertising the two more specific prefixes (see [Advertise IPv4 Prefixes to BGP Neighbors](../basic/3-originate.md) for more details).
* Configure two outbound prefix lists, one that matches only the more specific prefixes and another that only matches the aggregate prefixes. Apply them as outbound filters on EBGP sessions with X1 and X2 (see [Filter Advertised Prefixes](3-prefix.md) for more details).

## Verification

After completing the lab exercise, your router should:

* Advertise 172.16.4.0/23 and 172.16.6.0/23 (and nothing else) to X1
* Advertise 172.16.4.0/22 to X2

X2 should use the path through X1 to reach the 172.16.4.0/22 address space.

You can use the **netlab validate** command if you've installed *netlab* release 1.7.0 or later and use Cumulus Linux, FRR, or Arista EOS on the external routers. The validation tests check:

* The state of the EBGP session between RTR and X1/X2
* The prefixes RTR advertises to X1/X2
* Whether X2 uses X1 to get to the 172.16.4.0/22 address space.

For example, this is the result you'd get if you configured the prefix origination but forgot to apply prefix filters to outbound EBGP updates (the printout shows just the final tests):

![](policy-disaggregate-validate.png)

If the **netlab validate** command fails or you're using another network operating system on the ISP routers, do manual validation. Inspect the state of the BGP table on X1 and X2 (use a command similar to **show ip bgp regex 65000$** to limit the printout to prefixes originated by AS 65000) and check whether it matches the expected results.

This is the BGP table you should see on X1:

```
$ netlab connect -q x1 --show 'ip bgp regex 65000$'
BGP table version is 12, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 172.16.4.0/22    10.1.0.10                              0 65101 65000 ?
*> 172.16.4.0/23    10.1.0.1                               0 65000 ?
*> 172.16.6.0/23    10.1.0.1                               0 65000 ?

Displayed  3 routes and 5 total paths
```

And this is the BGP table you should see on X2:

```
$ netlab connect -q x2 --show 'ip bgp regex 65000$'
BGP table version is 12, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 172.16.4.0/22    10.1.0.5                      200      0 65000 ?
*> 172.16.4.0/23    10.1.0.9                               0 65100 65000 ?
*> 172.16.6.0/23    10.1.0.9                               0 65100 65000 ?

Displayed  3 routes and 5 total paths
```

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer routers.
* Use any device on which [_netlab_ can configure BGP local preference](https://netlab.tools/plugins/bgp.policy/#platform-support) for the provider routers.
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on X1 and X2. Automated lab validation requires _netlab_ release 1.7.0 or higher.
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
