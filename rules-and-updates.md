# Rules and Rule Sources

A **rule** is one line of text: a header that
says whose traffic, and a body in brackets
that says what to look for and what to call
it. Here is a real one, from the ruleset this
chapter fetches — a tracker rule for the
Feodo banking trojan:

```
alert ip $HOME_NET any -> [162.243.103.246] any
(msg:"ET CNC Feodo Tracker Reported CnC Server group 1";
reference:url,feodotracker.abuse.ch;
threshold: type limit, track by_src, seconds 3600, count 1;
flowbits:set,ET.Evil; classtype:trojan-activity;
sid:2404300; rev:8096; ...)
```

Read it as a sentence: *alert when any machine
at home talks to this one address, which a
public tracker lists as a botnet's
command-and-control server; once an hour per
source is enough; file it under
trojan-activity.* Three things worth noticing.
The knowledge here is not a byte pattern but
**intelligence** — a curated list of bad
addresses, refreshed daily. Every rule carries
a **sid** (signature id, its permanent number)
and a **rev** (revision, bumped when the rule
is edited — this one is on its 8,096th). And
the category comes from `classtype`, whose
definitions and default priorities live in
`classification.config`, a fact chapter 7
puts to work.

## Where rules come from

| Source | What it is | Cost |
|---|---|---|
| **ET Open** (Emerging Threats) | The big public ruleset: malware, botnets, scans, policy — maintained by Proofpoint, free | Free, the default |
| **ET Pro** | The same house's larger, faster-updated set | Subscription (needs a code) |
| **Snort Subscriber / Community** | Cisco Talos rules, written for Snort; Suricata runs most of them | Free / subscription tiers |
| **The engine's own event rules** | Decoder and protocol anomaly rules shipped in `/etc/suricata/rules/` | In the package |
| **Yours** | Local rules for your network's own concerns | Chapter 7 |

The sets have shapes: in the ET Open merge
this guide downloaded, **52,080** rules carry
ET messages, **915** are GPL-community rules,
and **320** are Suricata's own — one file,
several authors, which is why the merge needs
a manager.

## `suricata-update`, the manager

Rules change daily, and rulesets are not
single files but bundles that must be merged,
deduplicated, and adjusted for your choices
(rules you disable, rules you modify). That
job belongs to **`suricata-update`**, installed
alongside the engine. Out of the box it knows
one enabled source — ET Open — and running it
is one word:

```
$ sudo suricata-update
...
-- Loaded 69281 rules.
-- Disabled 14 rules.
-- Enabled 136 rules for flowbit dependencies.
-- Writing rules to /var/lib/suricata/rules/suricata.rules:
   total: 69281; enabled: 53316; added: 69281
-- Writing /var/lib/suricata/rules/classification.config
-- Testing with suricata -T.
```

Facts from this guide's real run: the merge
produced **69,281 rule lines** in a 44 MB
file, of which **53,316 are enabled** (the
rest ship commented out — deliberately
noisy or situational rules arrive disabled).
A first fetch took about a minute here,
network permitting; updates after the first
are incremental in spirit but still rewrite
the merged file. And note the last line:
**the updater tests the result with
`suricata -T` itself** — a broken merge never
quietly replaces a working file.

Day to day you will meet three companions:

- `suricata-update list-sources` — every
  ruleset the tool knows, free and paid.
- `/etc/suricata/disable.conf` — one sid (or
  pattern) per line: rules to leave enabled
  in the file but switched off. The polite way
  to silence a rule that cries wolf on *your*
  network — better than editing the merged
  file, which the next update would overwrite.
- `/etc/suricata/enable.conf` and
  `modify.conf` — the same idea in the other
  directions.

**Check:** after an update, the engine should
swallow the result whole. Its own log
(`suricata.log`, in the `-l` directory — the
lab's was `out-full/`) records the loading:

```
... Info: detect: 1 rule files processed. 53316 rules
    successfully loaded, 0 rules failed
... Info: detect: 53321 signatures processed. 1253 are
    IP-only rules, 4531 are inspecting packet payload,
    47304 inspect application layer, 108 are decoder event only
```

That census is worth a second look: most
modern rules judge **rebuilt application
events**, not raw packets — the app-layer
section of chapter 3 made flesh. It also
explains the price: loading all 53,316 rules
took this machine about **30 seconds** before
the first packet was read, where the lab's
single rule took 0.38 seconds for the whole
run. Rules are knowledge, and knowledge has
weight; the last section of chapter 12 deals
with a ruleset that will not load at all.
