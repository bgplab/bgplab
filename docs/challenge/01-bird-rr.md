# Using BIRD BGP Daemon as a BGP Route Reflector

In a [previous lab exercise](../ibgp/3-rr.md), you used BGP route reflectors on core routers to reduce the number of IBGP sessions in your network. BGP route reflection is a pure control plane functionality and does not have to run on a router (or a layer-3 switch). You'll use the BIRD Internet Routing Daemon in this lab as a BGP route reflector.

![Lab topology](topology-bird-rr.png)

You'll have to configure the IBGP sessions between routers in AS 65000 (PE1, PE2, and CORE) and the route reflector running BIRD in a container.

!!! Expert
    This is an expert-level challenge lab. We expect you to know what you're doing -- all you'll get from us are a few basic BIRD setup tricks and the verification guidelines.

## Existing Routing Protocol Configuration

The routers in your lab use the following BGP AS numbers:

| Node/ASN | Router ID | Advertised prefixes |
|----------|----------:|--------------------:|
| **AS65000** ||
| pe1 | 10.0.0.1 |  |
| core | 10.0.0.2 |  |
| pe2 | 10.0.0.3 |  |
| rr | 10.0.0.42 |  |
| **AS65100** ||
| x1 | 10.0.0.10 | 192.168.100.0/24 |
| **AS65101** ||
| x2 | 10.0.0.11 | 192.168.101.0/24 |

The EBGP sessions are preconfigured:

| Node | Router ID/<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|------------------|---------------------:|--------------:|
| **pe1** | 10.0.0.1 | 65000 |
| | x1 | 65100 | 10.1.0.2 |
| **pe2** | 10.0.0.3 | 65000 |
| | x2 | 65101 | 10.1.0.14 |
| **x1** | 10.0.0.10 | 65100 |
| | pe1 | 65000 | 10.1.0.1 |
| **x2** | 10.0.0.11 | 65101 |
| | pe2 | 65000 | 10.1.0.13 |

The routers in AS 65000 are running OSPF in area 0:

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| pe1 | Loopback | 10.0.0.1/32 | |
|  | eth2 | 10.1.0.6/30 | core |
| core | Loopback | 10.0.0.2/32 | |
|  | eth1 | 10.1.0.5/30 | pe1 |
|  | eth2 | 10.1.0.9/30 | pe2 |
|  | eth3 | 172.16.0.2/24 | rr |
| pe2 | Loopback | 10.0.0.3/32 | |
|  | eth1 | 10.1.0.10/30 | core |
| rr | eth1 | 172.16.0.1/24 | core |

## Start the Lab

You can start the lab [on your own lab infrastructure](../1-setup.md) or in [GitHub Codespaces](https://github.com/codespaces/new/bgplab/bgplab) ([more details](https://bgplabs.net/4-codespaces/)):

* Check the [device requirements](#req).
* If needed, [install containerlab](https://netlab.tools/labs/clab/) (it's preinstalled in GitHub Codespace) and build the BIRD container image with **netlab clab build bird**.
* Change directory to `challenge/01-bird`
* Execute **netlab up**
* Log into your devices with **netlab connect** and verify that the IP addresses, OSPF, and the EBGP sessions are properly configured.

## Configuring BIRD Daemon

The BIRD daemon is configured through configuration files. The configuration files are in the lab directory and mapped into the BIRD container:

| File | Mapped into | Contents |
|------|-------------|----------|
| bird.cfg | /etc/bird/bird.conf | Interfaces and OSPF configuration |
| bgp.cfg | /etc/bird/bgp.conf | BGP configuration (initially empty) |

To change the BIRD configuration:

* Edit the configuration file(s)
* Connect to the BIRD container with **netlab connect rr**
* Start **birdc**, the BIRD control program
* Execute **configure check** to check the configuration files[^MI]
* Execute **configure** to reconfigure the BIRD daemons

[^MI]: The main configuration file (`/etc/bird/bird.conf`) and any included file(s) (`/etc/bird/bgp.conf` in your lab)

```
$ netlab connect rr
Connecting to container clab-bird-rr, starting bash
root@rr:~# birdc
BIRD 2.14 ready.
bird> configure check
Reading configuration from /etc/bird/bird.conf
Configuration OK
bird> configure
Reading configuration from /etc/bird/bird.conf
Reconfiguration in progress
bird>
```

You can use the **show protocols** *birdc* command to display the BGP neighbors (BIRD configures every neighbor as a separate protocol instance):

Protocols run by the BIRD daemon after configuring the IBGP session with PE1
{ .code-caption }
```
bird> show protocols
Name       Proto      Table      State  Since         Info
device1    Device     ---        up     07:38:59.991
direct1    Direct     ---        up     07:38:59.991
kernel1    Kernel     master4    up     07:38:59.991
ospf_v2    OSPF       master4    up     07:50:49.423  Running
bgp_pe1_ipv4 BGP        ---        start  07:52:58.277  Active
```

The **show protocols all** command displays more information:

The details of a BGP neighbor (the IBGP session hasn't been configured on the other end)
{ .code-caption }
```
bird> show protocols all bgp_pe1_ipv4
Name       Proto      Table      State  Since         Info
bgp_pe1_ipv4 BGP        ---        start  07:52:58.277  Active        Socket: Connection reset by peer
  BGP state:          Active
    Neighbor address: 10.0.0.1
    Neighbor AS:      65000
    Local AS:         65000
    Connect delay:    1.598/5
    Last error:       Socket: Connection reset by peer
```

## Configure IBGP Sessions

You must configure these IBGP sessions in AS 65000 to propagate routes between X1 and X2:

| Route reflector | Source IP | RR client | Source IP |
|-----------------|----------:|-----------|----------:|
| rr | 172.16.0.1  | pe1    | 10.0.0.1  |
| | | core   | 10.0.0.2  |
| | | pe2    | 10.0.0.3  |

You might also have to revisit the concepts explained in these lab exercises[^TMI]:

* [Establish an IBGP Session](../ibgp/1-edge.md)
* [Build a Transit Network with IBGP](../ibgp/2-transit.md)
* [Use BGP Route Reflectors](../ibgp/3-rr.md)

[^TMI]: Trust me, I had to ;)

### BIRD Configuration Hints

* The default _netlab_ BIRD container runs BIRD version 2 ([documentation](https://bird.network.cz/?get_doc&f=bird.html&v=20))
* Each BGP neighbor is [configured](https://bird.network.cz/?get_doc&v=20&f=bird-6.html#ss6.4) as a separate protocol instance;
* You don't have to specify the source IPv4 address if the Linux host running the BIRD daemon has a single interface;
* If you don't activate the required address families (channels), BIRD terminates BGP sessions with *Unsupported Capability* notification.
* By default, BIRD imports all routes from a protocol (IBGP neighbor) into the master routing table, but does not export the master routing table routes into a protocol. If you want BIRD to advertise BGP routes to an IBGP neighbor, you have to [**export** them](https://bird.network.cz/?get_doc&v=20&f=bird-3.html#ss3.5).
* When configuring route export, ensure you export only BGP routes, not connected or OSPF routes. The easiest way to do that is to configure a **[filter](https://bird.network.cz/?get_doc&v=20&f=bird-5.html)** that matches BGP routes and then use that filter in the protocol **export** command.
* You'll have to restart the lab if you manage to crash the BIRD daemon. **bird** runs as the root process in the RR container, and the container terminates if you crash it. Unfortunately, there's no easy way to restart a container and reestablish its links in the containerlab environment[^LIF].

[^LIF]: All container interfaces are deleted when a container terminates. That might trigger interface removal in other containers if *containerlab* used *veth* pairs to establish inter-container connectivity. While *container* has a command to recreate the *veth* pairs, you'd still have to reapply (at least) the interface configuration to other containers.

## Verification

You've completed the lab exercise when:

* PE1, PE2, and CORE have a working IBGP session with RR.
* The BGP table on all routers contains prefixes advertised by X1 (192.168.100.0/24) and X2 (192.168.101.0/24)
* The BGP table on all routers contains exactly two prefixes, and they're both selected as the *best* routes.
* X1 can ping X2 from its loopback interface.

This is the BGP table you should see on the CORE router running FRR:

BGP table on the CORE router running FRR
{ .code-caption }
```
BGP table version is 8, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, u unsorted, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>i 192.168.100.0/24 10.0.0.1                 0    100      0 65100 i
 *>i 192.168.101.0/24 10.0.0.3                 0    100      0 65101 i

Displayed 2 routes and 2 total paths
```

And this is how you can ping X2 from X1 running FRR:

Pinging between X1 and X2
{ .code-caption }
```
netlab connect x1 ping x2 -I 192.168.100.1
Connecting to container clab-bird-x1, executing ping x2 -I 192.168.100.1
PING x2 (192.168.101.1) from 192.168.100.1: 56 data bytes
64 bytes from 192.168.101.1: seq=0 ttl=61 time=0.079 ms
64 bytes from 192.168.101.1: seq=1 ttl=61 time=0.078 ms
^C
--- x2 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.078/0.078/0.079 ms
```

## Reference Information

### Device Requirements {#req}

* BIRD daemon is running in a container; your *netlab* environment has to include Docker and containerlab installation (use **netlab install containerlab** on Ubuntu to install them).
* You must build a BIRD container with the **netlab clab build bird** command.
* Use any device [supported by the _netlab_ BGP and OSPF configuration modules](https://netlab.tools/platforms/#platform-routing-support) as your routers.
<!--
* You can do automated lab validation with Arista EOS or FRR running on lab routers.
-->
### Lab Wiring

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| x1 | eth1 | pe1 | eth1 |
| pe1 | eth2 | core | eth1 |
| core | eth2 | pe2 | eth1 |
| pe2 | eth2 | x2 | eth1 |
| core | eth3 | rr | eth1 |

### Lab Addressing

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **pe1** |  10.0.0.1/32 |  | Loopback |
| eth1 | 10.1.0.1/30 |  | pe1 -> x1 |
| eth2 | 10.1.0.6/30 |  | pe1 -> core |
| **core** |  10.0.0.2/32 |  | Loopback |
| eth1 | 10.1.0.5/30 |  | core -> pe1 |
| eth2 | 10.1.0.9/30 |  | core -> pe2 |
| eth3 | 172.16.0.2/24 |  | core -> rr |
| **pe2** |  10.0.0.3/32 |  | Loopback |
| eth1 | 10.1.0.10/30 |  | pe2 -> core |
| eth2 | 10.1.0.13/30 |  | pe2 -> x2 |
| **rr** |
| eth1 | 172.16.0.1/24 |  | rr -> core |
| **x1** |  192.168.100.1/24 |  | Loopback |
| eth1 | 10.1.0.2/30 |  | x1 -> pe1 |
| **x2** |  192.168.101.1/24 |  | Loopback |
| eth1 | 10.1.0.14/30 |  | x2 -> pe2 |
