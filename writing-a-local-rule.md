# Writing a Local Rule

Time to make the engine convict and acquit on
demand. The lab's rule watches for one act —
requesting a particular page from a pretend
web server — and the whole exercise is the
pair of captures from chapter 4: on
`trigger.pcap` it must fire exactly once; on
`control.pcap`, never. The rule, complete
(it ships in `examples/local.rules`):

```
alert http any any -> any any (msg:"MM LAB -- pangolin page requested"; flow:established,to_server; content:"pangolin"; http_uri; classtype:policy-violation; sid:9000001; rev:1;)
```

## The rule, piece by piece

| Piece | Meaning |
|---|---|
| `alert` | The action: record an alert. Its sibling `drop` only has power in IPS mode (chapter 9) |
| `http` | The protocol: judge rebuilt HTTP events, not raw packets |
| `any any -> any any` | Addresses and ports, source → destination. `any` because the lab's loopback falls outside `HOME_NET` (chapter 3); a real rule writes `$HOME_NET` and friends |
| `msg:"..."` | The words that will appear in every log. Write the headline you want to read at 3 a.m. |
| `flow:established,to_server` | Only settled connections, judged on the client's half — the request, not the response |
| `content:"pangolin"; http_uri;` | The heart: the word *pangolin* must appear in the **request address**. `http_uri` is a *sticky buffer* — it aims the `content` before it at one named part of the event |
| `classtype:policy-violation;` | Files the alert under a category from `classification.config`, which sets the priority readers see |
| `sid:9000001; rev:1;` | The rule's number and revision. Local rules take sids from 9000000 upward — the range the public sets leave for you |

The sticky buffer deserves one more sentence,
because it is the difference between a blunt
tool and this one. Without `http_uri`, the
rule would fire on the word *pangolin*
anywhere in the request — a form field, a
cookie, a posted essay about pangolins. With
it, only the address counts: the rule judges
*where the client asked to go*, which is the
act the lab actually cares about. Most of
rule-writing craft is choosing the right
buffer — `http_user_agent`, `http_host`,
`dns_query`, `tls_sni`, `file_data` — and the
engine's event model (chapter 3) is what
makes them exist.

## Proving it fires

`-S` loads one rule file **exclusively**,
shutting the 53,316 public rules out of the
courtroom so the only voice is ours:

```
$ suricata -r trigger.pcap -c /etc/suricata/suricata.yaml \
    -S local.rules -l out-trigger
i: pcap: read 1 file, 24 packets, 2316 bytes

$ cat out-trigger/fast.log
11/14/2023-22:13:25.000000  [**] [1:9000001:1] MM LAB -- pangolin
page requested [**] [Classification: Potential Corporate Privacy
Violation] [Priority: 1] {TCP} 127.0.0.1:41002 -> 127.0.0.1:18085
```

One alert. The flow is the middle fetch —
source port 41002, the pangolin request, as
the EVE record in chapter 6 confirms. The
fetches of `/` and `/field-notes.html` passed
unobjected, on the same run, in the same file.

## Proving it doesn't

```
$ suricata -r control.pcap -c /etc/suricata/suricata.yaml \
    -S local.rules -l out-control

$ wc -c out-control/fast.log
0

$ jq -s '[.[] | select(.event_type=="alert")] | length' \
    out-control/eve.json
0
```

And the acquittal is informed, not blind:
`out-control/eve.json` still holds 2 `http`
events and 2 `flow` events. The engine saw
the innocent traffic in full and let it go.
**That** is a tested rule.

**Check:** your rule earns its place when all
three hold — it loads (`suricata -T` with the
file, or a clean `-S` run), it fires on the
trigger and on nothing else in it, and it is
silent on the control. Miss the first and the
engine prints the rule's line number with its
complaint; miss the second and your pattern
is too narrow; miss the third and it is too
wide, and on a live network it would cry wolf
at scale.

## One honest footnote: the classtype

The lab's first version of this rule omitted
`classtype`, and it fired wearing
`[Classification: (null)] [Priority: 3]`. A
rule without a category still *works* — it
alerts — but it files itself under nothing,
at the lowest priority, in every reader's
view. Categories are not decoration; they are
how the next human sorts your verdict from
the noise. Both versions were run for real;
the difference above is the whole lesson.
