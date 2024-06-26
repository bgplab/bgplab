# Configuring Cumulus Linux and FRRouting

Most networking devices[^CL] use a configuration command line interface (CLI) to interact with the end-user. The CLI usually provides **show** commands to inspect the state of the device and a configuration mode that allows the user to configure the device.

[^CL]: Including devices based on Linux like Arista EOS, Cisco Nexus OS, or Nokia SR Linux

Cumulus Linux and FRRouting are different. They are implemented as an application/management layer on top of Linux and use Linux shell as the initial CLI. To configure them, you have to:

* Use standard Linux tools like *ifupdown* to configure the interfaces;
* [Edit FRRouting configuration files](#daemon) to start routing protocol daemons
* [Start FRRouting configuration shell](#vtysh) from the Linux CLI.

The Linux interfaces and IP addresses will be configured automatically if you start the BGP labs with the **netlab up** command. You will have to start the routing protocol daemons if you plan to use Cumulus Linux or FRRouting as the user routers, and you might have to execute **show** commands on Cumulus Linux or FRRouting acting as the external routers. You'll practice both in this lab exercise.

![Lab topology](topology-session.png)

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `basic/0-frrouting`
* Execute **netlab up** to start a lab with two Cumulus Linux or FRR virtual machines or containers (depending on your lab setup).

!!! tip
    The lab topology uses Cumulus Linux virtual machines or containers but switches to FRR containers if you're running the labs on an ARM CPU (for example, on [Macbooks using Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)).

* Log into the devices (`rtr` and `x1`) with the **netlab connect** command.

## Start the BGP Daemon {#daemon}

Most network devices start routing daemons when you configure them through the configuration CLI or API. FRRouting (the routing daemons used in Cumulus Linux) is different: you have to enable the desired routing daemons in a configuration file and restart the top-level FRRouting process.

!!! tip
    You can skip this step if you use NVUE CLI to configure routing on Cumulus Linux 5.x -- it automatically enables FRR daemons before configuring them.

!!! warning
    You cannot restart the top-level FRRouting process in an FRR container. When you use FRRouting containers in your labs, _netlab_ always enables the BGP daemon.

You can check the FRR daemons running on your device with the `ps -ef|grep frr` command. This is the printout you could get before enabling the BGP daemon:

```
rtr(bash)#ps -ef|grep frr
frr       1827     1  0 10:46 ?        00:00:00 /usr/lib/frr/zebra -d -F datacenter -M cumulus_mlag -M snmp -A 127.0.0.1 -s 90000000
frr       1841     1  0 10:46 ?        00:00:00 /usr/lib/frr/staticd -d -F datacenter -A 127.0.0.1
root      2291     1  0 10:46 ?        00:00:00 /usr/lib/frr/watchfrr -d -F datacenter zebra staticd
root      2340  2325  0 10:47 pts/1    00:00:00 grep frr
```

To enable the FRRouting BGP daemon, you have to:

* Add the `bgpd=yes` line to the `/etc/frrouting/daemons` file.
* Restart FRRouting with the `sudo systemctl restart frr.service` command (see also: [using sudo](#sudo))

!!! tip
    See [Configuring FRRouting](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-41/Layer-3/Configuring-FRRouting/) Cumulus Linux documentation for more details.

You could add the required line to the FRRouting daemons file with any text editor or use the following trick:

* Use **sudo bash** to start another Linux shell as the root user
* Use the **echo** command with output redirection to add a line to the `/etc/frrrouting/daemons` file.

```
rtr(bash)#sudo bash
root@rtr:/# echo 'bgpd=yes' >>/etc/frr/daemons
root@rtr:/# exit
```

After enabling the BGP daemon and restarting FRR, you should see the `bgpd` process in the `ps -ef` printout:

```
root      2543     1  0 10:52 ?        00:00:00 /usr/lib/frr/watchfrr -d -F datacenter zebra bgpd staticd
frr       2566     1  0 10:52 ?        00:00:00 /usr/lib/frr/zebra -d -F datacenter -M cumulus_mlag -M snmp -A 127.0.0.1 -s 90000000
frr       2580     1  0 10:52 ?        00:00:00 /usr/lib/frr/bgpd -d -F datacenter -M snmp -A 127.0.0.1
frr       2586     1  0 10:52 ?        00:00:00 /usr/lib/frr/staticd -d -F datacenter -A 127.0.0.1
root      2594  2325  0 10:52 pts/1    00:00:00 grep frr
```

## Work with the FRRouting CLI {#vtysh}

FRRouting suite includes a virtual shell (*vtysh*) closely resembling industry-standard CLI[^ISC]. It has to be started from the Linux command line with the vtysh command. The `vtysh` CLI has to run as the root user unless you change the FRR-related permissions to allow a regular user to use it. The usual command to start the _vtysh_ is thus `sudo vtysh` (but see also [To Sudo Or Not to Sudo](#sudo)).

[^ISC]: An euphemism for *Cisco IOS CLI* that is used when you try to avoid nasty encounters with Cisco's legal team.

```
rtr(bash)#sudo vtysh

Hello, this is FRRouting (version 7.5+cl4.4.0u4).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

rtr#
```

Once you started _vtysh_, you can execute **show** commands to inspect the device state, for example:

```
x1(bash)#sudo vtysh

Hello, this is FRRouting (version 7.5+cl4.4.0u4).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

x1# show ip bgp
BGP table version is 1, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.2/32      0.0.0.0                  0         32768 i

Displayed  1 routes and 1 total paths
```

!!! tip
    Starting with _netlab_ release 1.7.0, you can use the `--show` option of the **netlab connect** command to execute a single command on a FRR/Cumulus Linux device. For example, to inspect the BGP table, use `netlab connect --show ip bgp`.

To configure FRRouting daemons, use the **configure** _vtysh_ command and enter configuration commands similar to those you'd use on Cisco IOS or Arista EOS:

```
x1(bash)#sudo vtysh

Hello, this is FRRouting (version 7.5+cl4.4.0u4).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

x1# configure
x1(config)# router bgp 65100
x1(config-router)#
```

## To Sudo Or Not to Sudo {#sudo}

The _vtysh_ usually has to run as the **root** user, so you should start it with the `sudo vtysh` command. Unfortunately, things are never as simple as they look:

* When using SSH, you log into Cumulus Linux or FRRouting virtual machines as a regular user (user *vagrant* in _netlab_-created labs) and have to use the `sudo` command to start _vtysh_.
* Cumulus Linux and FRR containers run as the **root** user, and you connect to them as the **root** user with the `docker exec` or `netlab connect` commands. When working with containers, you can start _vtysh_ without using the `sudo` command.
* You can execute `sudo vtysh` as a root user on Cumulus Linux, but not within an FRR container -- the FRR container does not include the **sudo** command.

**Long story short:**

* Use `sudo vtysh` whenever possible to burn it into your muscle memory.
* Use `vtysh` if you use FRRouting containers as the lab devices.

## Using Output Filters

Unlike many other network operating systems, FRR `vtysh` does not have output filters. You probably don't need them as you'll be running FRR on top of a Unix-like operating system that supports pipes, but it might be a bit convoluted to use `vtysh` in a pipe.

To use the `vtysh` output in a pipe, you have to execute `vtysh` and get the results of a **show** command in a single command:

* You could use `sudo vtysh -c 'show command'` when you're in the **bash** shell of a lab device, for example:

```
$ sudo vtysh -c 'show ip bgp' | grep 32768
*> 192.168.100.0/24 0.0.0.0                  0         32768 i
```

* Alternatively, you could use the `netlab connect --show` command to execute a `vtysh` **show** command on a lab device:

```
$ netlab connect x1 --show ip bgp | grep 32768
Connecting to container clab-originate-x1, executing sudo vtysh -c "show ip bgp"
*> 192.168.100.0/24 0.0.0.0                  0         32768 i
```

!!! tip
    Use `netlab connect --quiet --show` to omit the `Connecting to...` message.

The following table contains a mapping between common network operating system filters and Linux CLI commands:

| NOS filter | Linux CLI command |
|------------|-------------------|
| `include`  | `grep`            |
| `exclude`  | `grep -v`         |
| `begin`    | `grep -A 10000`[^SLN]   |
| `end`      | `grep -B 10000`   |
| `section`  | *no equivalent*   |

[^SLN]: The '10000' parameter specifies the number of lines after the match. Increase it for very long printouts ;)
