# Configure a Single EBGP Session

We'll start with the simplest possible scenario: configure an EBGP session between your device and an upstream router (X1):

![Lab topology](topology.png)

After starting the lab with **netlab up**, log into your device (RTR) with **netlab connect rtr** and verify that the IP addresses are configured on all its interfaces.

Configure an EBGP session using the following parameters:

| neighbor IP address | neighbor AS number |
|--------------------:|-------------------:|
| 10.1.0.2            | 65100              |

You might also want to configure neighbor description and BGP session logging to get an information message when the BGP session is established.

Check the state of the BGP session with a command similar to **show ip bgp summary**. This is a printout taken from Arista EOS:

```
rtr#show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  10.1.0.2 4 65100             33        37    0    0 00:01:25 Estab   2      2
```

Finally, use a command similar to **show ip bgp** to verify that your router received two prefixes from the EBGP neighbor: the default route and the loopback remote interface (10.0.0.10/32). This is how the printout looks like on Arista EOS:

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
 * >      10.0.0.10/32           10.1.0.2              0       -          100     0       65100 i
```

**Next:**

* You might want to protect the EBGP session with an MD5 password and the TTL check.
* If you're in a rush, connect with the second upstream provider.