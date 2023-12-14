# Remove Private BGP AS Numbers from the AS Path

Some end customers use private BGP AS numbers when running BGP with their Internet Service Providers (ISPs). Those AS numbers should not appear in the BGP AS path when the ISP advertises those prefixes to its peers and upstream providers.

![Lab topology](topology-removeprivate.png)

In this lab exercise, you'll use the *remove private AS* feature available in many BGP implementations to remove the customer's private BGP AS number from the BGP AS path sent in EBGP updates.

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.