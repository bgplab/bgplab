# Merge Networks Using Different BGP AS Numbers

When dealing with the networking aspects of mergers and acquisitions, you might encounter a scenario in which you'll have to merge two networks running BGP:

* Two organizations (ORG-1 and ORG-2) have built large BGP networks. Each one is using a different BGP AS number.
* ORG-1 is running OSPF, ORG-2 is running IS-IS as their IGP.
* The first physical link between the two networks (PE2-PE3) has been delivered. You decided to use the IPv4 prefix 172.29.42.0/24 on that link.

Now, you have to connect the two networks with a minimum disruption of existing network operations:

* The only change you can make is a new BGP session between PE2 and PE3.
* Do not advertise the interconnect prefix (172.29.42.0/24) into either IGP.

[![Lab topology](topology-merge-as.png)](topology-merge-as.png)

!!! Tip
    You can change other aspects of device configuration on PE2 and PE3; for example, you'll have to assign IP addresses to the network interconnect. You cannot change configurations on other routers or redesign the routing protocols (even though that would be the best way to proceed).

At the end of the migration project:

* ORG-1 and ORG-2 must announce all BGP prefixes belonging to the merged network to the external BGP peers.
* The external BGP peers have AS-path filters in place. ORG-1 AS should not appear in the AS path advertised by routers in ORG-2 and vice versa.
* As you plan to add more connections between the two networks, you must implement optimal end-to-end routing across the merged network. The BGP next hop of every prefix in the BGP table must be the final egress router of the merged network.

!!! Expert
    This is an expert-level challenge lab -- you are on your own. Good luck and Godspeed!

## Existing Lab Configuration

The routers in your lab use the following BGP AS numbers. Some of them advertise an IPv4 prefix.

 Node/ASN | Router ID | BGP RR | Advertised prefixes |
|----------|----------:|:------:|--------------------:|
| **AS65000** |||
| pe1 | 10.0.0.1 |  | 192.168.1.0/24 |
| pe2 | 10.0.0.3 |  |  |
| rr1 | 10.0.0.2 | ✅ |  |
| **AS65003** |||
| pe3 | 10.0.0.4 |  |  |
| pe4 | 10.0.0.6 |  | 192.168.3.0/24 |
| rr2 | 10.0.0.5 | ✅ |  |
| **AS65100** |||
| x1 | 10.0.0.10 |  | 192.168.100.1/24 |
| **AS65107** |||
| x2 | 10.0.0.11 |  | 192.168.101.1/24 |

Your routers have these BGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **pe1** | 10.0.0.1 | 65000 |
| | rr1 | 65000 | 10.0.0.2 |
| | x1 | 65100 | 10.1.0.2 |
| **pe2** | 10.0.0.3 | 65000 |
| | rr1 | 65000 | 10.0.0.2 |
| **pe3** | 10.0.0.4 | 65003 |
| | rr2 | 65003 | 10.0.0.5 |
| **pe4** | 10.0.0.6 | 65003 |
| | rr2 | 65003 | 10.0.0.5 |
| | x2 | 65107 | 10.1.0.18 |
| **rr1** | 10.0.0.2 | 65000 |
| | pe1 | 65000 | 10.0.0.1 |
| | pe2 | 65000 | 10.0.0.3 |
| **rr2** | 10.0.0.5 | 65003 |
| | pe3 | 65003 | 10.0.0.4 |
| | pe4 | 65003 | 10.0.0.6 |

**IGP configuration:**

* Routers in AS 65000 run OSPF.
* Routers in AS 65003 run IS-IS.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `challenge/20-merge-as`
* Execute **netlab up** ([device requirements](#req))
* Log into your devices with **netlab connect** and verify that the IP addresses and the BGP sessions are properly configured.

## Verification

The BGP table on X1 should contain four prefixes. None of the prefixes should have AS 65003 in the AS path:

```
x1# show ip bgp
BGP table version is 4, local router ID is 10.0.0.10, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 192.168.1.0/24   10.1.0.1                               0 65000 ?
*> 192.168.3.0/24   10.1.0.1                               0 65000 ?
*> 192.168.100.0/24 0.0.0.0                  0         32768 i
*> 192.168.101.0/24 10.1.0.1                               0 65000 65107 i
```

The BGP table on X2 should contain four prefixes. None of the prefixes should have AS 65000 in the AS path:

```
x2# show ip bgp
BGP table version is 4, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65107
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 192.168.1.0/24   10.1.0.17                              0 65003 ?
*> 192.168.3.0/24   10.1.0.17                              0 65003 ?
*> 192.168.100.0/24 10.1.0.17                              0 65003 65100 i
*> 192.168.101.0/24 0.0.0.0                  0         32768 i

Displayed  4 routes and 4 total paths
```

On PE1, the next hop of the BGP prefix 192.168.3.0/24 (or 192.168.101.0/24) should be 10.0.0.6:

```
pe1>show ip bgp 192.168.3.0
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 192.168.3.0/24
 Paths: 1 available
  Local
    10.0.0.6 from 10.0.0.2 (10.0.0.2)
      Origin INCOMPLETE, metric 0, localpref 100, IGP metric 0, weight 0, tag 0
      Received 00:06:14 ago, valid, internal, best
...
```

## Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP, OSPF, and IS-IS configuration modules](https://netlab.tools/platforms/#platform-routing-support) for the customer routers.
* If your preferred device does not support IS-IS (for example, Cumulus Linux), replace the **org_2** group setting `module: [ bgp, isis ]` in the lab topology file with `module: [ bgp, ospf ]`.
* Use any device [supported by the BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the external routers.
