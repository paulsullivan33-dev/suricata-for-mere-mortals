# What Suricata Is

Suricata is a **network traffic inspector**.
Point it at a stream of packets — live from a
network card, or recorded in a file — and it
rebuilds what those packets *mean*: this was a
web request for that page, that was a DNS lookup
for this name, here is a file being downloaded.
Against each rebuilt event it checks a book of
**rules**. A rule describes one behaviour worth
noticing: a connection to an address on a
known botnet list, a web request whose shape
matches a known attack, a download of a file
type nobody expected. When traffic and rule
meet, Suricata writes an **alert** — a dated,
detailed record of what happened, between
whom, and which rule objected.

Three ideas carry the whole tool:

- **Packets become events.** Suricata does not
  just grep raw bytes. It tracks connections
  (**flows**), undoes the layering (Ethernet,
  IP, TCP, then the application protocol —
  HTTP, DNS, TLS, and dozens more), and only
  then applies rules. A request split across
  five packets is judged whole.
- **Rules are data, not code.** The knowledge
  of what is bad lives in text files anyone
  can read, written by security teams who
  publish them for everyone. Chapter 5 reads
  a real one.
- **Watching and blocking are two postures of
  one engine.** Beside the road, Suricata is
  an **IDS**: it sees a copy of the traffic
  and can only report. In the road, it is an
  **IPS**: traffic passes *through* it, and a
  rule can order a packet dropped. Nothing
  about the rules changes; the seat changes.

## What it is not

- **Not a firewall.** A firewall enforces a
  standing policy you wrote (these ports, those
  addresses). Suricata recognises behaviour,
  including behaviour on ports you deliberately
  left open — a perfectly legal web request can
  still be an attack on the web server.
- **Not an antivirus.** It watches the road,
  not the inside of your machines. It can spot
  a suspicious download crossing the wire; what
  the file does after landing is another tool's
  problem.
- **Not a log reader.** That is Fail2Ban's
  ground (see [the neighbours](the-neighbours.md)):
  Fail2Ban reads what services already logged;
  Suricata reads the wire itself, including
  traffic no service ever logged.
- **Not a recorder of everything.** Its cousin
  Zeek writes a rich diary of all activity,
  suspicious or not. Suricata's centre of
  gravity is the alert — though its `eve.json`
  output, chapter 6, quietly records a good
  deal of the diary too.

## The honest limit, stated early

Most modern traffic is **encrypted**. Suricata
can see a TLS session's outside — the addresses,
the timing, the server name in most handshakes,
the certificate — but not the web page inside
it. Rules that match on page content simply
never get their chance against HTTPS. This is
not a defect to configure away; it is the shape
of the modern internet, and chapter 10 returns
to what it means for a home watcher. What
remains visible is still a lot: DNS lookups
(often unencrypted), the list of servers your
machines talk to, downloads over plain HTTP,
scans, and the traffic of the many small
devices that never learned encryption.

## How this guide proceeds

Detection first, prevention last, and proof
before either: chapter 4 replays recorded
packets, chapter 7 writes one rule and makes
the engine convict and acquit on demand. Live
capture (chapter 8) and blocking (chapter 9)
are taught after the verdicts can be trusted —
and are marked **(documented)**, because the
machine this guide was built on is not allowed
to open a live capture socket, so those steps
could not be run here. The ledger in
`criteria.md` says exactly which is which.
