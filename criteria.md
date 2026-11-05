# Writing Criteria

Every guide in this repo is written to the same
standard. If you're adding or editing a guide —
human or AI — hold it to these.

1. **Plain words, real ideas.** Simple language,
   never dumbed-down concepts. Explain jargon on
   first use; collect terms in the glossary.
2. **No hype.** No marketing adjectives, no
   "revolutionary," no promises about what
   something will do for the reader.
3. **Honest about limits.** Say what the thing
   *can't* do. State uncertainty instead of
   smoothing it over. Validation notes include
   what remains unverified.
4. **No invented numbers.** Benchmarks, defaults,
   and specs are either measured or qualified with
   "depends on your setup." If it wasn't tested,
   say so.
5. **Checkable.** Commands are meant to be run,
   with "Check:" blocks showing what success looks
   like. Sources are linked, not asserted.
6. **Respect the reader's setup.** Call out
   Windows/Mac/Linux differences. Don't assume a
   GPU, a budget, or prior experience.
7. **Safety isn't skipped.** Real risks get
   stated plainly, not buried.
8. **Scoped.** Each guide says what it covers and
   points elsewhere for the rest. No guide
   pretends to be the whole subject.
9. **Structure over prose.** Tables, before/after
   examples, symptom → fix. Scannable beats essay.

## Verification notes for this guide

Standard 3 and 4 applied to this guide,
specifically. The lab ran on the build machine
with **Suricata 7.0.3** (Ubuntu package
1:7.0.3-1build3). All transcripts are kept with
the lab (`suricata-lab/transcripts/`, 16
files); the chapters quote them trimmed but
unaltered.

**Run for real, captured:**

- *Inventory.* `suricata -V` (7.0.3 RELEASE;
  there is no `--version` flag — bare
  `suricata` prints usage); the
  `--build-info` feature string (AF_PACKET,
  AF_XDP, NFQ, PCRE_JIT, Lua, Rust, NSS,
  HTTP2_DECOMPRESSION, MAGIC); the stock
  `/etc/suricata` tree — `suricata.yaml`
  measured at 2,173 lines / 85,175 bytes, 22
  shipped event-rule files in
  `/etc/suricata/rules/`, and
  `/var/lib/suricata/rules/` empty.
- *The fresh-install surprise.* `suricata -T`
  on the virgin install exited 1 with "No
  rule files match the pattern
  /var/lib/suricata/rules/suricata.rules"
  (twice). A stock install has the engine and
  no detection rules; chapter 2 is written
  around exactly this evidence.
- *The update.* `suricata-update` fetched its
  one default enabled source (ET Open) and
  merged: 69,281 rule lines written to
  `/var/lib/suricata/rules/suricata.rules`
  (44 MB), 53,316 enabled, 14 disabled by the
  set itself, 136 enabled for flowbit
  dependencies; the updater finished by
  running `suricata -T` itself. First fetch
  took about 56 seconds on this machine.
  Afterwards `suricata -T` exited 0:
  "Configuration provided was successfully
  loaded."
- *Ruleset census.* From the merged file:
  52,080 rules with ET messages, 915 GPL,
  320 SURICATA. One ET rule is quoted verbatim
  in chapter 5 (Feodo tracker, sid 2404300,
  rev 8096).
- *The captures.* Live capture is impossible
  in this sandbox (below), so the lab's two
  captures were **synthesised with scapy
  2.5.0** (installed for the purpose): complete
  TCP sessions carrying real HTTP requests and
  responses whose bodies are the fixture
  pages; the generator ships in `examples/`.
  `trigger.pcap`: 24 packets, 3 requests
  (`/`, `/pangolin-survey.html`,
  `/field-notes.html`), confirmed by tshark
  before Suricata ran. `control.pcap`: 16
  packets, 2 requests, neither the pangolin
  page.
- *The rule firing.* Offline run, local rule
  only (`-S local.rules`): wall time 0.38 s;
  "read 1 file, 24 packets, 2316 bytes";
  exactly **1 alert**, sid 9000001, on the
  pangolin flow (127.0.0.1:41002 →
  127.0.0.1:18085), in both `fast.log` and
  `eve.json`; `stats.log` reconciles —
  decoder.pkts 24, tcp.sessions 3,
  app_layer.flow.http 3, detect.alert 1.
- *The control acquitting.* Same rule, control
  capture: 0 alerts, `fast.log` empty, while
  `eve.json` still recorded 2 `http` and 2
  `flow` events — the engine saw the innocent
  traffic and let it pass. Trigger-run EVE
  census: alert 1, http 3, flow 3, fileinfo 3,
  stats 1.
- *The classtype footnote.* The rule was first
  run **without** `classtype`: it fired with
  `[Classification: (null)] [Priority: 3]`.
  Adding `classtype:policy-violation` and
  re-running produced "Potential Corporate
  Privacy Violation" / Priority 1. Both runs
  are real; chapter 7 teaches from the pair.
- *The full ruleset against the trigger.*
  Same 24 packets, no `-S`: the engine log
  records "53316 rules successfully loaded,
  0 rules failed" and "53321 signatures
  processed. 1253 are IP-only rules, 4531 are
  inspecting packet payload, 47304 inspect
  application layer, 108 are decoder event
  only". Alerts on the benign traffic: **0**.
  Wall time 29.7 s, against 0.38 s for the
  one-rule run — the difference is rule
  compilation, measured, not asserted.

**Documented-only (not run), and why:**

- *Live capture on any interface* — the
  sandbox holds no capture privilege:
  `tcpdump` is refused ("You don't have
  permission to perform this capture on that
  device") and Suricata itself fails with
  "af-packet: lo: failed to create AF_PACKET
  socket: Operation not permitted", exit 1,
  both as root (transcript 15). Chapter 8 is
  built from the shipped configuration, the
  captured `--list-runmodes` output, and the
  manual, and says so on its face.
- *IPS / inline operation* (NFQUEUE verdicts,
  AF_PACKET bridge forwarding, `drop` actually
  dropping) — impossible without live capture
  and forwarding; chapter 9 is documented for
  the same reason. The one alert this guide
  fired carries `"action": "allowed"` because
  IDS mode only watches; no blocked action was
  observed anywhere in the lab.
- *Home placement in practice* — no managed
  switch, mirror port, or router seat exists
  in the sandbox; chapter 10 is survey and
  reasoning, labelled as such.
- *Throughput and tuning claims* — thread
  counts, drop rates under load, and any
  packets-per-second figure would need live
  traffic at rates a sandbox cannot offer;
  the guide quotes no such numbers.
- *Windows and macOS use* — builds exist;
  nothing here ran them. Platform remarks are
  from the project's documentation.

Sandbox state after the build, for the record:
the suricata and python3-scapy packages remain
installed; the ET Open ruleset remains fetched
in `/var/lib/suricata/rules/`; the lab
directory inside this checkout keeps its
captures, fixture pages, rule, generator, and
transcripts. No service was started, no
interface was captured from, and no traffic
other than the lab's own synthetic loopback
conversations was ever read.
