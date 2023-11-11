# BGP Routing Policies

These lab exercises will help you master the essential tools you can use in BGP routing policies. You will also be able to practice creating more complex routing policies.

The labs are grouped into three sections:

* Filtering BGP updates
* Adjusting outgoing traffic flow
* Influencing incoming traffic flow

## Filtering BGP Updates {#filter}

The first thing you should do when you use BGP to connect to the public Internet is limit the information you advertise to your neighbors to the prefixes you own. These labs will help you get there:

* [Prevent route leaking between upstream providers](2-stop-transit.md) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](3-prefix.md) with a prefix list
* [Minimize the size of your BGP table](4-reduce.md) with inbound filters

## Adjusting Outgoing (Egress) Traffic Flow {#egress}

It's relatively easy to change how traffic leaves your network (autonomous system) -- you have to modify the BGP- and routing tables on your routers. These labs -- ranging from simple one-router scenarios to complex network-wide policies -- will help you master the BGP tools you can use to get the job done:

* [Use BGP weights](1-weights.md) to prefer one of the upstream providers
* [Implement a consistent AS-wide routing policy](5-local-preference.md) with BGP local preference.

Once you master the basics, you'll be ready for more complex scenarios:

* [Use the backup link to reach the adjacent autonomous system](a-locpref-route-map.md). This exercise combines AS-path filters, prefix lists, route maps, and BGP local preference.

## Influencing Incoming (Ingress) Traffic Flow {#ingress}

Trying to persuade neighboring autonomous systems to change how they send you the traffic is much more complicated than changing the routing in your network. While there's no definitive one-size-fits-all solution, you will find these tools indispensable:

* [Use MED to Influence Incoming Traffic Flow](6-med.md)
* [Use AS-Path Prepending to Influence Incoming Traffic Flow](7-prepend.md)
* [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md)
