# IBGP Load Balancing with BGP Additional Paths

In the [previous lab exercise](3-ibgp.md), you implemented IBGP load balancing across prefixes received by two WAN edge routers. The load balancing worked because you did not use BGP route reflectors in your autonomous system. Like any other BGP router, BGP route reflectors send *their best routes* to their clients; in your network, the IBGP clients of the BGP route reflector receive a single path to the external prefix.

![Lab topology](topology-ibgp-add-path.png)

You can use the *BGP Additional Paths* functionality to make the BGP route reflector send more than one best path to its clients, resulting in IBGP load balancing on BGP route reflector clients. You'll practice that in this lab exercise.

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.