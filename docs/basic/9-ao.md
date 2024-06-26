# Protect BGP Sessions with TCP Authentication Option (TCP-AO)

In a previous lab we [used MD5 checksum to password-protect EBGP sessions](6-protect.md). In this one we'll implement EBGP session protection using a newer mechanism: [TCP Authentication Option defined in RFC 5925](https://datatracker.ietf.org/doc/html/rfc5925).

![Lab topology](topology-ao.png)

## Lab Requirements

This lab uses a slightly different supporting infrastructure than all other BGP labs. Linux kernel does not support TCP-AO (as of September 2023), which means that we cannot use virtual machines or containers running Cumulus Linux or Ubuntu/FRR as the external BGP routers. It's also impossible to use Arista cEOS container as it relies on the TCP/IP stack of the underlying Linux kernel.

The only way to run this lab is to start external routers as virtual machines using Virtualbox or KVM/libvirt virtualization. _netlab_ currently [supports TCP-AO](https://netlab.tools/plugins/ebgp.utils/) on these devices:

* Arista EOS virtual machines
* Cisco CSR 1000v
* Nokia SR-OS (virtual machine running in a container)

!!! Warning
    This lab was designed to be used with _netlab_. You need _netlab_ release 1.6.3 or later to run it -- we added TCP-AO support in that release.

## Adjusting Lab Topology

The topology file (`topology.yml`) in the `basic/9-ao` directory uses Arista EOS virtual machines. You can use it as-is if:

* You're running labs with Virtualbox or KVM/libvirt and
* You installed Arista EOS Vagrant box (instructions: [Virtualbox](https://netlab.tools/labs/virtualbox/), [KVM/libvirt](https://netlab.tools/labs/eos/))

If you created Cisco CSR1000v Vagrant box for your environment, replace `device: eos` in the **external** group in `topology.yml` with `device: csr`.

If you want to run your labs with containers, you could use Nokia SR-OS as the external router[^GLF] -- replace the `device: eos` with `device: sros`. _netlab_ uses _containerlab_ provider to run Nokia SR-OS, so you might have to add `provider: clab` to the **external** group.

!!! Warning
    * Nokia SR-OS runs as a virtual machine inside a container. You'll still need _nested virtualization_ to run it if you're running your labs in a Ubuntu virtual machine.
    * TCP-AO does not work on Arista EOS container as it uses underlying Linux TCP/IP stack.

[^GLF]: Assuming you manage to get a license to do it from Nokia.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md).

* Change directory to `basic/9-ao`
* Execute **netlab up**
* Log into your device (RTR) with **netlab connect rtr** and verify its configuration.

If you're using a device supported by *netlab*, you'll get configured interfaces, IP addresses, BGP routing process, and BGP neighbors.

If you're using an unsupported device, it's best if you do this lab exercise after the [Advertise IPv4 Prefixes to BGP Neighbors](3-originate.md) one. If you're using your own lab infrastructure, use the wiring information from the [protect EBGP sessions](6-protect.md) lab.

## Configuration Tasks

The EBGP sessions with X1 and X2 will not be established because X1 and X2 use TCP-AO BGP session protection. They might be stuck in `Connect`, `OpenSent` or `OpenConfirm` state as illustrated by the following printout produced on Arista EOS:

```
rtr#show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  x1                       10.1.0.2 4 65100             11        17    0    0 00:00:04 Connect
  x2                       10.1.0.6 4 65101             11        15    0    0 00:00:07 Connect
```

To make BGP sessions work, configure TCP-AO on both EBGP sessions on your router using the following parameters:

| BGP neighbor | IP address | TCP-AO secret | Algorithm    |
|--------------|-----------:|---------------|--------------|
| x1           | 10.1.0.2   | `BigSecret`   | HMAC-SHA1-96 |
| x2           | 10.1.0.6   | `GuessWhat`   | HMAC-SHA1-96 |

## Verification

Check the state of the BGP sessions with a command similar to **show ip bgp summary** -- the BGP sessions should be established, and you should have received several prefixes from both neighbors.

This is a printout taken from Arista EOS:

```
rtr#show ip bgp summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  x1                       10.1.0.2 4 65100             16        24    0    0 00:00:09 Estab   1      1
  x2                       10.1.0.6 4 65101             16        22    0    0 00:00:04 Estab   1      1
```

You can also inspect the TCP-AO details on some network devices. This is what Arista EOS displays as part of the **show ip bgp neighbor** command:

```
rtr#show ip bgp neighbors 10.1.0.2|section TCP-AO
TCP-AO Authentication:
  Profile: x1
  MAC algorithm: hmac-sha1-96
  Current key ID: 0
  Next receive key ID: 0
  Active receive key IDs: 0
```
