# Passive BGP Sessions

BGP routers continuously try to establish TCP sessions (and start the BGP protocol) with the configured neighbors. That persistence might result in performance challenges when a hub router has hundreds (or thousands) of spoke neighbors that might not always be reachable. In those cases, a *passive* BGP router might offer an advantage; such a router would accept incoming TCP sessions to port 179 but never try to establish a TCP session with its BGP neighbors.

Passive BGP is a rarely used feature but might make sense in these scenarios:

* [Route reflectors](../ibgp/3-rr.md) with many clients,
* [Route servers](5-routeserver.md),
* Hubs in large VPN deployments,
* Leaf switches running BGP with servers or virtual machines, 
* BGP monitoring tools, 
* Routers outside a firewall [running BGP with an inside router](../basic/e-ebgp-multihop.md).

In this lab exercise, you'll make the hub BGP router passive and explore what happens with its view of its BGP neighbors as they shut down their BGP sessions.

![Lab topology](topology-passive-bgp.png)

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. Each router router advertises an IPv4 prefix.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| hub | 10.0.0.1 | 10.0.0.1/32 |
| **AS65100** ||
| s1 | 10.0.0.2 | 10.0.0.2/32 |
| **AS65103** ||
| s2 | 10.0.0.3 | 10.0.0.3/32 |
| **AS65107** ||
| s3 | 10.0.0.4 | 10.0.0.4/32 |

The hub router has these EBGP neighbors:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **hub** | 10.0.0.1 | 65000 |
| | s1 | 65100 | 172.16.0.2 |
| | s2 | 65103 | 172.16.0.3 |
| | s3 | 65107 | 172.16.0.4 |

_netlab_ automatically configures device interfaces, IP addresses, and BGP routing; if you're using another lab infrastructure, you'll have to configure lab devices manually.

## Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for HUB and S1.
* Use any device for which _netlab_ implements [passive BGP neighbors and BGP timers](https://netlab.tools/plugins/bgp.session/#platform-support) for the external routers (S2 and S3). The Git repository contains external router initial device configurations for Cumulus Linux.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `session/8-passive`
* Execute **netlab up**
* Log into your devices (HUB and S1) with **netlab connect** and verify that their IP addresses and the EBGP sessions are properly configured.

## The Problem

Log into the hub router and check its EBGP sessions. It should have three established EBGP sessions. Now shut down S2:

* Use **netlab status** to find the container/VM name of S2.
* Use **docker kill _container_** if you're running network devices as containers.
* Use **vagrant halt _vm_** if you're running network devices as virtual machines

After the BGP hold timer expires[^S2HD], the corresponding EBGP session on the hub router will most probably enter the `Connect` state[^CST]:

[^S2HD]: S2 tries to negotiate a 3-second BGP hold timer with the hub router

[^CST]: The state in which a device actively tries to open a TCP session with a BGP neighbor might be displayed as an `Active` state on some other network devices.

```
hub>show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  s1                       172.16.0.2 4 65100             10        12    0    0 00:04:32 Estab   1      1
  s2                       172.16.0.3 4 65103             65        75    0    0 00:01:36 Connect
  s3                       172.16.0.4 4 65107            101       114    0    0 00:04:31 Estab   1      1
```

We don't want that; we would like the hub router to ignore the unreachable neighbors.

## Configuration Tasks

On the hub router, configure all EBGP neighbors as passive BGP neighbors with a configuration command similar to **neighbor passive**.

!!! warning
    Cumulus Linux or FRR might reset the BGP session when you configure the device to be a passive BGP neighbor.

## Verification

Inspect the state of the BGP sessions on the hub router with a command similar to **show ip bgp summary**. The session with S2 should be in an `Idle` or `Active` state (but not in `Connect` state). This is the printout you should get on Arista EOS:

```
hub>show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  s1                       172.16.0.2 4 65100              6         8    0    0 00:01:24 Estab   1      1
  s2                       172.16.0.3 4 65103             47        56    0    0 00:00:46 Active
  s3                       172.16.0.4 4 65107             38        42    0    0 00:01:24 Estab   1      1
```

!!! tip
    When in doubt (the BGP states displayed by network devices can be confusing), use a command similar to **show ip bgp neighbor _ip-address_** and look for the *passive* keyword in the printout.
    
Now clear all BGP sessions on the hub router with a command similar to **clear ip bgp \***. The session with S3 should enter the `Idle` or `Active` state -- S3 is configured to be a passive EBGP peer, and two passive peers cannot establish a session.

## Reference Information

### Lab Wiring

| Origin Device | Origin Port | Link Name (NET) | Description          |
|---------------|-------------|-----------------|----------------------|
| hub | Ethernet1 | passive_1 | Carrier Ethernet LAN |
| s1 | Ethernet1 | passive_1 | Carrier Ethernet LAN |
| s2 | swp1 | passive_1 | Carrier Ethernet LAN |
| s3 | swp1 | passive_1 | Carrier Ethernet LAN |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **hub** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 172.16.0.1/24 |  | Carrier Ethernet LAN |
| **s1** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 172.16.0.2/24 |  | Carrier Ethernet LAN |
| **s2** |  10.0.0.3/32 |  | Loopback |
| swp1 | 172.16.0.3/24 |  | Carrier Ethernet LAN |
| **s3** |  10.0.0.4/32 |  | Loopback |
| swp1 | 172.16.0.4/24 |  | Carrier Ethernet LAN |
