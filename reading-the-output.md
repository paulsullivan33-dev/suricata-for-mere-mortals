# Reading the Output

Suricata writes three logs you will actually
read, and this chapter reads real ones — all
from the lab runs of chapter 7, against the
24-packet `trigger.pcap` (three page fetches,
one of them watched) and its 16-packet
`control.pcap` sibling.

## `fast.log` — the headline

One line per alert, nothing else:

```
11/14/2023-22:13:25.000000  [**] [1:9000001:1] MM LAB -- pangolin page requested [**] [Classification: Potential Corporate Privacy Violation] [Priority: 1] {TCP} 127.0.0.1:41002 -> 127.0.0.1:18085
```

Left to right: when (the capture's clock, not
yours), the rule's identity as
`[gid:sid:rev]` — generator 1, signature
**9000001**, revision 1 — the message, the
classification and priority the rule's
`classtype` brought with it, and the flow it
fired on. `fast.log` answers exactly one
question — *did anything object, and to
what?* — which makes it the right first look
and the wrong last one. The control run's
`fast.log` is empty, and empty is a complete
sentence: no rule objected to anything.

## `eve.json` — the evidence

EVE (Extensible Event Format) writes **one
JSON object per event**, alerts included but
not alone. Counted by type, the two lab runs:

| Event type | trigger.pcap | control.pcap | What it records |
|---|---|---|---|
| `alert` | 1 | 0 | A rule fired — the verdict |
| `http` | 3 | 2 | One rebuilt request/response, with method, address, status, agent |
| `flow` | 3 | 2 | One connection's summary: packets and bytes each way, start and end |
| `fileinfo` | 3 | 2 | A file seen crossing (here, the HTML pages themselves) |
| `stats` | 1 | 1 | The engine's counters at shutdown |

Read that table twice; it teaches the tool's
character. The control capture is **not**
blank — the engine watched both innocent
fetches, rebuilt them, and filed them; it
simply had nothing to object to. Absence of
alerts with presence of `http` events is a
healthy watcher. Absence of *everything* is
a watcher pointed at the wrong wire.

The alert event itself carries the whole
story in one object ( trimmed here):

```json
{"event_type": "alert",
 "src_ip": "127.0.0.1", "src_port": 41002,
 "dest_ip": "127.0.0.1", "dest_port": 18085,
 "alert": {"signature_id": 9000001, "rev": 1,
   "signature": "MM LAB -- pangolin page requested",
   "category": "Potential Corporate Privacy Violation",
   "severity": 1, "action": "allowed"},
 "http": {"url": "/pangolin-survey.html",
   "http_method": "GET", "status": 200,
   "http_user_agent": "LabBrowser/1.0"},
 "flow": {"pkts_toserver": 4, "pkts_toclient": 2,
   "bytes_toserver": 318, "bytes_toclient": 360}}
```

Three fields deserve habits. `alert.action`
says **allowed** — this engine watched and
reported; in IPS mode a dropped flow says so
here (chapter 9). The `http` block is the
*transaction* the rule judged, status 200 and
all: proof the verdict was about a completed,
real request. And because EVE is JSON, it is
meant to be queried, not eyeballed:

**Check:** these two commands, verbatim from
the lab, separate verdict from silence:

```
$ jq -c 'select(.event_type=="alert")' out-trigger/eve.json
{...the alert above, on one line...}

$ jq -s '[.[] | select(.event_type=="alert")] | length' out-control/eve.json
0
```

## `stats.log` — the engine's own account

Counters, written at shutdown (and
periodically in live runs). The lines the lab
quotes most:

```
decoder.pkts          | Total | 24
decoder.bytes         | Total | 2316
tcp.sessions          | Total | 3
app_layer.flow.http   | Total | 3
detect.alert          | Total | 1
```

This is the reconciliation page: packets read
(24, matching the replay's own report), TCP
sessions tracked (3 — the three fetches),
flows the HTTP parser claimed (3), alerts
raised (1). When a run surprises you, these
four numbers usually confess where: packets
high but sessions zero means the traffic was
not TCP; `app_layer.flow.http` at zero on
known web traffic means the parser never saw
it — wrong port, wrong direction, or a
capture that starts mid-conversation.

In live running, EVE and stats are also what
you *ship*: the ecosystem's normal shape is
Suricata writing `eve.json` on each sensor
and a collector (the Elastic stack, Splunk,
or a humble `jq` habit) reading it elsewhere.
Nothing in this guide needs that machinery —
but everything you have just read is exactly
what the machinery eats.
