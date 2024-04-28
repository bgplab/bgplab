# IBGP Load Balancing with BGP Link Bandwidth

In the [previous lab exercise](2-dmz-bw.md), you used the BGP Link Bandwidth extended community to implement unequal-cost load balancing across multiple links connected to the same router. In this exercise, you'll use the same approach but extend it across your autonomous system — routers receiving external routes over IBGP should perform unequal-cost multipathing (UCMP) toward external destinations based on the BGP Link Bandwidth extended community attached to BGP paths.

![Lab topology](topology-lb-ibgp-dmz-bw.png)

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.