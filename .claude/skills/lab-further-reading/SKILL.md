---
name: lab-further-reading
description: Add a "Further Reading" section to a BGP lab exercise (docs/**/*.md) with per-platform vendor configuration links (text-fragment URLs, one per configuration step) and a few well-written blog posts, plus a tip pointing to it from "Configuration Tasks". Use when asked to add documentation pointers, vendor docs, configuration guidelines, or further reading to a lab.
---

# Add "Further Reading" to a lab exercise

Reference implementation: `docs/basic/1-session.md` (the "Further Reading" section and the second tip in "Configuration Tasks"). Read it first and match its structure and wording.

## 1. Identify the configuration steps

Read the lab's "Configuration Tasks" section and list the distinct configuration steps the student has to perform (for example: start a BGP process, configure a BGP neighbor). Each step gets its own link per platform.

Add an extra step for platforms whose defaults interfere with the lab. For basic EBGP sessions, that is the RFC 8212 default EBGP policy:

| Platform | Default EBGP filters? | What to link |
|----------|-----------------------|--------------|
| FRRouting | Yes | `bgp ebgp-requires-policy` |
| Cisco IOS XR | Yes | route policy requirement / `bgp unsafe-ebgp-policy` |
| Cisco IOS XE, Arista EOS, Junos | No | — |

## 2. Find vendor documentation

Cover these platforms, in this order: **Cisco IOS XE, Arista EOS, FRRouting, Cisco IOS XR, Junos**.

Sources that worked for the session lab (reuse them when the topic is covered there):

| Platform | Document |
|----------|----------|
| Cisco IOS XE | IP Routing Configuration Guide, IOS XE 17.x — `https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-routing/b-ip-routing.html` (table of contents; one chapter per feature) |
| Arista EOS | EOS User Manual, BGP chapter — `https://www.arista.com/en/um-eos/eos-border-gateway-protocol-bgp` |
| FRRouting | `https://docs.frrouting.org/en/latest/bgp.html` |
| Cisco IOS XR | BGP Configuration Guide for NCS 5500, IOS XR 26.x — `https://www.cisco.com/c/en/us/td/docs/iosxr/ncs5500/bgp/26xx/configuration/guide/b-bgp-cg-ncs5500-26xx.html` |
| Junos | Junos BGP user guide topic maps under `https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/` |

Rules:

* **IOS XR documents MUST cover recent releases (25.x or 26.x), not 7.x.** The platform does not matter (there is no XRd-specific BGP guide). Prefer guides whose title states the release; the Cisco 8000 guide is unversioned ("Cisco IOS XR Releases") and was rejected.
* Link only to pages you verified exist. Never guess URLs.

## 3. Build text-fragment links

Do **not** use auto-generated `#anchor` (`#xx1115306`, `#task_81F0...`); they might change. When you can't find a usable anchor, use text fragments (`#:~:text=...`) so long documents open at the relevant section.

* The browser jumps to the **first** text fragment match, and vendor pages usually start with a table of contents (Cisco "Chapter Contents", Arista and Junos side/top TOCs) that repeats the section headings. Choose the phrase in this order of preference:
    1. A **low-level heading** that is not listed in the table of contents (typically a task or subsection heading a level or two below the chapter headings, or a command name heading in FRRouting docs). Use the whole heading text.
    2. Otherwise, the **first sentence of the section's body text**.
    3. Never a heading that also appears in the table of contents.
* Check before using it: the phrase must be verbatim and occur exactly once on the page (a heading that occurs twice is almost always also in the TOC). With a saved page, `fragment.py` reports the count; with the fetch tool, ask explicitly whether the heading appears in the page's table of contents and how many times the exact phrase occurs.
* Encode with `scripts/fragment.py`, which percent-encodes spaces, commas, parentheses, and hyphens (`-` must be `%2D` in text fragments) and, given a saved copy of the page, checks how often the phrase occurs:

  ```
  python3 .claude/skills/lab-further-reading/scripts/fragment.py URL "phrase" [saved-page.html]
  ```

Fetching pages:

* FRRouting and Juniper pages can be downloaded with `curl` (save them to the scratchpad and pass them to `fragment.py`).
* cisco.com (403) and arista.com (406) block `curl`. Use WebFetch (or the web-fetch agent): ask for the **verbatim** subheadings under a named section (and whether each one is in the table of contents), or the first sentence under the section if there are no suitable subheadings, and whether a phrase occurs in the excerpt. Pages longer than 100,000 characters must be read with `offset` chunks; the fetch tool may not reach the end of very long Cisco chapters (if a section is unreachable, link to an equivalent step in a reachable section, e.g. the neighbor step inside IOS XR "Enable BGP Routing").

## 4. Find blog posts

Add up to three blog posts that explain the lab's concepts and configuration steps.

* MUST NOT require registration (no LinkedIn, Medium, or similar; avoid networklessons.com — much of it is members-only).
* SHOULD be ad-free (vendor self-promotion is acceptable; ad networks are not).
* Prefer `blog.ipspace.net` (search it with `allowed_domains`); it rarely covers basics, but often covers specific details (address-family activation, RFC 8212, session protection...).
* Use the web-fetch agent to check each candidate: loads without a wall, ads or not, what it covers, correctness, and quality. Reject posts whose examples contradict their own outputs, content-farm posts, and packet-level deep dives when the lab is about configuration.
* Posts used for the session lab: Kentik "BGP Routing Tutorial Series: Part 3", ipSpace "Use the explicit address-family ipv4 in BGP configurations", ipSpace "Default EBGP Policy (RFC 8212)".

## 5. Edit the lab

1. In "Configuration Tasks", add a tip (after any existing tips):

   ```
   !!! Tip
       Not sure how to configure BGP on your device? You'll find pointers to the relevant vendor documentation in the [Further Reading](#further) section.
   ```

2. Add `## Further Reading {#further}` right before `## Reference Information` (or at the end of the lab if there is no such section) containing:
   * An intro sentence naming the configuration steps (and which platforms need the extra step).
   * A `| Platform | Configuration guidelines |` table, one row per platform. Format each cell's links as an HTML bullet list — `<ul><li>[Step name](url)</li>...</ul>` — because Markdown tables cannot contain Markdown lists. Mark the IOS XR row with its release, e.g. `Cisco IOS XR (release 26.x)`.
   * "You might also find these blog posts useful:" followed by a bulleted list; each item is the post title as a link plus one sentence on what it explains.

3. Run `mkdocs build -q -d <scratchpad>/site` and check the rendered table in `<site>/<section>/<lab>/index.html`.

## 6. Report

Tell the user which links were verified and how (raw page vs. fetch tool), any assumptions (e.g. platform defaults you could not confirm), and which blog candidates were rejected and why. Do not commit unless asked.
