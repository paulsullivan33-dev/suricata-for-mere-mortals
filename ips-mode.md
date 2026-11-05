# IPS Mode

**(Documented — not run on the build machine,**
for the same reason as chapter 8: inline mode
needs live capture and forwarding, which the
sandbox refuses outright. Taught from the
configuration and the manual.)

Chapter 1's distinction becomes concrete
here. An IDS watches a **copy**. An IPS sits
**in the path**: packets enter Suricata
before they are allowed to continue, and a
rule's verdict of `drop` is executed on the
spot. Nothing else about the tool changes —
same rules, same logs, same engine — but the
consequences of every mistake invert. A wrong
IDS rule makes noise. A wrong IPS rule makes
an outage, authored by you, at line rate.

## The three ways in

| Mechanism | How traffic is diverted | Typical seat |
|---|---|---|
| **NFQUEUE** | The firewall (nftables/iptables) hands packets to Suricata's queue and obeys its verdict | A Linux router or server protecting itself |
| **AF_PACKET bridge** | Suricata copies between two interfaces, forwarding what it allows | A transparent box cabled into a link |
| **Host inline on one interface** | AF_PACKET's IPS mode on a single interface with copy semantics decided by setup | Small appliances, lab rigs |

NFQUEUE is the one a Linux reader is likeliest
to meet: the engine's own list shows `NFQ`
runmodes (`autofp`, `workers`), the build
carries NFQ support (chapter 2's feature
string), and the diversion is a firewall rule
you write — which means *you* decide exactly
which traffic pays the toll, and everything
else flows past unjudged. Choose the toll
narrowly on purpose.

## What changes in the rules

- The action word `drop` gains force. The
  same line that logged in chapter 7, written
  `drop http ...`, now stops the request.
  Rulesets are written `alert`-first for this
  reason: a public rule will not block your
  network until you promote it.
- EVE says so: a blocked flow's alert carries
  `"action": "blocked"` where chapter 6's
  said `"allowed"`. That one field is how
  your future self audits what the box did.
- New failure modes arrive: if Suricata
  dies, an inline path can die with it unless
  the diversion is built to fail open (traffic
  flows, unwatched) or fail closed (nothing
  flows). That choice is a policy decision
  about your network, not a default to accept
  blindly.

## The working discipline

Everyone who runs inline learns the same
order of operations, and it is not optional:

1. **Run the seat as an IDS first.** Same
   position, same rules, alert-only, for long
   enough to meet your network's ordinary
   weirdness — days, not minutes.
2. **Promote rules one at a time**, starting
   with the verdicts you would defend in
   writing (known botnet addresses, chapter
   6's tracker rules), never by the thousand.
3. **Keep an undo in reach**: how to stop the
   diversion or the service, rehearsed before
   it is needed at midnight.

**Check:** you are ready for IPS when the IDS
in the same seat produces a week of alerts
you have read and agree with. If that week
has not happened yet, the honest answer to
"should this block?" is still no.
