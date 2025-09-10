---
title: Installation and Setup
---
# Software Installation and Lab Setup

It's easiest to use the BGP labs with _[netlab](https://netlab.tools/)_. Still, you can use most of them (potentially with slightly reduced functionality) with any other virtual lab environment or on physical gear. For the rest of this document, we'll assume you decided to use _netlab_; if you want to set up your lab in some other way, read the [Manual Setup](external/index.md) document.

!!! Warning
    While BGP labs work with _netlab_ release 1.8.3 or later, we recommend using a recent release (for example, 25.09). If you're using an earlier _netlab_ release, please upgrade with `pip3 install --upgrade networklab`.

## Select the Network Devices You Will Work With

FRRouting devices can be run in all [_netlab_-supported virtualization environments](https://netlab.tools/providers/) (Docker containers or KVM/libvirt virtual machines), and if you want to start practicing BGP with minimum hassle, consider using them for all lab devices.

If you'd like to use a more traditional networking device, use any other [_netlab_-supported device](https://netlab.tools/platforms/) for which we implemented [basic BGP configuration](https://netlab.tools/module/bgp/#platform-support) as the device to practice with[^x86]. I recommend Arista cEOS or Nokia SR Linux containers; they are the easiest ones to install and use.

!!! tip
    You must use container-based network devices such as Arista cEOS, FRR, Nokia SR Linux, or VyOS to run the BGP labs in [GitHub Codespaces](4-codespaces.md).

[^x86]: You will have to run the labs on a device with an x86 CPU (Intel or AMD).

## Select the Additional Devices in Your Lab

The labs heavily rely on external BGP feeds -- preconfigured devices with which your routers exchange routing information. You won't configure those devices, but you might have to log into them and execute **show** commands.

It's best if you use FRR containers or virtual machines for external BGP feeds, but you can choose any one of these devices[^OPL]:

| Environment | Devices that can be used<br>as external BGP feeds[^XF] |
|-------------------|--------------------------------|
| Containers (clab) | Arista EOS, FRR, Nokia SR Linux[^R164] |
| Virtual machines (libvirt) | Arista EOS, Aruba AOS-CX, Cisco IOSv, Cisco IOS-XE, FRR |
| [ARM (Apple) CPU](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html) | Arista EOS, FRR, or SR Linux containers |

!!! Tip
    * Several more complex labs require additional configuration on the external routers. That configuration is usually available for Arista EOS and FRR.
    * Each lab description contains specific *device requirements* section. Consult those if you want to use less-popular devices in your labs.

[^XF]: You can only use devices supported by **[bgp.session](https://netlab.tools/plugins/bgp.session/)** and **[bgp.policy](https://netlab.tools/plugins/bgp.policy/)** _netlab_ plugins as external BGP feeds.

[^R164]: You must [install additional software](https://netlab.tools/caveats/#caveats-srlinux) to configure Nokia SR Linux.

[^OPL]: If you'd like to use other devices as external BGP feeds and are willing to contribute your changes, please add the support for your devices to **bgp.session** and **bgp.policy** plugins. Thank you!

## Select the Virtualization Environment

Now that you know which network device to use, check [which virtualization environment](https://netlab.tools/platforms/#supported-virtualization-providers) you can use. I prefer _containerlab_ over _libvirt_ (containers usually start faster), but that's just me.

!!! tip
    You can also run the BGP labs in a [free GitHub Codespace](4-codespaces.md).

Everything else being equal, I'd create a [Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS (including [Macs with Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/)) to run _netlab_. You could also invest in a tiny brick of densely-packed silicon ([example](https://www.minisforum.com/)).

A gotcha: your hardware and virtualization software (for example, VirtualBox or VMware Fusion) must support _nested virtualization_ if you want to use _libvirt_ on that Ubuntu VM. You don't need nested virtualization to run Docker containers unless you're using the crazy trick we're forced to use for Aruba AOS-CX, most Cisco platforms, Junos, or Nokia SR OS -- they're running as a virtual machine _within a container_.

## Software Installation

Based on the choices you made, you'll find the installation instructions in one of these documents:

* [Using GitHub Codespaces](4-codespaces.md)
* [Ubuntu VM Installation](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS
* [Ubuntu Server Installation](https://netlab.tools/install/ubuntu/)
* [Running netlab on any other Linux Server](https://netlab.tools/install/linux/)
* [Running netlab in a Public Cloud](https://netlab.tools/install/cloud/)
* [Running netlab on Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)

Once you have completed the software installation, you have to deal with the stupidities of downloading and installing network device images ([libvirt](https://netlab.tools/labs/libvirt/#vagrant-boxes), [containers](https://netlab.tools/labs/clab/#container-images)) unless you decided to use FRR, Nokia SR Linux, or Vyos.

I would love to simplify the process, but the networking vendors refuse to play along. Even worse, their licenses prohibit me from downloading the images and creating a packaged VM with preinstalled network devices for you[^NPAL]. Fortunately, you only have to go through this colossal waste of time once.

[^NPAL]: I'm not going to pay a lawyer to read their boilerplate stuff, and I'm definitely not going to rely on my amateur understanding of US copyright law.

## Setting Up the Labs {#defaults}

We finally got to the fun part -- setting up the labs. If you're not using GitHub Codespaces:

* Select a directory where you want to have the BGP labs
* Clone the `bgplab` [GitHub repository](https://github.com/bgplab/bgplab) with `git clone https://github.com/bgplab/bgplab.git`. [GitHub UI](https://github.com/bgplab/bgplab) gives you other options in the green `Code` button, including _Download ZIP_

After you get a local copy of the repository:

* Change the directory to the top directory of the cloned repository[^BLB].
* Verify the current project defaults with the `netlab defaults --project` command[^R27]:

```
$ netlab defaults --project
device = frr (project)
groups.external.device = frr (project)
provider = clab (project)
```

[^BLB]: `bgplab` if you used the simple version of the **git clone** command

[^R27]: Available in _netlab_ release 2.0.1 and later. Edit the `defaults.yml` file if you're using an older release.

[^CSR]: Assuming you built the [CSR Vagrant box](https://netlab.tools/labs/csr/) first

* If needed, change the project defaults to match your environment with the `netlab defaults --project _setting_=_value_` command or edit the `defaults.yml` file with a text editor like `vi` or `nano`. For example, use these commands to change your devices to Cisco CSRs running as virtual machines[^CSR]:

```shell
$ netlab defaults --project device=csr
The default setting device is already set in project defaults
Do you want to change that setting in project defaults [y/n]: y
device set to csr in /home/user/BGP/defaults.yml

$ netlab defaults --project provider=libvirt
The default setting provider is already set in netlab,project defaults
Do you want to change that setting in project defaults [y/n]: y
provider set to libvirt in /home/user/BGP/defaults.yml
```

* In a terminal window, change the current directory to one of the lab directories (for example, `basic/1-session`), and execute **netlab up**.
* Wait for the lab to start and use **netlab connect** to connect to individual lab devices
* Have fun.
* When you're done, collect the device configurations with **netlab collect** (if you want to save them) and shut down the lab with **netlab down**
* Change the current directory to another lab directory and repeat.
* Once you run out of lab exercises, create a new one and contribute it with a pull request ;)
