# Learning Offline

Suricata has two doors for packets: a live
interface, and a **file**. The file door —
recorded traffic in the standard **pcap**
format — is where all learning should happen,
for three plain reasons. A file can be replayed
forever, so an experiment can be repeated
until it is understood. A file cannot be
harmed: no setting, however wrong, breaks a
recording. And a file separates the two skills
this tool demands — *reading verdicts* from
*managing capture* — so each can be learned
without the other shouting.

The replay command is the one this guide uses
throughout:

```
$ suricata -r traffic.pcap -c /etc/suricata/suricata.yaml -l out/
```

`-r` names the capture, `-c` the configuration,
`-l` the folder the logs are written to. A
small capture is over in a blink; the lab's
24-packet file took **0.38 seconds** end to
end, engine start included.

**Check:** a good replay announces what it
ate:

```
i: pcap: read 1 file, 24 packets, 2316 bytes
```

If your run reports 0 packets, the file is
empty or not a pcap — check it with
`capinfos traffic.pcap` (packet count, size,
duration) before suspecting Suricata.

## Where captures come from

- **Record your own.** On any Linux box,
  `tcpdump -i any -w mine.pcap 'port 8080'`
  writes the standard format while traffic
  flows; Wireshark saves the same format from
  its graphical view. Record on a machine and
  a network you own — a capture is other
  people's traffic in a bag (see the safety
  rule in the README).
- **Generate them.** Test traffic can be
  synthesised packet by packet; libraries
  like Python's scapy build complete,
  valid conversations on demand.
- **Download specimens.** Public sample
  captures exist for study — malware-traffic
  archives and the Wireshark sample library
  among them. Treat strangers' captures of
  real attacks as the hazardous material they
  are: read them offline, on a machine that
  does not hold anything precious.

## This guide's lab captures, honestly

The lab needs two small captures of a pretend
web server on one machine: one in which a
particular page is requested, one in which it
is not. The build machine's sandbox forbids
live capture outright — `tcpdump` is refused
with `Operation not permitted` even as root,
because the sandbox holds no capture
privilege — so the lab's captures were
**synthesised with scapy**: complete TCP
conversations (handshake, request, response
carrying the real fixture pages, orderly
goodbye), checksums correct. Nothing about
the offline analysis changes: Suricata reads
packets from the file either way, and every
verdict in chapters 6 and 7 can be re-run
from the shipped files. The generator is in
`examples/` next to the rule it serves.

What the two files hold:

| File | Packets | Conversations | The point |
|---|---|---|---|
| `trigger.pcap` | 24 | 3 page fetches, one of them `/pangolin-survey.html` | The lab rule must fire — once |
| `control.pcap` | 16 | 2 page fetches, neither of them the pangolin page | The lab rule must stay silent |

`tshark` confirms the cast list before
Suricata ever runs:

```
$ tshark -r trigger.pcap -Y http.request \
    -T fields -e http.request.method -e http.request.uri
GET	/
GET	/pangolin-survey.html
GET	/field-notes.html
```

Keeping a **control** beside every trigger is
the habit that makes offline work science
instead of theatre: an engine that alerts on
both files has told you nothing, and a rule
that fires on the trigger alone has told you
something true. Chapter 7 collects on exactly
this pair.
