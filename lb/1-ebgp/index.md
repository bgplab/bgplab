# Load Balancing across External BGP Paths

Modern BGP implementations usually forward traffic across equal-cost external BGP paths (Equal-Cost Multipath or ECMP). Unfortunately, the default definition of the *equal-cost* paths usually includes *most BGP path attributes being equal*, and many implementations provide nerd knobs you can use to fine-tune which BGP path attributes you want to ignore when considering ECMP paths.

In this lab exercise, you'll observe simple EBGP ECMP across parallel paths toward AS 651000 (X1 and X2) and try to configure your router to forward traffic across all paths toward AS 65001 (X1, X2, and X3).

![Lab topology](topology-lb-ebgp.png)

!!! Warning
    ECMP traffic forwarding across multiple autonomous systems is usually not a good idea, as you need to know the internal structure and the end-to-end delay across individual autonomous systems. Still, you might have to configure multi-AS ECMP in environments that replaced IGP with EBGP.
    
!!! Tip
    This lab is still under development. Follow [blog.ipspace.net](https://blog.ipspace.net/) or [Ivan Pepelnjak on LinkedIn](https://www.linkedin.com/in/ivanpepelnjak/) to find out when it will be ready.