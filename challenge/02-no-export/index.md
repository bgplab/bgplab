# Using No-Export Community to Filter Transit Routes

[RFC 1997](https://www.rfc-editor.org/rfc/rfc1997.html) defined several well-known BGP communities recognized by almost all BGP implementations. One of them is the NO_EXPORT community, defined as:

> All routes received carrying a communities attribute containing this value MUST NOT be advertised outside a BGP confederation boundary (a stand-alone autonomous system that is not part of a confederation should be considered a confederation itself).

Forgetting the weird wording, the NO_EXPORT community attached to a BGP prefix means "_do not advertise this one over EBGP sessions_" -- seemingly an ideal solution to our *[do not leak transit routes](../policy/2-stop-transit.md)* challenge. You'll practice that scenario in this lab exercise.

![Lab topology](topology-no-export.png)

!!! Expert
    This is a challenging lab. We expect you have completed most of the foundational labs and know what you're doing. All you'll get from us are a few basic guidelines.

!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.