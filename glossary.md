# Glossary

**AF_PACKET** — the Linux mechanism Suricata
normally uses for live capture: the kernel
hands the engine copies of packets straight
from an interface.

**Alert** — a dated record that traffic
matched a rule: who, to whom, which rule, and
the transaction it judged. In `fast.log` as
one line, in `eve.json` as a full object.

**App layer** — the top of the protocol
layering, where traffic becomes meaning: HTTP
requests, DNS questions, TLS handshakes.
Suricata parses these properly rather than
searching bytes.

**Capture (pcap)** — traffic recorded to a
file in the standard pcap format, the input
for offline analysis and Wireshark alike.

**Classtype** — a rule's category, defined in
`classification.config` with a default
priority; how alerts get filed and sorted.

**Control capture** — in this guide's lab, a
recording *without* the watched act, used to
prove a rule's silence is earned.

**Drop** — the rule action that discards a
packet. Only has power when Suricata sits
inline (IPS); in IDS mode the same verdict is
recorded with action "allowed".

**ET Open / ET Pro** — Emerging Threats, the
principal public ruleset (free) and its
larger subscription sibling, both published
by Proofpoint.

**EVE / eve.json** — Suricata's structured
output: one JSON object per event (alert,
http, dns, flow, stats, and more).

**Fast log** — `fast.log`, the classic
one-line-per-alert output.

**Flow** — one conversation between two
endpoints, tracked as a unit: its packets and
bytes in both directions, from first packet
to last.

**HOME_NET** — the configuration variable
naming *your* networks; rules are written
against it so one ruleset fits every house.

**IDS / IPS** — intrusion **detection**
system (watches a copy, can only report) and
intrusion **prevention** system (sits inline,
can drop traffic). One engine, two postures.

**Inline** — placed in the traffic's path, so
packets pass through the engine before
continuing. The seat that turns detection
into prevention.

**Mirror / SPAN port** — a switch feature
that copies all traffic crossing the switch
to one port, where a sensor can watch it.

**NFQUEUE** — a Linux firewall mechanism that
hands packets to a program (Suricata) for a
verdict, used for inline IPS on a host or
router.

**Offline mode** — running Suricata against a
recorded capture (`suricata -r`) instead of a
live interface.

**pcap_cnt** — an EVE field naming a packet's
position within the capture file it was read
from.

**Rule** — one line of detection knowledge:
header (action, protocol, addresses, ports,
direction) plus options (what to match, the
message, the sid).

**Runmode** — Suricata's threading
arrangement: `single`, `autofp`, or `workers`,
per capture mechanism.

**sid** — signature id, a rule's permanent
number. Public sets own their ranges; local
rules take 9000000 and up.

**Sticky buffer** — a rule keyword (`http_uri`,
`dns_query`, `tls_sni`, …) that aims the
match following it at one named part of the
rebuilt event.

**suricata-update** — the companion tool that
fetches rule sources, merges them into
`/var/lib/suricata/rules/suricata.rules`,
applies your enable/disable choices, and
tests the result.

**Thresholding** — rules and settings that
limit how often a match alerts (once an hour
per source, say), so a true verdict does not
become a flood.

**Trigger capture** — in this guide's lab, a
recording *containing* the watched act, used
to prove a rule fires.
