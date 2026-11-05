# Suricata for Mere Mortals

Your network talks all day: laptops asking for
web pages, phones checking mail, a printer
announcing itself, and — now and then — something
talking to an address it has no business talking
to. **Suricata** is the watcher on the wire. It
reads network traffic as it passes, compares what
it sees against a large book of **rules** — one
rule per known bad behaviour — and writes down
what matched, in detail, in a log you can search.
Run it the other way, inline, and it can also
*stop* the traffic it condemns. Watching is
called **IDS** mode (intrusion detection);
stopping is **IPS** mode (intrusion prevention).
Same engine, two postures.

This guide teaches the watching first, the way
you can prove every step: offline, against
recorded packets, with a rule you write yourself.
It installs Suricata for real, reads its one big
configuration file section by section, fetches
the standard open ruleset and counts what
arrived, then runs a small lab capture through
the engine twice — once where a hand-written
rule must fire, once where it must not.

A note on how this guide was verified, because
it matters here. Suricata 7.0.3 was installed
for real on the build machine. The lab rule
really fired — exactly once, on exactly the
request it was written for — and a control
capture proved the silence was earned, not
empty. The full open ruleset, all 53,316 enabled
rules, really was loaded against the same small
capture. One thing the build machine would not
do: its sandbox refuses to open a live capture
socket at all, even for root, so **live capture
and IPS blocking are marked (documented)** —
taught from the configuration and the manual,
never presented as run. `criteria.md` keeps the
exact ledger, including how the lab captures
were made and why.

## What this guide covers

- [**What Suricata is**](what-suricata-is.md) —
  the watcher on the wire, detection versus
  prevention, and what it cannot see
- [**Installing Suricata**](installing-suricata.md) —
  the package, the files it lays down, and the
  surprise in a fresh install: no rules at all
- [**The configuration file**](the-configuration-file.md) —
  `suricata.yaml` read section by section: address
  groups, outputs, protocol parsers, capture
- [**Learning offline**](learning-offline.md) —
  packet captures, replaying them with
  `suricata -r`, and why offline comes first
- [**Rules and rule sources**](rules-and-updates.md) —
  what a rule is, where the big rulesets come
  from, and `suricata-update`, the tool that
  fetches and merges them
- [**Reading the output**](reading-the-output.md) —
  `eve.json`, `fast.log` and `stats.log`, and
  what a real alert looks like up close
- [**Writing a local rule**](writing-a-local-rule.md) —
  one small rule taken apart piece by piece,
  then proven twice: firing, and not firing
- [**Going live**](going-live.md) — capture on a
  real interface, runmodes and threads, and
  the checks to make before trusting it
  **(documented)**
- [**IPS mode**](ips-mode.md) — standing in the
  road instead of beside it: inline setups,
  drop actions, and what changes when a wrong
  verdict stops real traffic **(documented)**
- [**On a home network**](on-a-home-network.md) —
  where a watcher can sit in a house, and the
  encrypted-traffic limit stated plainly
- [**The neighbours**](the-neighbours.md) —
  Snort, Zeek, Fail2Ban and Wireshark: who does
  which part of this job
- [**Troubleshooting**](troubleshooting.md) —
  symptom → cause → fix, drawn from the lab
- [**Glossary**](glossary.md) — the words, in
  plain language
- [**Writing criteria**](criteria.md) — the
  standard every guide in this series is held
  to, and this guide's verification ledger

## The one safety rule

Suricata reads traffic, and traffic is other
people's private business as well as your own.
**Only monitor networks you own or are
explicitly authorised to watch**, and treat
captured packets as sensitive data: a capture
can hold passwords sent unencrypted, private
messages, and the shape of someone's whole day.
Everything in this guide's lab is traffic the
lab generated itself, on one machine, between
two pretend programs.
