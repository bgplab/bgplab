# BGP Session Templates

In the _[Use BGP Route Reflectors](../ibgp/3-rr.md)_ exercise, you had to configure numerous IBGP neighbors on BGP route servers. All the neighbor configurations were identical; you had to:

* Specify the source interface for the IBGP session;
* Set the remote AS number to be equal to the local AS number;
* Configure the neighbor as a route reflector client.

Wouldn't it be great if you could configure all those parameters in another configuration object and then apply them to the IBGP neighbors? Most BGP implementations have something along those lines and call that feature *BGP groups* or *BGP session templates*. That's what you'll practice in this lab exercise.

![Lab topology](topology-session-templates.png)

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.
