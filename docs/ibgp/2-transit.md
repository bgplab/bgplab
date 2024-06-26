# Build a Transit Network with IBGP

In the *[Establish an IBGP Session Between WAN Edge Routers](1-edge.md)* lab exercise, you built a simple network with two adjacent BGP routers. In this exercise, you'll explore the impact of adding a core router between edge routers running BGP.

![Lab topology](topology-ibgp-transit.png)

After starting the lab, you'll have to configure all the IBGP sessions needed to establish connectivity between the loopback interfaces of PE2 and EXT routers. You MUST NOT use route redistribution between OSPF and BGP to solve the connectivity issues (there's an [excellent reason](https://blog.ipspace.net/2020/10/redistributing-bgp-into-ospf.html) for that restriction).

## Existing Lab Configuration

When starting the lab with _netlab_, you'll get a preconfigured lab:

* All routers will have their interfaces and IP addresses configured
* OSPF will be running between PE1, PE2, and CORE routers.
* BGP will be configured on PE1, PE2 and EXT routers. All three routers will advertise their loopback interfaces in BGP.
* There will be an EBGP session between PE1 and EXT routers.

!!! Warning
    To simplify the verification process, the lab topology uses an unnumbered IPv4 link between PE2 and CORE routers. That link will be changed to a regular IPv4 subnet if your devices don't [support unnumbered IPv4 links](https://netlab.tools/platforms/#platform-initial-addresses) or cannot [run OSPF over unnumbered IPv4 links](https://netlab.tools/module/ospf/#ospf-interfaces), resulting in a slight change in IP routing tables and printouts.

The following tables summarize the existing lab configuration.
    
### BGP Configuration

The routers in your lab use the following BGP AS numbers. The external router advertises an IPv4 prefix; your PE routers advertise their loopback IPv4 addresses.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| pe1 | 10.0.0.2 | 10.0.0.2/32 |
| pe2 | 10.0.0.3 | 10.0.0.3/32 |
| **AS65100** ||
| ext | 10.0.0.10 | 172.16.42.0/24 |

_netlab_ also configures the EBGP session between PE1 and EXT routers.

| Node | Neighbor | Neighbor AS | Neighbor IPv4 |
|------|----------|------------:|--------------:|
| **ext** | pe1 | 65000 | 10.1.0.6 |
| **pe1** | ext | 65100 | 10.1.0.5 |
 
### OSPF Configuration

OSPF backbone area is configured on the following routers in AS 65000:

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| core | Loopback | 10.0.0.1/32 | |
|  | Ethernet1 | 10.1.0.1/30 | pe1 |
|  | Ethernet3 | True | pe2 |
| pe1 | Loopback | 10.0.0.2/32 | |
|  | swp1 | 10.1.0.2/30 | core |
| pe2 | Loopback | 10.0.0.3/32 | |
|  | Ethernet3 | True | core |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `ibgp/2-transit`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your devices (R1, R2) with **netlab connect** and verify that _netlab_ correctly configured their IP addresses, OSPF routing, and EBGP sessions.

!!! Warning
    If you're not using _netlab_, you must configure CORE and PE2 routers yourself. Configurations for PE1 and EXT routers are in the `config` subdirectory.

## Propagate External BGP Routes to PE2

Try to ping the external router (`172.16.42.42`) from PE2. You have to check the connectivity between the loopback addresses, so you should use a version of the **ping** command that specifies the source interface or the source IP address. For example, you must use `ping 172.16.42.42 source loop 0` on Arista EOS.

!!! Tip
    * You don't have to worry about the source IP address of the ICMP Echo packets on devices that support unnumbered IPv4 interfaces -- these devices will automatically set the packet's source IP address to the device's loopback IP address.
    * The extended **ping** command is often available only in privileged (**enable**) CLI mode.

The **ping** command will most likely fail[^DP]. Arista EOS displays the root cause of the failure: the destination network is not in the IP routing table:

```
pe2#ping 172.16.42.42 source loop 0
PING 172.16.42.42 (172.16.42.42) from 10.0.0.3 : 72(100) bytes of data.
ping: sendmsg: Network is unreachable
ping: sendmsg: Network is unreachable
ping: sendmsg: Network is unreachable
ping: sendmsg: Network is unreachable
ping: sendmsg: Network is unreachable

--- 172.16.42.42 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 40ms
```

[^DP]: If it doesn't, you have a more interesting problem to troubleshoot -- why does it work? 

A quick look into the routing- and BGP table on PE2[^UBP] confirms that PE2 knows nothing about the IPv4 prefix `172.16.42.0/24`.

[^UBP]: Most **show** printouts in this lab exercise use the `| begin Something` pipe to skip the (mostly irrelevant) header information.

```
pe2#show ip route | begin Gateway
Gateway of last resort is not set

 O        10.0.0.1/32 is directly connected, Ethernet3
 O        10.0.0.2/32 [110/20] via 10.0.0.1, Ethernet3
 C        10.0.0.3/32 is directly connected, Loopback0
 O        10.1.0.0/30 [110/20] via 10.0.0.1, Ethernet3

pe2#show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.3/32            -                     -       -          -       0       i
```

!!! Warning
    You might not have the 10.0.0.3/32 prefix in the BGP table on PE2 due to a bug in _netlab_ releases older than 1.6.4-post2. If that's the case, configure BGP on PE2 to advertise the PE2 loopback interface (see [Advertise IPv4 Prefixes to BGP Neighbors](../basic/3-originate.md) for more details). Even better: stop the lab, upgrade _netlab_, and restart the lab.

The lack of BGP routes on PE2 shouldn't surprise you if you completed the *[Establish an IBGP Session Between WAN Edge Routers](1-edge.md)* lab exercise -- you already know you need an IBGP session between PE1 and PE2.

**Configuration task:**

* Configure an IBGP session between the loopback interfaces of PE1 and PE2[^DFA].

!!! Tip
    The IBGP session is preconfigured on PE1 and should be established as soon as you configure it on PE2.

[^DFA]: Remember to activate the IBGP session within the IPv4 address family (AF) if your device requires per-AF neighbor activation.

**Verification:**

Check the BGP neighbors and the BGP table on PE2. You should see an established IBGP session between PE1 and PE2 in the BGP summary printout and the BGP route for `172.16.42.0/24` in the BGP table.

This is the printout you should get on Arista EOS:

```
pe2#show ip bgp sum
BGP summary information for VRF default
Router identifier 10.0.0.3, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  10.0.0.2 4 65000             20        20    0    0 00:00:08 Estab   2      2
pe2#show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.2/32            10.0.0.2              0       -          100     0       i
 * >      10.0.0.3/32            -                     -       -          -       0       i
 * >      172.16.42.0/24         10.0.0.2              0       -          100     0       65100 i
```

Retry the **ping** command. It should no longer complain that the network is unreachable but could generate another bit of information on devices that parse and display ICMP error reports. For example, Arista EOS reports that the CORE router (10.0.0.1) claims it cannot reach the destination:

```
pe2#ping 172.16.42.42 source loop 0
PING 172.16.42.42 (172.16.42.42) from 10.0.0.3 : 72(100) bytes of data.
From 10.0.0.1 icmp_seq=1 Destination Net Unreachable

--- 172.16.42.42 ping statistics ---
5 packets transmitted, 0 received, +1 errors, 100% packet loss, time 30ms
```

## Fixing the Core Routing

Log into the router complaining it cannot reach the destination (the CORE router) and check its IP routing table. The route for `172.16.42.0/24` is missing.

```
core#show ip route | begin Gateway
Gateway of last resort is not set

 C        10.0.0.1/32 is directly connected, Loopback0
 O        10.0.0.2/32 [110/10] via 10.1.0.2, Ethernet1
 O        10.0.0.3/32 is directly connected, Ethernet3
 C        10.1.0.0/30 is directly connected, Ethernet1
```

That shouldn't be a big surprise; after all, the external prefix is advertised only in BGP, and the CORE router runs only OSPF.

There are at least four ways to fix the routing in the core of your autonomous system:

* Redistribute EBGP information into OSPF. That's [dangerous in real-life networks with large BGP tables](https://blog.ipspace.net/2020/10/redistributing-bgp-into-ospf.html), and thus, you are not allowed to do it in this lab exercise.
* Advertise an OSPF default route from PE1. That would solve your immediate problem but wouldn't result in an actual transit network -- you would run into "exciting" challenges when trying to connect external networks to PE2. This option is thus also off the table.
* Hide the transit packets from the CORE router using MPLS or IP-over-something tunnels. While the MPLS approach is commonly used to [build BGP-free core networks](https://blog.ipspace.net/2012/01/bgp-free-service-provider-core-in.html), it's too complex for this lab exercise[^FFDI].
* Make the CORE router part of the BGP routing. This is the approach we'll use.

[^FFDI]: ... but as you have a running lab that's easy to restart, please feel free to try to get it to work. You get bonus points if you [decide to use Segment Routing](https://blog.ipspace.net/2021/05/segment-routing-mpls-bgp-free-core.html) and a virtual 6-pack of Kool-Aid if you use SRv6 ;)

**Configuration tasks:**

* Configure BGP with AS number 65000 on the CORE router
* Configure IBGP sessions between all BGP routers in AS 65000.

!!! Tip
    * Due to the IBGP loop avoidance mechanism (never advertise IBGP routes to other IBGP neighbors), you must configure a full mesh of IBGP sessions, adding PE1-CORE and PE2-CORE IBGP sessions. Your lab might work without the PE2-CORE IBGP session but would probably stop working when you connect an EBGP neighbor to PE2[^DLER].
    * The IBGP session between PE1 and CORE routers is preconfigured on PE1 and should be established as soon as you configure it on the CORE router. You'll have to configure the PE2-CORE IBGP session on both ends.

[^DLER]: Proving that is left as an exercise for the reader

**Verification:**

Check the BGP neighbors and the BGP table on the CORE router. The router should have two established IBGP sessions and three prefixes in its BGP table:

```
core#show ip bgp sum
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  10.0.0.2 4 65000             14        14    0    0 00:00:10 Estab   2      2
  10.0.0.3 4 65000             10         9    0    0 00:00:08 Estab   1      1
core#show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.2/32            10.0.0.2              0       -          100     0       i
 * >      10.0.0.3/32            10.0.0.3              0       -          100     0       i
 * >      172.16.42.0/24         10.0.0.2              0       -          100     0       65100 i
```

Retry the **ping** command on PE2. PE2 should be able to reach the EXT router:

```
pe2#ping 172.16.42.42 source loop 0
PING 172.16.42.42 (172.16.42.42) from 10.0.0.3 : 72(100) bytes of data.
80 bytes from 172.16.42.42: icmp_seq=1 ttl=62 time=0.086 ms
80 bytes from 172.16.42.42: icmp_seq=2 ttl=62 time=0.007 ms
80 bytes from 172.16.42.42: icmp_seq=3 ttl=62 time=0.008 ms
80 bytes from 172.16.42.42: icmp_seq=4 ttl=62 time=0.006 ms
80 bytes from 172.16.42.42: icmp_seq=5 ttl=62 time=0.007 ms

--- 172.16.42.42 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.006/0.022/0.086/0.032 ms, ipg/ewma 0.032/0.053 ms
```

**Next:** [Use BGP Route Reflectors](3-rr.md)

## Reference Information

This lab uses the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP and OSPF configuration modules](https://netlab.tools/platforms/#platform-routing-support).
* Git repository contains initial device configurations for Cumulus Linux.

### Lab Wiring

This lab uses the [4-router lab topology](../external/4-router.md) with the following mapping between the routers in the 4-router lab topology and this lab:

| 4-router-topology device | Lab device |
|-----|------|
| C1  | Core |
| C2  | PE2  |
| X1  | PE1  |
| X2  | EXT  |

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
|  | core | Ethernet1 | pe1 | swp1 |
| Unused link | core | Ethernet2 | ext | swp1 |
| Inter-AS link | pe1 | swp2 | ext | swp2 |
| Unused link | pe2 | Ethernet1 | pe1 | swp3 |
| Unused link | pe2 | Ethernet2 | ext | swp3 |
|  | core | Ethernet3 | pe2 | Ethernet3 |

**Note**: Some interfaces are not used to conform with the predefined 4-router lab topology.

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **core** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | core -> pe1 |
| Ethernet2 |  |  | Unused link |
| Ethernet3 | True |  | core -> pe2 |
| **ext** |  172.16.42.42/24 |  | Loopback |
| swp1 |  |  | Unused link |
| swp2 | 10.1.0.5/30 |  | Inter-AS link |
| swp3 |  |  | Unused link |
| **pe1** |  10.0.0.2/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | pe1 -> core |
| swp2 | 10.1.0.6/30 |  | Inter-AS link |
| swp3 |  |  | Unused link |
| **pe2** |  10.0.0.3/32 |  | Loopback |
| Ethernet1 |  |  | Unused link |
| Ethernet2 |  |  | Unused link |
| Ethernet3 | True |  | pe2 -> core |

**Note**: Some interfaces are not configured with IP addresses to conform with the predefined 4-router lab topology.

