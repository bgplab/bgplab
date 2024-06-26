# EBGP-Only Data Center Design

In this lab exercise, you'll build a modern layer-3-only leaf-and-spine data center fabric using EBGP as the sole routing protocol within the fabric and between the leaf (top-of-rack) switches and the servers.

![Lab topology](topology-ebgp-dc.png)

The fabric you'll build has these characteristics:

* It has no VLANs. All links are point-to-point layer-3 links.
* It supports only IPv6. Implementing a single layer-3 protocol within the data center and having multiprotocol address translation (NAT64) or proxy web servers at the data center edge is more manageable than running a dual-stack fabric.
* Point-to-point links have only IPv6 link-local addresses.
* The fabric uses EBGP as the only routing protocol. EBGP sessions are established between IPv6 link-local addresses.
* The fabric uses EBGP to implement redundant server connectivity. Servers use EBGP to advertise their loopback addresses to adjacent leaf switches.

!!! Expert
    This is an expert-level challenge lab -- you are on your own. Good luck and Godspeed!

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.
