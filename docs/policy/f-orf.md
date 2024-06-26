# Use Outbound Route Filters (ORF) for IP Prefixes

In the [Minimize the Size of Your BGP Table](4-reduce.md) lab exercise, you learned how to configure an inbound prefix list that filters incoming BGP updates. However, filtering incoming updates seems like a waste of CPU cycles and bandwidth:

* The upstream router has to build BGP update messages containing all the prefixes it wants to advertise.
* The receiving router has to process all those prefixes and filter many of them.

Wouldn't it be better if an inbound prefix list would automatically install an outbound prefix filter in the adjacent router? Welcome to the *Outbound Route Filters* (ORF), defined in [RFC 5292](https://datatracker.ietf.org/doc/html/rfc5292) (prefix-based ORF) and [RFC 5291](https://datatracker.ietf.org/doc/html/rfc5291) (ORF BGP capability).

![Lab topology](topology-orf.png)

!!! tip
    Outbound route filters make sense only when (A) the bandwidth is expensive and (B) the receiving router has significantly fewer CPU resources than the sending router. They also move the CPU load to the sending router, so you probably won't see them deployed between ISPs and their customers.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. X1 advertises several IPv4 prefixes plus the default route:

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 10.0.0.1/32 |
| **AS65100** ||
| x1 | 10.0.0.2 | 192.168.100.1/24<br>172.16.8.0/22<br>172.16.1.0/24<br>10.0.0.2/32 |

There is a single EBGP session between RTR and X2. _netlab_ configures it automatically; if you're using another lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **rtr** | 10.0.0.1 | 65000 |
| | x1 | 65100 | 10.1.0.2 |
| **x1** | 10.0.0.2 | 65100 |
| | rtr | 65000 | 10.1.0.1 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Find a [device that supports prefix-based ORF](#req) (for example, Cumulus Linux or FRR)
* If needed, temporarily change the lab device type with the `NETLAB_DEVICE` environment variable, for example:

```
$ export NETLAB_DEVICE=cumulus
```

* Change directory to `policy/f-orf`
* Execute **netlab up**
* Log into the lab devices with the **netlab connect** command and verify that the IP addresses and the EBGP sessions are properly configured.

## Configure an Inbound Prefix List

* Using the configuration commands you mastered in the [Minimize the Size of Your BGP Table](4-reduce.md) lab exercise, create an inbound prefix list on RTR that will permit the default route and prefixes in the 172.16.0.0/16 address space with prefix length lower than /24.
* Apply that prefix list to inbound EBGP updates received from X1.
* Inspect the BGP table on RTR to verify the proper operation of the prefix list. You should get a printout similar to this one:

```
rtr# show ip bgp
BGP table version is 17, local router ID is 10.0.0.1, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
 *> 0.0.0.0/0        10.1.0.2(x1)             0             0 65100 i
 *> 10.0.0.1/32      0.0.0.0(rtr)             0         32768 i
 *> 172.16.8.0/22    10.1.0.2(x1)             0             0 65100 i

Displayed 3 routes and 3 total paths
```

* Turn on BGP update debugging and clear the BGP session between RTR and X1 (use **terminal monitor**, followed by **debug bgp updates in** and **clear ip bgp \*** on recent FRR releases). You should see incoming BGP updates for all prefixes known by X1, several of them filtered by the inbound prefix list on RTR:

[![](policy-orf-printout-prefix-list.png)](policy-orf-printout-prefix-list.png)

## Enable Outbound Route Filters

With the inbound prefix list configured on RTR, it's time to get ORF working on X1. ORF is a negotiated BGP capability that is usually not enabled by default. You must enable it on both ends of a BGP session with a configuration command similar to **neighbor capability** within the BGP routing process configuration or the BGP address family configuration.

Use a command similar to **show bgp neighbors** to verify that the routers in your lab agreed to use ORF. You should get a printout like this one on FRR (ORF capability is negotiated within a BGP address family):

```
rtr# show bgp neighbors 10.1.0.2
BGP neighbor is 10.1.0.2, remote AS 65100, local AS 65000, external link
...
 For address family: IPv4 Unicast
  Update group 8, subgroup 8
  Packet Queue length 0
  AF-dependant capabilities:
    Outbound Route Filter (ORF) type (64) Prefix-list:
      Send-mode: advertised, received
      Receive-mode: advertised, received
  Outbound Route Filter (ORF): sent;
  Community attribute sent to this neighbor(large)
  Inbound path policy configured
  Incoming update prefix filter list is *inbound
  2 accepted prefixes
```

Once you have verified your routers agreed to use ORF, clear the EBGP session and observe the reduced number of inbound updates on RTR:

[![](policy-orf-printout-orf.png)](policy-orf-printout-orf.png)

!!! note
    The BGP daemon in FRR release 10.0.1 resends the BGP prefixes permitted by the ORF filter three times. That's probably a bug that might be fixed when you do this lab exercise.

Some devices have **show** commands that display installed ORF entries. For example, you can use the **show bgp *af* neighbor *address* received prefix-filter** command on FRR to display them:

```
x1# show bgp ipv4 nei 10.1.0.1 received prefix-filter
Address Family: IPv4 Unicast
ip prefix-list 10.1.0.1.1.1: 2 entries
   seq 5 permit 0.0.0.0/0
   seq 10 permit 172.0.0.0/8 le 23
```

## Dynamic Changes in ORF Prefix Filters

Finally, add another entry to the inbound prefix list on RTR and use the **debug bgp updates** together with **debug bgp neighbor-events** on FRR (other platforms have similar debugging commands) to observe the ORF updates and refreshed routing updates triggered by changes in the inbound prefix list.

## Reference Information

This lab can run on a subset of the [4-router lab topology](../external/4-router.md).

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) that implements prefix-based ORF (for example, Cumulus Linux or FRR)
* Git repository contains initial device configurations for Cumulus Linux.
* If you want to use the **terminal monitor** command on FRR, you must use a newer image[^FIL] than the one used by other BGP labs[^FRO]. You can [change the lab defaults](../1-setup.md#defaults) or change the FRR image with an environment variable before executing **netlab up**, for example:

```
export NETLAB_DEVICES_FRR_CLAB_IMAGE=quay.io/frrouting/frr:10.0.1
```

[^FIL]: Inspect the [list of available FRR containers](https://quay.io/repository/frrouting/frr?tab=tags&tag=latest) to select a recent image.

[^FRO]: We have to use an older version of FRR due to the [undesired OSPF/BGP interaction behavior in recent FRR versions](https://blog.ipspace.net/2024/03/frr-ibgp-loopbacks.html).

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | swp1 | x1 | swp1 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  192.168.100.1/24 |  | Loopback |
| eth1 | 10.1.0.2/30 |  | x1 -> rtr |
| **x2** |  192.168.101.1/24 |  | Loopback |
| eth1 | 10.1.0.6/30 |  | x2 -> rtr |
