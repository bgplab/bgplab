# Master BGP Configuration with ipSpace.net Hands-On Labs

The following series of hands-on BGP labs will help you master numerous aspects of EBGP and IBGP on a platform of your choice[^PC]. The labs will cover:

**Basic BGP Setup**

* [Establish a BGP session](basic-session/) (basic-session)
* Protect a BGP session with MD5 password, TCP-AO password, and TTL check
* (Advanced) Run EBGP over unnumbered IPv4 interfaces or over IPv6 link-local addresses

**Simple End-User Setup**

* Connect to two upstream providers and advertise your IP prefixes
* Use BGP weights to prefer one of the upstream providers
* Prevent route leaking between upstream providers with AS-path filters
* Minimize the size of your BGP table with inbound filters
* Redistribute IGP information into BGP and use BGP summarization to minimize the number of BGP advertisements
* Perform simple load balancing across parallel links and across upstream provider

**Multiprotocol BGP**

* Run BGP with IPv6
* (Advanced) Run IPv4 and IPv6 over the same BGP session

**Simple Transit Network Setup**

* Use IBGP to transport BGP information across your network
* Use BGP route reflectors to reduce the number of IBGP sessions
* (Advanced) Use a hierarchy of route reflectors

**Networks with Multiple BGP Speakers**

* Use multiple WAN edge routers to connect to upstream ISPs
* Use BGP local preference to prefer one of the upstream providers
* Use more complex BGP local preference setup to prefer direct connectivity with customers of upstream ISPs
* Use MED to influence route selection in an upstream ISP
* Use AS-path prepending to influence route selection across multiple upstream ISPs

**Complex BGP Route Policies**

* Use BGP communities to influence route selection in upstream ISPs
* Build a transit autonomous system using BGP communities to change routing policies

[^PC]: Some assembly required: while the Cumulus Linux VMs/containers that are used for external BGP speakers are easy to download, you'll have to build a Vagrant box or install a Docker container image for your platform. 