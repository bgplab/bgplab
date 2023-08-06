# Configure Multiple EBGP Sessions

Now that you know how to configure an EBGP session let's move on to a more realistic scenario: you have a site with a WAN edge router connected to two upstream ISPs, and you're running EBGP with them.

![Lab topology](topology.png)

The routers in your lab use the following BGP AS numbers. Each upstream router advertises its loopback, another IPv4 prefix, and the default route.

| Node/ASN | Router ID | BGP RR | Advertised prefixes |
|----------|----------:|--------|--------------------:|
| **AS65000** |||
| rtr | 10.0.0.1 |  | |
| **AS65100** |||
| x1 | 10.0.0.10 |  | 10.0.0.10/32<br>192.168.100.0/24 |
| **AS65101** |||
| x2 | 10.0.0.11 |  | 10.0.0.11/32<br>192.168.101.0/24 |

After starting the lab with **netlab up**, log into your device (RTR) with **netlab connect rtr** and verify that the IP addresses are configured on all its interfaces.

Configure EBGP sessions using the following parameters:

| Node | Neighbor | Neighbor IPv4 | Neighbor AS | Local AS |
|------|----------|--------------:|------------:|---------:|
| rtr | x1 | 10.1.0.2 | 65100 |  |
| rtr | x2 | 10.1.0.6 | 65101 |  |

You might also want to configure neighbor description and BGP session logging to get an information message when the BGP session is established.

Check the state of the BGP session with a command similar to **show ip bgp summary**. This is a printout taken from Arista EOS:

```
rtr#show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  10.1.0.2 4 65100             11        10    0    0 00:00:17 Estab   3      3
  10.1.0.6 4 65101              9         8    0    0 00:00:12 Estab   3      3
```

Finally, use a command similar to **show ip bgp** to verify that your router received three prefixes from each EBGP neighbor: the  IPv4 prefix configured on the remote loopback interface, another IPv4 prefix, and the default route. This is how the printout looks like on Arista EOS:

```
rtr#show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      0.0.0.0/0              10.1.0.2              0       -          100     0       65100 i
 *        0.0.0.0/0              10.1.0.6              0       -          100     0       65101 i
 * >      10.0.0.10/32           10.1.0.2              0       -          100     0       65100 i
 * >      10.0.0.11/32           10.1.0.6              0       -          100     0       65101 i
 * >      192.168.100.0/24       10.1.0.2              0       -          100     0       65100 i
 * >      192.168.101.0/24       10.1.0.6              0       -          100     0       65101 i
```

**Next:**

* Advertise your address space

## Reference Information

You might find the following information useful if you're not using _netlab_ to build the lab:

### Lab Wiring

| Link Name       | Origin Device | Origin Port | Destination Device | Destination Port |
|-----------------|---------------|-------------|--------------------|------------------|
|  | rtr | Ethernet1 | x1 | swp1 |
|  | rtr | Ethernet2 | x2 | swp1 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | rtr -> x1 |
| Ethernet2 | 10.1.0.5/30 |  | rtr -> x2 |
| **x1** |  10.0.0.10/32 |  | Loopback |
| swp1 | 10.1.0.2/30 |  | x1 -> rtr |
| **x2** |  10.0.0.11/32 |  | Loopback |
| swp1 | 10.1.0.6/30 |  | x2 -> rtr |

