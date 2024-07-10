# Reduce BGP Table Size on Provider Edge Routers

The global Internet BGP routing table has close to a million entries, and even though most of them use the same small set of exit point, you still have to store them in the forwarding tables of your routers, making your devices more expensive than necessary.

A smarter design would use default routing toward the network core and store only the locally-significant routes on the routers facing the end-customers. You would still have to use expensive gear for the core routers and devices peering with upstream Service Provider, but could use more optimized equipment on the customer-facing devices.

![Lab topology](topology-table-size.png)

That sounds like a great plan until you get a customer who wants to receive the whole global BGP routing table, forcing you to have that information on your PE-routers. While you could 

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.

<!--    
!!! Expert
    This is an expert-level challenge lab -- you are on your own. Good luck and Godspeed!
-->