---
title: Installation and Setup
---
# Software Installation and Lab Setup

It's easiest to use the BGP labs with _[netlab](https://netlab.tools/)_, but you can use most of them (potentially with slightly reduced functionality) with any other virtual lab environment or on physical gear. For the rest of this document we'll assume you decided to use _netlab_; if you want to set up your lab in some other way you might find the [Manual Setup](external/index.md) document useful.

## Selecting the Network Devices

The labs heavily rely on external BGP feeds -- preconfigured devices that you have to connect to and exchange routing information with. It's best if you run Cumulus Linux on those devices; if you insist on using something else we'd appreciate if you would consider submitting your configurations in a pull request.

You can run Cumulus Linux in all [_netlab_-supported virtualization environments](https://netlab.tools/providers/) (VirtualBox, libvirt or Docker), and  if you want to keep your life simple consider using it for your devices as well. Obviously you can use any other [_netlab_-supported device](https://netlab.tools/platforms/) for which we implemented [basic BGP configuration](https://netlab.tools/module/bgp/#platform-support).

## Selecting the Virtualization Environment

Now that you know which network device you want to use, check [which virtualization environment](https://netlab.tools/platforms/#supported-virtualization-providers) you can use. I would prefer _containerlab_ over _libvirt_ with _virtualbox_ being a distant third, but that's just me.

There's a gotcha though: you can use _containerlab_ and _libvirt_ only on a Linux host. You can use _virtualbox_ if you want to run the labs on your Windows- or MacOS laptop, or run a Ubuntu VM on the laptop.

One more gotcha: your hardware and virtualization software (example: VirtualBox or VMware Fusion) must support _nested virtualization_ if you want to use _libvirt_ on that Ubuntu VM. You don't need that to run Docker containers, unless you're using the crazy trick we're forced to use for Juniper vMX or Nokia SR OS -- they're running as a virtual machine _within a container_.

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
* Clone the `bgplab` [GitHub repository](https://github.com/ipspace/bgplab) with `git clone git@github.com:ipspace/bgplab.git`. [GitHub UI](https://github.com/ipspace/bgplab) gives you other options in the green `Code` button, including _Download ZIP_
* Open the `defaults.yml` file in the main directory and edit it to set your preferred network device and virtualization environment. For example, I'm using the following settings to run the labs with Arista EOS containers:

```
device: eos         # Change to your preferred network device
provider: clab      # Change to virtualbox or libvirt if needed
```

* In a terminal window, change current directory to one of the lab directories (for example, `basic/1-session`) and execute **netlab up**.
* Wait for the lab to start and use **netlab connect** to connect to individual lab devices
* Have fun.
* When you're done, collect the device configurations with **netlab collect** (if you want to save them) and shut down the lab with **netlab down**
