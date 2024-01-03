# About the Project

In the early 1990s, I managed to persuade the powers that be within Cisco's European training organization that they needed a deep-dive BGP course, resulting in a three-day (later extended to five days) Advanced BGP Configuration and Troubleshooting (ABCT) course[^CD]. I was delivering that course for close to a decade, allowing me to gradually build a decent story explaining the reasoning and use cases behind most of (then available) BGP features, from simple EBGP sessions to BGP route reflectors and communities[^EC].

Now imagine having more than a dozen hands-on labs following the "_BGP from rookie to hero_" story available for any platform of your choice[^NL]. Welcome to the [Open-Source BGP Configuration Labs](https://bgplabs.net/) project.

The project uses _[netlab](https://netlab.tools)_[^HT] to set up the labs and FRRouting containers or a [few other devices](1-setup.md#select-the-additional-devices-in-your-lab) as external BGP routers. You can use [whatever networking devices](1-setup.md#select-the-network-devices-you-will-work-with) you wish to work on[^XP], and if they happen to be supported by _netlab_, you'll get lab topology and basic device configuration for each lab set up in seconds[^XR]. Most lab exercises include device configurations for the external BGP routers for people who love wasting time with GUI.

[^XP]: Including physical hardware if you have a few extra Cumulus switches and are willing to do some crazy stuff to set things up.

You'll find the lab topology files and initial device configurations in a [GitHub repository](https://github.com/ipspace/bgplab), but you might [explore the lab exercises first](https://bgplabs.net/).

I also created a long list of [labs that would be nice to have](https://bgplabs.net/3-upcoming/). I probably missed something important -- please [open an issue](https://github.com/bgplab/bgplab/issues) or a [discussion](https://github.com/bgplab/bgplab/discussions), or (even better) become a contributor and submit a PR.

[^EC]: The echoes of those ideas are still visible (if you know where to look) in the Configuring BGP on Cisco Routers course --  ABCT eventually morphed into CBCR and became part of the original CCIP curriculum in the early 2000s, but that's another story.

[^CD]: If you happen to have the original ABCT course description, please send it over. I tried to find it in Web Archive, but it's been way too long...

[^NL]: As long as it's supported by _netlab_.

[^HT]: When you happen to have a Hammer of Thor handy, everything looks like a nail waiting to be hit ;)

[^XR]: Unless you love using resource hogs like Nexus OS, IOS XR, or some Junos variants.
