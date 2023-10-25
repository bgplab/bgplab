# Manual Setup

You don't have to use _[netlab](https://netlab.tools)_ to create your labs; you can build them with any other tool, or use physical devices or a mix of physical- and virtual devices.

## Lab Topologies

Lab instructions contain wiring tables that you can use to set up your infrastructure, and I tried to use the same setup for as many labs as possible to reduce your hassle. For the moment, all exercises use the 4-router lab.

## External BGP Routers

The labs rely on preconfigured external BGP routers using Cumulus Linux. They are automatically configured by _netlab_; if you decide to use some other infrastructure you'll have to configure them yourself.

Lab directories in the [GitHub repository](https://github.com/bgplab/bgplab) contain `config` subdirectory with `/etc/frr/frr.conf` and `/etc/network/interfaces` files. I would use `git clone` to clone the GitHub repository to the local disk; GitHub also offers ZIP download. If you prefer point-and-click approach feel free to download individual files from the GitHub web UI. Finally, you could use `curl` on Cumulus Linux to pull them into the devices straight from GitHub.

Whatever you decide to do, in the end you have to get the configuration files to individual Cumulus Linux devices, reconfigure interfaces with `ifreload -a`, and restart FRR.

## Initial Device Configurations

When using _netlab_, you'll get IP addressing configured on your devices. Most labs (apart from the _configure BGP sessions_ ones) also configure basic BGP setup on your devices. Without _netlab_ you'll have to start from scratch; the information you need is in the lab instructions but it might become tedious.

**Long story short:** Use *netlab* 😉