# Using Bird BGP Daemon as a BGP Route Reflector

In a previous lab exercise, you used BGP route reflectors on core routers to reduce the number of IBGP sessions in your network. BGP route reflection is a pure control plane functionality and does not have to run on a router (or a layer-3 switch). In this lab, you'll use the Bird BGP daemon as a BGP route reflector.

![Lab topology](topology-bird-rr.png)

!!! Expert
    This is an expert-level challenge lab. We expect you to know what you're doing -- all you'll get from us are a few basic Bird setup tricks and the verification guidelines.

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.