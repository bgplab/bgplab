# Manual Setup

You don't have to use _[netlab](https://netlab.tools)_ to create your labs; you can build them with any other tool, or use physical devices or a mix of physical- and virtual devices.

## Lab Topologies

Lab instructions contain wiring tables that you can use to set up your infrastructure, and I tried to use the same setup for as many labs as possible to reduce your hassle. For the moment, all exercises use the 4-router lab.

## External BGP Routers

The labs rely on preconfigured external BGP routers. They are automatically configured by _netlab_; if you decide to use some other infrastructure, you'll have to configure them yourself.

## Initial Device Configurations

When using _netlab_, you'll get IP addressing configured on your devices. Most labs (apart from the _configure BGP sessions_ ones) also configure basic BGP setup on your devices. Without _netlab_ you'll have to start from scratch; the information you need is in the lab instructions, but it might become tedious.

**Long story short:** Use *netlab* 😉
