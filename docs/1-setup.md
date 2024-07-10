---
title: Installation and Setup
---
# Software Installation and Lab Setup

It's easiest to use the BGP labs with _[netlab](https://netlab.tools/)_. Still, you can use most of them (potentially with slightly reduced functionality) with any other virtual lab environment or on physical gear. For the rest of this document, we'll assume you decided to use _netlab_; if you want to set up your lab in some other way, read the [Manual Setup](external/index.md) document.

!!! Warning
    BGP labs work best with _netlab_ release 1.8.3 or later. If you're using an earlier _netlab_ release, please upgrade with `pip3 install --upgrade networklab`.

## Select the Network Devices You Will Work With

Cumulus Linux and FRRouting devices can be run in all [_netlab_-supported virtualization environments](https://netlab.tools/providers/) (VirtualBox, libvirt, or Docker), and if you want to start practicing BGP with minimum hassle, consider using it for all lab devices. Use FRR on the ARM CPU (for example, [Macbooks with Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)).

If you'd like to use a more traditional networking device, use any other [_netlab_-supported device](https://netlab.tools/platforms/) for which we implemented [basic BGP configuration](https://netlab.tools/module/bgp/#platform-support) as the device to practice with[^x86]. I recommend Arista cEOS or Nokia SR Linux containers; they are the easiest ones to install and use.

!!! tip
    You must use container-based network devices like Arista cEOS, Cumulus Linux, FRR, Nokia SR Linux, or Vyos if you plan to run the BGP labs in [GitHub Codespaces](4-codespaces.md). 

[^x86]: You will have to run the labs on a device with an x86 CPU (Intel or AMD).

## Select the Additional Devices in Your Lab

The labs heavily rely on external BGP feeds -- preconfigured devices with which your routers exchange routing information. You won't configure those devices, but you might have to log into them and execute **show** commands.

Use Cumulus Linux on those devices with _netlab_ releases older than 1.6.4.

With release 1.6.4 (and later), you can choose any one of these devices for your external BGP feeds[^OPL]:

| Environment | Devices that can be used<br>as external BGP feeds[^XF] | Recommended |
|-------------------|--------------------------------|-----|
| Containers (clab) | Arista EOS, Aruba AOS-CX, Cumulus Linux, FRR, Nokia SR Linux[^R164] | FRR (`frr`)[^FSF] |
| Virtual machines (libvirt) | Arista EOS, Aruba AOS-CX, Cisco IOSv, Cisco IOS-XE, Cumulus Linux, FRR | Cumulus Linux (`cumulus`)[^CSF] |
| Virtual machines (Virtualbox) | Arista EOS, Cisco IOSv, Cisco IOS-XE, Cumulus Linux, FRR | Cumulus Linux (`cumulus`) |
| [ARM (Apple) CPU](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html) | FRR containers | FRR (`frr`) |

!!! Tip
    * Several more complex labs require additional configuration on the external routers. That configuration is usually available for Arista EOS, Cumulus Linux, and FRR.
    * Each lab description contains specific *device requirements* section. Consult those if you want to use less-popular devices in your labs.

[^XF]: You can only use devices supported by **[bgp.session](https://netlab.tools/plugins/bgp.session/)** and **[bgp.policy](https://netlab.tools/plugins/bgp.policy/)** _netlab_ plugins as external BGP feeds.

[^R164]: You need _netlab_ release 1.6.4-post2 or later to use Nokia SR Linux as additional routers in more complex labs. To configure Nokia SR Linux, you must also [install additional software](https://netlab.tools/caveats/#caveats-srlinux).

[^OPL]: If you'd like to use other devices as external BGP feeds and are willing to contribute your changes, please add the support for your devices to **bgp.session** and **bgp.policy** plugins. Thank you!

[^FSF]: An FRR container starts slightly faster than a Cumulus Linux container. Also, the FRR containers are built by the FRR project, while the Cumulus Linux containers came from a hobby project of their former employee.

[^CSF]: There is no official FRR virtual machine image -- _netlab_ has to download and install FRR on a Ubuntu VM whenever you start an `frr` node as a virtual machine. Using Cumulus Linux Vagrant box is faster and consumes way less bandwidth.

## Select the Virtualization Environment

Now that you know which network device to use, check [which virtualization environment](https://netlab.tools/platforms/#supported-virtualization-providers) you can use. I would prefer _containerlab_ over _libvirt_ with _virtualbox_ being a distant third, but that's just me.

!!! tip
    You can also run the BGP labs in a [free GitHub Codespace](4-codespaces.md).

A gotcha: You can use _virtualbox_ if you want to run the lab devices as virtual machines on your Windows- or MacOS laptop with Intel CPU, but even then, I'd prefer running them in a [Ubuntu VM](https://netlab.tools/install/ubuntu-vm/).

One more gotcha: your hardware and virtualization software (for example, VirtualBox or VMware Fusion) must support _nested virtualization_ if you want to use _libvirt_ on that Ubuntu VM. You don't need nested virtualization to run Docker containers unless you're using the crazy trick we're forced to use for Aruba AOS-CX, Juniper vMX, or Nokia SR OS -- they're running as a virtual machine _within a container_.

## Software Installation

Based on the choices you made, you'll find the installation instructions in one of these documents:

* [Using GitHub Codespaces](4-codespaces.md)
* [Ubuntu VM Installation](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS
* [Ubuntu Server Installation](https://netlab.tools/install/ubuntu/)
* [Running netlab on any other Linux Server](https://netlab.tools/install/linux/)
* [Running netlab in a Public Cloud](https://netlab.tools/install/cloud/)
* [Running netlab on Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)
* Discouraged: [Virtualbox-Based Lab on Windows or MacOS](https://netlab.tools/labs/virtualbox/)

Once you have completed the software installation you have to deal with the stupidities of downloading and installing network device images ([Virtualbox](https://netlab.tools/labs/virtualbox/), [libvirt](https://netlab.tools/labs/libvirt/#vagrant-boxes), [containers](https://netlab.tools/labs/clab/#container-images)) unless you decided to use Cumulus Linux, FRR, Nokia SR Linux, or Vyos.

I would love to simplify the process, but the networking vendors refuse to play along. Even worse,  their licenses prohibit me from downloading the images and creating a packaged VM with preinstalled network devices for you[^NPAL]. Fortunately, you only have to go through this colossal waste of time once.

[^NPAL]: I'm not going to pay a lawyer to read their boilerplate stuff, and I'm definitely not going to rely on my amateur understanding of US copyright law.

## Setting Up the Labs {#defaults}

We finally got to the fun part -- setting up the labs. If you're not using GitHub Codespaces:

* Select a directory where you want to have the BGP labs
* Clone the `bgplab` [GitHub repository](https://github.com/bgplab/bgplab) with `git clone https://github.com/bgplab/bgplab.git`. [GitHub UI](https://github.com/bgplab/bgplab) gives you other options in the green `Code` button, including _Download ZIP_

After you get a local copy of the repository:

* If needed, edit the `defaults.yml` file in the top directory to set your preferred network device and virtualization environment. For example, I'm using the following settings to run the labs with Arista EOS containers while using FRR as the external BGP feeds:

```
device: eos             # Change to your preferred network device
provider: clab          # Change to virtualbox or libvirt if needed

groups:
  external:
    device: frr         # Change to your preferred external router
```

* In a terminal window, change the current directory to one of the lab directories (for example, `basic/1-session`), and execute **netlab up**.
* Wait for the lab to start and use **netlab connect** to connect to individual lab devices
* Have fun.
* When you're done, collect the device configurations with **netlab collect** (if you want to save them) and shut down the lab with **netlab down**
* Change the current directory to another lab directory and repeat.
* Once you run out of lab exercises, create a new one and contribute it with a pull request ;)
