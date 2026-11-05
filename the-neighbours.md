# The Neighbours

Four tools live on Suricata's street. Each
shares one of its jobs and none shares all,
and placing them keeps every chapter of this
guide in proportion.

| Tool | Watches | Answers | The difference that matters |
|---|---|---|---|
| **Snort** | The wire | "Did known-bad behaviour cross?" | The elder IDS/IPS (Cisco Talos); rule language close enough that its sets mostly run here |
| **Zeek** | The wire | "What happened, in full?" | A diarist, not a sentry: rich logs of every connection, lookup, and file — verdicts optional |
| **Fail2Ban** | Service logs | "Who keeps failing, and shall we ban them?" | Never sees a packet; convicts on what services already wrote down, then asks the firewall to act |
| **Wireshark / tcpdump** | The wire | "Show me the packets themselves" | Your eyes, not a watchman: records and dissects; raises no alerts and keeps no vigil |

**Snort** is the ancestor: founded 1998,
Suricata (2010) was built by the OISF as a
multi-threaded answer to the same problem,
and the rivalry is friendly enough that rule
sets cross the street in both directions —
chapter 5's source list includes Talos's own.
Choose Snort for its ecosystem and track
record; choose Suricata for threads and its
application-layer depth. Households rarely
need both pointed at the same wire.

**Zeek** (formerly Bro) is the one to add
when alerts stop being enough. Where
Suricata's diary (`eve.json`) is a by-product,
Zeek's logs are the product: every connection,
DNS query, TLS handshake, and file, indexed
for asking questions later — including
questions nobody had when the traffic flowed.
Incident work is usually Zeek's diary read
beside Suricata's verdicts.

**Fail2Ban** — this series has a guide of its
own — works a floor below: no packets at all,
just the logs of SSH, mail, and web services,
counting failures and banning offenders at
the firewall. It catches the password-guesser
that Suricata, watching encrypted SSH from
outside, can only see knocking. The two are
complements, not rivals: Suricata for what
crosses the wire, Fail2Ban for what the
doorman already wrote in his book.

**Wireshark and tcpdump** are how captures
are born and read (chapter 4); every other
tool on this page eats what tcpdump writes.
When a Suricata verdict needs a second
opinion, the pcap in Wireshark *is* the second
opinion — the same packets, dissected for a
human instead of an engine.
