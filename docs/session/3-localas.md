# Use Multiple AS Numbers on the Same Router

Some end-customers want to run BGP with their Internet Service Providers (ISPs) without acquiring a public BGP AS number. In such cases, ISPs might allocate a private BGP AS number to them. However, if you want to connect to multiple ISPs, you cannot expect to get the same private BGP AS number from all of them; your router will have to pretend it has multiple identities.

![Lab topology](topology-localas.png)

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each router router advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 10.0.0.1/32 |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.1/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.1/24 |

Your router has these EBGP neighbors.  _netlab_ configures them automatically; if you're using some other lab infrastructure, you'll have to configure EBGP neighbors and advertised prefixes manually.

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **rtr** | 10.0.0.1 | 65000 |
| | x1 | 65100 | 10.1.0.2 |
| | x2 | 65101 | 10.1.0.6 |

However, X2 (belonging to ISP-2) thinks your router should have AS number 65007:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **x2** | 10.0.0.11 | 65101 |
| | rtr | 65007 | 10.1.0.5 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `session/3-localas`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

## The Problem

Log into your router and check its EBGP sessions. The session with X1 should be established; the one with X2 should be stuck in the `Active` or `Idle` state[^IS]. This is the printout you would get on Arista EOS:

```
rtr>show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  x1                       10.1.0.2 4 65100             10        10    0    0 00:00:16 Estab   1      1
  x2                       10.1.0.6 4 65101             12        12    0    0 00:00:17 Active 
```

[^IS]: Most BGP implementations keep trying and show a BGP session that cannot be successfully established as `Active`. FRR (also used by Cumulus Linux) gives up and shows it as `Idle`. You have to clear the BGP session to tell FRR to retry.

You know that the BGP session with X2 is not established due to a BGP AS number mismatch, but you might not be so lucky in real life. Figure out how you'd discover that in a production environment.

For example, Arista EOS BGP logging messages tell you that the BGP neighbor (X2) keeps rejecting your BGP OPEN message due to "a bad AS number":

```
%BGP-3-NOTIFICATION: received from neighbor 10.1.0.6 (VRF default AS 65101) 2/2 (Open Message Error/bad AS number) 2 bytes
```

## Configuration Tasks

Most BGP implementations have a nerd knob that changes the local BGP AS number on a single EBGP session. It's usually configured with a command similar to **neighbor local-as**. The syntax and capabilities of this command vary between implementations. Some implementations cannot do anything else but "_use a different AS number_" while others have configurable AS-path handling behavior.  For example, you can decide whether to include the node BGP AS number in the AS path on Cumulus Linux.

* Configure BGP local AS on the EBGP session between RTR and X2 to be 65007.
* Ensure that the AS number 65000 never appears in the AS path advertised to X2.

!!! Warning
    After configuring the BGP local AS number, you might have to clear the BGP session with X2.

## Verification

You can use the **netlab validate** command if you've installed *netlab* release 1.8.3 or later and use Cumulus Linux, FRR, or Arista EOS on the external routers. The validation tests check:

* The state of the EBGP session between RTR and X2
* Whether RTR sends any routing updates to X2
* Whether RTR removes AS 65000 from the AS path before sending the updates to X2.

For example, this is the result you'd get if you configured the BGP local AS number on Cumulus Linux but forgot to remove AS 65000 from the outbound AS path:

![](session-localas-validate.png)

If the **netlab validate** command fails or you're using another network operating system on the ISP routers, it's time to start a troubleshooting session.

* Check the state of the BGP sessions on RTR with a command similar to **show ip bgp summary**. All sessions should be in the established state.
* Check the BGP table on X2 with a command similar to **show ip bgp**.

If you forgot to remove AS 65000 from the updates sent to X2, X2 will have a BGP table similar to the following one:

```
x2# show ip bgp
BGP table version is 3, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.1/32      10.1.0.5                 0             0 65007 65000 i
*> 192.168.100.0/24 10.1.0.5                               0 65007 65000 65100 i
*> 192.168.101.0/24 0.0.0.0                  0         32768 i

Displayed  3 routes and 3 total paths
```

The correct version of the BGP table on X2 is in the following printout. Please note that the AS 65000 is no longer in the AS path.

```
x2# show ip bgp
BGP table version is 11, local router ID is 10.0.0.11, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.1/32      10.1.0.5                 0             0 65007 i
*> 192.168.100.0/24 10.1.0.5                               0 65007 65100 i
*> 192.168.101.0/24 0.0.0.0                  0         32768 i

Displayed  3 routes and 3 total paths
```

**Next:** [Remove private AS numbers from the AS path](4-removeprivate.md).

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for the customer- and provider routers.
* You can do automated lab validation with Arista EOS, Cumulus Linux, or FRR running on X1 and X2. Automated lab validation requires _netlab_ release 1.8.3 or higher.
* Git repository contains external router initial device configurations for Cumulus Linux.

### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | x1 | swp1 |
| rtr | Ethernet2 | x2 | swp1 |

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
