# Implement Anycast Services with BGP

In this lab exercise, you'll build a DNS server farm with multiple servers connected to the same layer-3 access switch[^DFNR]. 

![Lab topology](topology-anycast.png)

[^DFNR]: A device formerly known as _router_

Enterprise architects would recommend using a load balancer in a typical scale-out architecture. As DNS is connectionless[^UDP] and has no concept of sessions, we don't need a load balancer; equal-cost multipathing on the access switch will do the job just fine.

[^UDP]: We're assuming UDP-based DNS. Implementing TCP-based services with anycast is more complex but doable; many large-scale web properties use anycast web servers.

Regardless of the underlying load balancing mechanism, the solution must track individual servers' health and availability. In our design[^UEW], we'll use BGP to track server availability. All servers will advertise the same IP address[^HP] to the access switch and offer DNS services on that IP address[^SDNS].

[^UEW]: This design is used in many large-scale DNS implementations.

[^HP]: Technically, a /32 IPv4 or a /128 IPv6 prefix

[^SDNS]: We won't go as far as configuring the DNS servers. We'll declare *mission accomplished* as soon as we ping the anycast IP address.

<!--
!!! Expert
    This is an expert-level challenge lab -- you are on your own. Good luck and Godspeed!
-->
!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.