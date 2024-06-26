# Limit the Number of Accepted BGP Prefixes

Numerous global BGP routing incidents are caused by fat fingers, including those in which a network running BGP starts advertising an enormous amount of BGP prefixes[^RD]. Most BGP implementations contain mechanisms that shut down BGP sessions with neighbors that advertise excessive BGP prefixes; you'll practice them in this lab exercise.

[^RD]: Most often caused by careless route redistribution and lack of output filters.

![Lab topology](topology-max-prefix.png)

!!! Warning
    Recent Ansible releases broke the Ansible playbook used within the **netlab config** command. You must use *netlab* release `1.7.2-post1` or later to run this lab. Upgrade _netlab_ with the `sudo pip3 install --upgrade networklab` command or a similar command, depending on your Python setup.

## Existing BGP Configuration

The routers in your lab use the following BGP AS numbers. The _customer_ router advertises either a single prefix or over a dozen prefixes.

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| rtr | 10.0.0.1 | 10.0.0.1/32 |
| **AS65100** ||
| customer | 192.168.100.1 | 192.168.100.0/24 |

Your router has a single EBGP neighbor (the _customer_ router).  _netlab_ configures it automatically. Configure BGP manually if you're using some other lab infrastructure.

| Node | Neighbor | Neighbor AS | Neighbor IPv4 |
|------|----------|------------:|--------------:|
| **rtr** | customer | 65100 | 10.1.0.1 |

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `basic/b-max-prefix`
* Execute **netlab up** ([device requirements](#req), [other options](../external/index.md))
* Log into your router (RTR) with **netlab connect rtr** and verify that the IP addresses and the EBGP sessions are properly configured.

## The Problem

Log into your router and examine its BGP table. You should see two prefixes: a local one and one from the _customer_ router. This is the printout you would get on Arista cEOS:

```
rtr>show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      192.168.100.0/24       10.1.0.1              0       -          100     0       65100 i
```

Now emulate a *fat fingers* incident in the customer network. Use **sh** to execute the `start` script, optionally specifying the number of prefixes you want the customer to generate:

```
$ sh start 20
Generating 20 prefixes on the customer router
PLAY 1: DEPLOY DEVICE CONFIGURATION
task 9: customer
task 12: customer

Done
```

!!! tip
    If you don't want to run a shell script, use `netlab config addprefixes --limit customer`
    
Next, log into your router and examine its BGP table. You should see twenty additional prefixes advertised by the _customer_ router:

```
rtr>show ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      10.42.1.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.2.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.3.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.4.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.5.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.6.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.7.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.8.0/24           10.1.0.1              0       -          100     0       65100 i
 * >      10.42.9.0/24           10.1.0.1              0       -          100     0       65100 i

... The rest of the printout was deleted ...
```

To stop the *fat finger* incident, run `sh stop` or `netlab config removeprefixes --limit customer`.

```
$ sh stop
Stop advertising extra BGP prefixes
PLAY 1: DEPLOY DEVICE CONFIGURATION
task 11: customer

Done
```

Let's make sure we're not affected by the customer's clumsiness. The best way to do that is to limit the number of BGP prefixes we accept from the customer.

## Configuration and Validation

* Configure BGP session logging on your router and ensure the logging messages are sent to the terminal window you're using to connect to the router.
* Limit the number of prefixes accepted from the _customer_ router to 10 using a router configuration command similar to **neighbor maximum-routes**. Generate a warning if the number of prefixes is exceeded.
* In another window, execute the **sh start 15** command [^NC15] and check whether you got the expected warning. This is what you should get on Arista cEOS:

[^NC15]: Or `netlab config addprefixes --limit customer -e pfx=15`

```
%BGP-5-AFI_SAFI_MAX_ROUTES_WARNING: Peer 10.1.0.1 (VRF default AS 65100) has exceeded its configured maximum total number of routes (10) of address family IPv4 Unicast; ROUTING INFORMATION IS BEING LOST
```

!!! tip
    Some BGP implementations generate a warning message while accepting all incoming prefixes. Arista EOS generates a warning message and drops random extraneous prefixes.

* Stop the *fat finger* incident with **sh stop**
* Limit the number of prefixes accepted from the _customer_ router to 20, with a warning generated when the number of prefixes exceeds 10.
* Simulate a lower-impact incident with **sh start 10**. You should see a warning message on your router; this is the message generated by Arista cEOS:

```
%BGP-5-AFI_SAFI_MAX_ROUTES_EARLY_WARNING: Number of paths received from peer 10.1.0.1 (VRF default AS 65100) has exceeded the configured early warning limit (10) of address family IPv4 Unicast
```

* Increase the severity of the incident with **sh start 20**. Your router should terminate the EBGP session with the _customer_ router and generate an error message similar to the one generated by Arista cEOS:

```
%BGP-5-ADJCHANGE: peer 10.1.0.1 (VRF default AS 65100) old state Established event MaxPath new state Idle
%BGP-3-NOTIFICATION: sent to neighbor 10.1.0.1 (VRF default AS 65100) 6/1 (Cease/maximum number of prefixes reached) 0 bytes
```

* Inspect the state of the BGP sessions with a command similar to **show ip bgp summary**. The EBGP session with the _customer_ router should be *idle* or *shutdown*:

```
rtr#show ip bgp sum
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  customer                 10.1.0.1 4 65100            257       288    0    0 00:01:02 Idle(MaxPath)
```

* Reset the session with the _customer_ router with a command similar to **clear ip bgp 10.1.0.1**. You should see a log message when the session is re-established and another a few moments later when the number of received prefixes yet again exceeds the specified limits. Arista cEOS generates these messages:

```
rtr##clear ip bgp 10.1.0.1
%BGP-5-PEER_CLEAR: BGP peering for neighbor 10.1.0.1 (vrf default) was hard reset by admin on vty8 (192.168.121.1)
%BGP-5-ADJCHANGE: peer 10.1.0.1 (VRF default AS 65100) old state OpenConfirm event Established new state Established
%BGP-5-AFI_SAFI_MAX_ROUTES_EARLY_WARNING: Number of paths received from peer 10.1.0.1 (VRF default AS 65100) has exceeded the configured early warning limit (10) of address family IPv4 Unicast
%BGP-5-AFI_SAFI_MAX_ROUTES_LIMIT: Peer 10.1.0.1 (VRF default AS 65100) has exceeded its configured maximum total number of routes (20) of address family IPv4 Unicast; Put into idle state forever
%BGP-5-ADJCHANGE: peer 10.1.0.1 (VRF default AS 65100) old state Established event MaxPath new state Idle
%BGP-3-NOTIFICATION: sent to neighbor 10.1.0.1 (VRF default AS 65100) 6/1 (Cease/maximum number of prefixes reached) 0 bytes
```

* Fix the _customer_ router with the **sh stop** script and reset the EBGP session on your router. The EBGP session should be established and remain operational.

## Reference Information

This lab uses a subset of the [4-router lab topology](../external/4-router.md). The following information might help you if you plan to build custom lab infrastructure:

### Device Requirements {#req}

* Use any device [supported by the _netlab_ BGP configuration module](https://netlab.tools/platforms/#platform-routing-support) for your router.
* Use Arista EOS, Cumulus Linux, or FRR for the _customer_ router to use the provided configuration scripts. You'll have to manually configure the origination of excessive BGP prefixes if you use any other _netlab_-supported device for the customer router.
* The Git repository contains the initial Cumulus Linux device configuration for the _customer_ router.

### Lab Wiring

Point-to-Point links:

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| rtr | Ethernet1 | customer | swp1 |

Stub links:

| Origin Device | Origin Port | Description          |
|---------------|-------------|----------------------|
| customer | swp2 | customer -> stub |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | rtr -> customer | 
| **customer** |  192.168.100.1/24 |  | Loopback |
| swp1 | 10.1.0.1/30 |  | customer -> rtr |
| swp2 | 10.42.1.10/24 |  | customer -> stub |
