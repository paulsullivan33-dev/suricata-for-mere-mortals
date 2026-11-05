# The Configuration File

One file runs everything: `/etc/suricata/suricata.yaml`,
2,173 lines as shipped. That sounds like a
phone book, but it is a phone book with a
sane order — a handful of sections you will
actually touch, standing in front of long
stretches of tuning you can leave alone for
months. This chapter walks the sections in
the order they appear and names what each is
for. YAML rules apply throughout: indentation
is structure, and a stray space is a syntax
error that `suricata -T` will find for you.

## `vars` — the address book (line 15)

The file opens by naming the networks the
rules will talk about:

```yaml
vars:
  address-groups:
    HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
    EXTERNAL_NET: "!$HOME_NET"
    HTTP_SERVERS: "$HOME_NET"
    DNS_SERVERS: "$HOME_NET"
```

Rules are written against these names — `$HOME_NET`,
`$EXTERNAL_NET` (everything *not* home) — so
the same ruleset works in every house. **This
is the first thing to set on a real install:**
if your network is `192.168.7.0/24`, say so
here, or rules written to protect home
servers will watch the wrong crowd. Two honest
details from the shipped defaults: the three
private ranges are all claimed as home, which
is generous; and **loopback is not in
`HOME_NET`** — traffic to `127.0.0.1` counts
as external by the `!` definition. The lab in
chapter 7 writes its rule with `any` for
addresses precisely so this subtlety cannot
hide its traffic.

## `outputs` — what gets written (line 82)

One long section switches each output on or
off and names its file. The three this guide
lives in, all on by default:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
  - fast:
      enabled: yes
      filename: fast.log
  - stats:
      enabled: yes
      filename: stats.log
```

`eve-log` is the structured record (chapter 6);
`fast` is the one-line-per-alert classic;
`stats` is the engine's own counters. Others
on the shelf — packet logs, TLS session logs,
unified2 for ancient tooling — start disabled
or niche. Where the files land follows
`default-log-dir` (line 61, `/var/log/suricata/`)
or the `-l` flag on the command line, which is
how every lab run in this guide keeps its
output in the lab.

## `app-layer` — the protocol readers (line 866)

The longest section: one block per protocol
Suricata can rebuild — HTTP, TLS, DNS, SMB,
and dozens more, each with an on/off switch
and its parser's tolerances. Two lessons here.
First, a protocol switched off is invisible to
every rule written for it; troubleshooting a
silent rule starts by checking its parser is
enabled. Second, this section is why Suricata
outruns a byte-searcher: the HTTP block does
not find "something like a request" — it
parses requests properly, which is what lets
a rule say "the word *pangolin* in the
**address** of the request" and mean it
(chapter 7).

## The capture sections

Four blocks describe ways packets arrive, and
the offline/online split of this guide lives
in them:

| Section (line) | What it configures |
|---|---|
| `af-packet:` (614) | Live capture from Linux interfaces — the normal way in |
| `af-xdp:` (695), `dpdk:` (744) | Faster, more specialised live capture for heavy traffic |
| `pcap:` (806) | Live capture through the portable pcap library |
| `pcap-file:` (838) | Replay settings for recorded files — checksum handling lives here |

For a first install, the only line of these
you may meet is the interface name inside
`af-packet` (`interface: eth0` as shipped) —
and on a modern setup you name the interface
on the command line instead and leave the
file alone.

## Rules, thresholds, and the tail

Near the end (line 2152), the file lists which
rule files to load:

```yaml
default-rule-path: /var/lib/suricata/rules
rule-files:
  - suricata.rules
```

One merged file, built by `suricata-update`
(chapter 5). Around it sit `classification-file`
and `reference-config-file` (where alert
categories and reference links are defined)
and room for `threshold-file` — suppressions
you write when a rule is true but useless on
your network. Engine-wide settings (threading,
memory, `host-mode`) occupy the middle
stretches; chapter 8 touches the runmode ones.

**Check:** change nothing yet. Run
`suricata -T -c /etc/suricata/suricata.yaml`
and get either the clean pass of chapter 2
or, on a virgin install, its one expected
warning. Then make one harmless edit — set
`HOME_NET` to your real network in a *copy*
of the file (`cp suricata.yaml ~/lab.yaml`)
and test the copy with `-c ~/lab.yaml` — and
you have the working habit of this whole
guide: **edit, test with `-T`, then run.**
