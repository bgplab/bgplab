# Use Disaggregated Prefixes to Select the Primary Link

Previous lab exercises in the *[‌Influencing Incoming (Ingress) Traffic Flow](index.md#ingress)* part of the *[BGP Routing Policies](index.md)* section described various mechanisms you can use to try to influence the inbound traffic flow. None of these tools work when dealing with "suboptimal" ISPs; in those rare moments you'll have to use a bigger hammer.

One the scenarios that is unfortunately oft used in the global Internet is prefix disaggregation: a customer owning address space larger than the minimum prefix size accepted in the public Internet can advertise the summary prefix over the backup link and two more specific prefixes over the primary link. That's what you'll practice in this lab exercise.

![Lab topology](topology-disaggregate.png)

!!! Warning
    Prefix disaggregation should be the tool-of-last-resort as it pollutes the routing tables throughout the Internet. Do not use it unless all the other tools failed.

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.