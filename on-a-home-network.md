# On a Home Network

A watcher can only judge traffic that crosses
its wire, and home networks are mostly built
so that traffic *doesn't* cross wires: the
switch in your router keeps the laptop's
conversation with the printer between the two
of them. Where Suricata can sit is therefore
the first home question, before any software
one. Three seats work:

| Seat | What it sees | The price |
|---|---|---|
| **On the router itself** | Everything entering or leaving the house; with the right setup, traffic between local devices too | The router must run Linux you control (a mini-PC with OPNsense or plain Linux, a capable OpenWrt box) |
| **On a mirror/SPAN port** | A switch copies all traffic crossing it to the port Suricata listens on | Needs a managed switch with a mirror feature; receive-only by nature — IDS forever, never IPS |
| **Inline at the door** | All internet-bound traffic passes through it (chapter 9) | It is now part of the road: its failure is the house's failure |

The common beginner disappointment — Suricata
on a laptop plugged into any spare router
port, seeing almost nothing — is the switch
doing its job. Broadcasts and the laptop's
own traffic are all a plain port ever gets.

## What a home watcher actually catches

Not Hollywood intrusions, mostly. The honest
list, in rough order of how often it matters:

- **Devices phoning strange homes.** The
  camera, plug, or TV holding conversations
  with addresses on tracker and botnet lists
  (chapter 5's rules are built for exactly
  this). Often it is merely chatty telemetry;
  now and then it is worse, and either way it
  is news.
- **DNS, the household's diary.** Plain DNS
  lookups are visible in full — every name
  every device asked for. Suricata logs them
  as events even without alerts, which makes
  the `dns` stream of `eve.json` the single
  most informative file on a home sensor.
- **Scans and knocks at the door.** If any
  service faces the internet, attempts against
  it arrive labelled and categorised.
- **Plain-HTTP anything.** Downloads,
  updates, and legacy devices still speak it,
  and every word is judgeable.

## The encrypted limit, applied

Chapter 1's limit in household dress: the
laptops' and phones' web traffic is TLS, so
page-level rules never see it. What remains —
destinations, timing, DNS, certificates,
unencrypted stragglers — still answers the
question a home watcher is really for: **what
are the things in my house saying, and to
whom?** It cannot answer "was that page an
attack?" for a page it could not read, and a
guide that promised otherwise would be
selling something.

Two courtesies close the chapter. Other
people live on home networks: a sensor's logs
are a record of their activity too, and
deserve the same care as any capture
(README's safety rule). And a watcher should
be **boring to run**: disk for `eve.json`,
a weekly update on a timer (chapter 5), and a
glance at alerts you have learned to trust.
A sensor that needs daily nursing gets
unplugged by November.
