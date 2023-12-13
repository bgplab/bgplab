# BGP Local Preference in a Complex Routing Policy

In a previous lab exercise, you [used BGP local preference to prefer a high-speed uplink over a low-speed uplink](5-local-preference.md). That approach works well if you leave the backup link idle while the primary link is operational. Now, imagine that you want to send at least some of the traffic over the backup link that is connected to a different ISP:

![Lab topology](topology-policy-2isp.png)

In this lab, you'll create a routing policy using BGP local preference to:

* Send traffic toward prefixes in AS 65101 over the C2-X2 link
* Send all other traffic over the C1-X1 link

## Initial Router Configurations

The routers in your lab use the following BGP AS numbers. Each autonomous system advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| c1 | 10.0.0.1 | 192.168.42.0/24 |
| c2 | 10.0.0.2 | 192.168.42.0/24 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.0/24 |

Your routers have these BGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **c1** | 10.0.0.1 | 65000 |
| | c2 | 65000 | 10.0.0.2 |
| | x1 | 65100 | 10.1.0.2 |
| **c2** | 10.0.0.2 | 65000 |
| | c1 | 65000 | 10.0.0.1 |
| | x2 | 65101 | 10.1.0.10 |

Your network is also running OSPF in the backbone area:

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| c1 | Loopback | 10.0.0.1/32 | |
|  | Ethernet3 | 192.168.42.1/24 | c2 |
| c2 | Loopback | 10.0.0.2/32 | |
|  | Ethernet3 | 192.168.42.2/24 | c1 |

## External Autonomous Systems

Three other autonomous systems (AS65200, AS65205 and AS65207) are connected to the upstream ISPs:

![External autonomous systems](policy-extra-asn.png)

The external autonomous systems advertise these prefixes:

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65200** ||
| uc200 | 192.168.200.1 | 192.168.200.0/24 |
| **AS65205** ||
| uc205 | 192.168.205.1 | 192.168.205.0/24 |
| **AS65207** ||
| uc207 | 192.168.207.1 | 192.168.207.0/24 |

The virtual lab topology uses three additional devices to implement the external autonomous systems. If your lab environment is low on memory, or if you want to use [lab infrastructure that is not managed by _netlab_](../external/index.md), you can use the [common 4-router lab topology](../external/4-router.md) with Cumulus Linux as the external devices  (additional autonomous systems are emulated during BGP prefix origination on X1 and X2).

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `policy/a-locpref-route-map`
* Execute **netlab up** if you have enough memory to start a 7-node lab ([device requirements](#req)) or **netlab up topology.4-router.yml** if you want to create a 4-node lab[^XC]. You can also [deploy the lab on your lab infrastructure](../external/index.md).
* Log into your devices (C1 and C2) with **netlab connect** and verify their configurations.

[^XC]: The 4-node lab needs additional device configuration on X1 and X2. That configuration is only available for Arista EOS, Cumulus Linux, and FRR.

**Note:** *netlab* will configure IP addressing, OSPF, BGP, IBGP sessions, EBGP sessions, and BGP prefix advertisements on your routers. If you're not using *netlab*, you must manually configure your routers.

## Default Outgoing Traffic Flow

After starting the lab, log into C2 and examine its BGP table. You should get a printout similar to this one (generated on Arista cEOS):

```
c2>show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      0.0.0.0/0              10.1.0.10             0       -          100     0       65101 i
 *        0.0.0.0/0              10.0.0.1              0       -          100     0       65100 i
 * >      192.168.42.0/24        -                     -       -          -       0       i
 *        192.168.42.0/24        10.0.0.1              0       -          100     0       i
 * >      192.168.100.0/24       10.0.0.1              0       -          100     0       65100 i
 *        192.168.100.0/24       10.1.0.10             0       -          100     0       65101 65100 i
 * >      192.168.101.0/24       10.1.0.10             0       -          100     0       65101 i
 * >      192.168.200.0/24       10.0.0.1              0       -          100     0       65100 65200 i
 *        192.168.200.0/24       10.1.0.10             0       -          100     0       65101 65100 65200 i
 * >      192.168.205.0/24       10.1.0.10             0       -          100     0       65101 65205 i
 *        192.168.205.0/24       10.0.0.1              0       -          100     0       65100 65205 i
 * >      192.168.207.0/24       10.1.0.10             0       -          100     0       65101 65207 i
```

As you can see, C2 uses the C2-X2 link to reach AS 65100, AS 65205, and AS 65207. It also uses the C2-X2 link to reach unknown destinations (the default route points to X2).

Hint: there's an easier way to find BGP prefixes using the C2-X2 link if your devices support printout filters with regular expressions -- match all lines that include the '>' character (best route) and 10.1.0.10 (the next hop):

```
c2>show ip bgp | include >.*10.1.0.10
 * >      0.0.0.0/0              10.1.0.10             0       -          100     0       65101 i
 * >      192.168.101.0/24       10.1.0.10             0       -          100     0       65101 i
 * >      192.168.205.0/24       10.1.0.10             0       -          100     0       65101 65205 i
 * >      192.168.207.0/24       10.1.0.10             0       -          100     0       65101 65207 i
```

## Implement Complex Routing Policy

We want to use the C2-X2 link only for the traffic toward destinations in AS65101 -- you will have to create a routing policy on C2 that will:

* Increase the local preference for BGP prefixes originating in AS 65101 (where the AS path ends with 65101)
* Decrease the local preference for the default route -- BGP routers advertise the default route as belonging to their autonomous system
* Decrease the local preference for all other BGP prefixes received from AS 65101

**Hint:** you have probably used routing policies (often called **route maps**) in [previous lab exercises](index.md). You have also practiced:

* AS-path filters in the [Filter Transit Routes](2-stop-transit.md) exercise
* Prefix filters in the [Minimize the Size of Your BGP Table](4-reduce.md) exercise

!!! Warning
    Applying routing policy parameters to BGP neighbors doesn't necessarily change the BGP table, as the new routing policy might be evaluated only on new incoming updates. You might have to use a command similar to `clear ip bgp * soft in` to tell your router to ask its neighbors to resend their BGP updates.

## Verification

Examine the BGP table on C2 to verify the local preference of routes received from X2. You could use the simple **show ip bgp** command and sift through the printout, or use printout filters matching on the next hop (`10.1.0.10`), or display routes from a specific neighbor (assuming your device supports that)[^RA].

[^RA]: Some devices (example: Arista cEOS) can display routes *received* from a neighbor (before being processed by inbound routing policies) and routes *received and accepted* from a neighbor (after the routing policies). Make sure you use the correct form of the **show** command.

The following printout uses the last mechanism on Arista cEOS:

```
c2#show ip bgp neighbors 10.1.0.10 routes | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 *        0.0.0.0/0              10.1.0.10             0       -          50      0       65101 i
 *        192.168.100.0/24       10.1.0.10             0       -          50      0       65101 65100 i
 * >      192.168.101.0/24       10.1.0.10             0       -          200     0       65101 i
 *        192.168.200.0/24       10.1.0.10             0       -          50      0       65101 65100 65200 i
 *        192.168.205.0/24       10.1.0.10             0       -          50      0       65101 65205 i
 *        192.168.207.0/24       10.1.0.10             0       -          50      0       65101 65207 i
```

As you can see:

* Routes originating in AS 65101 have local preference 200 and are used as the best routes
* All other routes advertised by AS 65101 have local preference 50 and are not used.

Finally, you should log into C1 and examine routes received from C2. C1 should use C2 only to reach `192.168.101/24`.

```
c1>show ip bgp neighbors 10.0.0.2 routes | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 *        192.168.42.0/24        10.0.0.2              0       -          100     0       i
 * >      192.168.101.0/24       10.0.0.2              0       -          200     0       65101 i
```

!!! Tip
    C2 does not advertise routes it does not use to C1, so you won't be able to see any other routes from the C2 BGP table on C1.
    
## Reference Information

### Device Requirements {#req}

* Customer- and external routers: use any device [supported by the _netlab_ BGP and OSPF configuration modules](https://netlab.tools/platforms/#platform-routing-support).
* The 4-router topology requires additional configuration on X1 and X2. That configuration is only available for Arista EOS, Cumulus Linux, and FRR.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

The minimized version of this lab uses a subset of the [4-router lab topology](../external/4-router.md). Some links are unused to retain the interface names from that topology.

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
| Primary uplink | c1 | Ethernet1 | x1 | swp1 |
| Unused link | c1 | Ethernet2 | x2 | swp1 |
| Inter-ISP link | x1 | swp2 | x2 | swp2 |
| Unused link | c2 | Ethernet1 | x1 | swp3 |
| Backup uplink | c2 | Ethernet2 | x2 | swp3 |
| Customer internal link | c1 | Ethernet3 | c2 | Ethernet3 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **c1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | Primary uplink |
| Ethernet2 |  |  | Unused link |
| Ethernet3 | 192.168.42.1/24 |  | Customer internal link |
| **c2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 |  |  | Unused link |
| Ethernet2 | 10.1.0.9/30 |  | Backup uplink |
| Ethernet3 | 192.168.42.2/24 |  | Customer internal link |
| **x1** |  192.168.100.1/24 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | Primary uplink |
| swp2 | 10.1.0.5/30 |  | Inter-ISP link |
| swp3 |  |  | Unused link |
| **x2** |  192.168.101.1/24 |  | Loopback |
| swp1 |  |  | Unused link |
| swp2 | 10.1.0.6/30 |  | Inter-ISP link |
| swp3 | 10.1.0.10/30 |  | Backup uplink |

