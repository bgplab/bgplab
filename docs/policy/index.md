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
* [Use No-Export Community to Filter Transit Routes](d-no-export.md)
* [Use Outbound Route Filters (ORF) for IP Prefixes](f-orf.md)

## Adjusting Outgoing (Egress) Traffic Flow {#egress}

It's relatively easy to change how traffic leaves your network (autonomous system) -- you have to modify the BGP- and routing tables on your routers. These labs -- ranging from simple one-router scenarios to complex network-wide policies -- will help you master the BGP tools you can use to get the job done:

* [Use BGP weights](1-weights.md) to prefer one of the upstream providers
* [Implement a consistent AS-wide routing policy](5-local-preference.md) with BGP local preference.

Once you master the basics, you'll be ready for more complex scenarios:

## Influencing Incoming (Ingress) Traffic Flow {#ingress}

Trying to persuade neighboring autonomous systems to change how they send you the traffic is much more complicated than changing the routing in your network. While there's no definitive one-size-fits-all solution, you will find these tools indispensable:

* [Use MED to Influence Incoming Traffic Flow](6-med.md)
* [Use AS-Path Prepending to Influence Incoming Traffic Flow](7-prepend.md)
* [Attach BGP Communities to Outgoing BGP Updates](8-community-attach.md)
* [Resolve BGP Wedgies](e-wedgies.md)
* [Use Disaggregated Prefixes to Select the Primary Link](b-disaggregate.md)

## More Complex Routing Policies {#complex}

You use these labs to practice how to use a combination of BGP attributes and routing policy tools to build more complex routing policies:

* [Use BGP Communities in Routing Policies](9-community-use.md).
This exercise combines BGP community lists, route maps, and the BGP local preference.
* [Use the backup link to reach the adjacent autonomous system](a-locpref-route-map.md).
This exercise combines AS-path filters, prefix lists, route maps, and the BGP local preference.
* [BGP Policy Templates](../session/7-policy.md)
In this exercise, you'll learn how to create scalable BGP policy deployments using a combination of AS-path filters, prefix lists, and BGP communities.
