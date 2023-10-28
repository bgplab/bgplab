---
title: Installation and Setup
---
# Software Installation and Lab Setup

It's easiest to use the BGP labs with _[netlab](https://netlab.tools/)_, but you can use most of them (potentially with slightly reduced functionality) with any other virtual lab environment or on physical gear. For the rest of this document we'll assume you decided to use _netlab_; if you want to set up your lab in some other way you might find the [Manual Setup](external/index.md) document useful.

!!! Warning
    BGP labs work best with _netlab_ release 1.6.4 or later. If you're using an earlier _netlab_ release, please upgrade with `pip3 install --upgrade networklab`.

## Selecting the Network Devices

The labs heavily rely on external BGP feeds -- preconfigured devices that you have to connect to and exchange routing information with. Use Cumulus Linux on those devices if you're running a _netlab_ release prior to 1.6.4.

With release 1.6.4 (and later) you can choose any one of these devices for your external BGP feeds[^OPL]:

| Environment | Devices that can be used<br>as external BGP feeds[^XF] | Recommended |
|-------------------|--------------------------------|-----|
| Containers (clab) | Arista EOS, Aruba AOS-CX, Cumulus Linux, FRR, Nokia SR Linux[^R164] | FRR (`frr`)[^FSF] |
| Virtual machines (libvirt) | Arista EOS, Aruba AOS-CX, Cisco IOSv, Cisco IOS-XE, Cumulus Linux, FRR | Cumulus Linux (`cumulus`)[^CSF] |
| Virtual machines (Virtualbox) | Arista EOS, Cisco IOSv, Cisco IOS-XE, Cumulus Linux, FRR | Cumulus Linux (`cumulus`) |

[^XF]: You can only use devices supported by **[bgp.session](https://netlab.tools/plugins/bgp.session/)** and **[bgp.policy](https://netlab.tools/plugins/bgp.policy/)** _netlab_ plugins as external BGP feeds.

[^R164]: You need _netlab_ release 1.6.4-post2 to use Nokia SR Linux as additional routers in more complex labs. You will also need to [install additional software](https://netlab.tools/caveats/#caveats-srlinux) to configure Nokia SR Linux.

[^OPL]: If you'd like to use other devices as external BGP feeds and are willing to contribute your changes, please add the support for your devices to **bgp.session** and **bgp.policy** plugins. Thank you!

[^FSF]: An FRR container starts slightly faster than a Cumulus Linux container. Also, the FRR containers are built by the FRR project, while the Cumulus Linux containers are a result of a hobby project of their former employee.

[^CSF]: There is no official FRR virtual machine image -- _netlab_ has to download and install FRR on a Ubuntu VM every time you start an `frr` node as a virtual machine. Using Cumulus Linux Vagrant box is faster and consumes way less bandwidth.

You can run Cumulus Linux (and FRR) in all [_netlab_-supported virtualization environments](https://netlab.tools/providers/) (VirtualBox, libvirt or Docker), and if you want to start practicing BGP with minimum hassle consider using it for all lab devices. Obviously you can use any other [_netlab_-supported device](https://netlab.tools/platforms/) for which we implemented [basic BGP configuration](https://netlab.tools/module/bgp/#platform-support) as the device to practice with.

## Selecting the Virtualization Environment

Now that you know which network device you want to use, check [which virtualization environment](https://netlab.tools/platforms/#supported-virtualization-providers) you can use. I would prefer _containerlab_ over _libvirt_ with _virtualbox_ being a distant third, but that's just me.

There's a gotcha though: you can use _containerlab_ and _libvirt_ only on a Linux host. You can use _virtualbox_ if you want to run the lab devices as virtual machines on your Windows- or MacOS laptop, but even then I'd prefer running them in a [Ubuntu VM running on the laptop](https://netlab.tools/install/ubuntu-vm/).

One more gotcha: your hardware and virtualization software (example: VirtualBox or VMware Fusion) must support _nested virtualization_ if you want to use _libvirt_ on that Ubuntu VM. You don't nested virtualization to run Docker containers, unless you're using the crazy trick we're forced to use for Aruba AOS-CX, Juniper vMX or Nokia SR OS -- they're running as a virtual machine _within a container_.

## Software Installation

Based on the choices you made, you'll find the installation instructions in one of these documents:

* [Virtualbox-Based Lab on Windows or MacOS](https://netlab.tools/labs/virtualbox/)
* [Ubuntu VM Installation](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS
* [Ubuntu Server Installation](https://netlab.tools/install/ubuntu/)
* [Running netlab on any other Linux Server](https://netlab.tools/install/linux/)
* [Running netlab in a Public Cloud](https://netlab.tools/install/cloud/)

Once you completed the software installation you have to deal with the stupidities of downloading and installing network device images ([Virtualbox](https://netlab.tools/labs/virtualbox/), [libvirt](https://netlab.tools/labs/libvirt/#vagrant-boxes), [containers](https://netlab.tools/labs/clab/#container-images)) unless you decided to use Cumulus Linux, FRR, Nokia SR Linux, or Vyos.

I would love to make the whole process simpler, but the networking vendors refuse to play along. Even worse, it looks like[^NPAL] their licenses prohibit me from downloading the images and creating a packaged VM with preinstalled network devices for you. Fortunately, you only have to go through this colossal waste of time once.

[^NPAL]: I'm not going to pay a lawyer to read their boilerplate stuff, and I'm definitely not going to rely on my amateur understanding of US copyright law.

## Setting Up the Labs

We finally got to the fun part -- setting up the labs:

* Select a directory where you want to have the BGP labs
* Clone the `bgplab` [GitHub repository](https://github.com/bgplab/bgplab) with `git clone git@github.com:bgplab/bgplab.git`. [GitHub UI](https://github.com/bgplab/bgplab) gives you other options in the green `Code` button, including _Download ZIP_
* Open the `defaults.yml` file in the main directory and edit it to set your preferred network device and virtualization environment. For example, I'm using the following settings to run the labs with Arista EOS containers while using FRR as the external BGP feeds:

```
device: eos             # Change to your preferred network device
provider: clab          # Change to virtualbox or libvirt if needed

groups:
  external:
    device: frr         # Change to your preferred external router
```

* In a terminal window, change current directory to one of the lab directories (for example, `basic/1-session`), and execute **netlab up**.
* Wait for the lab to start and use **netlab connect** to connect to individual lab devices
* Have fun.
* When you're done, collect the device configurations with **netlab collect** (if you want to save them) and shut down the lab with **netlab down**
* Change current directory to another lab directory and repeat.
* Once you run out of lab exercises, create a new one and contribute it with a pull request ;)
