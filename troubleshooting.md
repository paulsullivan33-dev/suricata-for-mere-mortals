# Troubleshooting

Symptom → cause → fix. Every entry below was
either met in this guide's lab or follows
directly from a mechanism the lab proved.

| Symptom | Likely cause | Fix |
|---|---|---|
| `suricata -T` fails: "No rule files match the pattern … suricata.rules" | Fresh install; no ruleset fetched yet | Run `sudo suricata-update` (chapter 5), then test again |
| `-T` fails naming a rule file and line | A syntax error in a rule — usually yours | Read the named line; the engine points at the broken rule precisely. Test local rules alone with `-S` |
| Replay reports "read 1 file, 0 packets" | The capture is empty, truncated, or not a pcap | `capinfos file.pcap` for the truth; re-record or re-generate |
| Offline run succeeds, `fast.log` empty, `eve.json` has `http` events | No rule matched — possibly the correct answer | Check against a trigger you control (chapter 7's pair); silence with evidence of sight is health, not failure |
| `eve.json` entirely empty after a replay | The engine saw nothing it could parse, or outputs are off | Confirm `decoder.pkts` in `stats.log`; check the capture really holds traffic (tshark); confirm `eve-log` is enabled in `outputs` |
| Your rule never fires, though the traffic is in the capture | Wrong sticky buffer, wrong direction, or the protocol parser never claimed the flow | Test the pattern with `content` alone first; check `app_layer.flow.<proto>` in `stats.log`; confirm the parser is enabled (chapter 3) and the port is one it watches |
| Your rule fires on the control capture too | The pattern is too wide — it matched something ordinary | Narrow the buffer (`http_uri`, not the whole request) or the pattern; a rule is only tested when a control acquits |
| Alert shows `[Classification: (null)] [Priority: 3]` | The rule has no `classtype` | Add one from `classification.config` (chapter 7's footnote) |
| Rule works on loopback in the lab, not on the real network | Address groups: your rule says `$HOME_NET`, the traffic's real addresses differ — or the traffic never crosses the sensor | Re-read the `vars` section (chapter 3); then the placement seats (chapter 10) |
| Live start fails: "failed to create AF_PACKET socket: Operation not permitted" | No privilege to capture — wrong user, missing capabilities, or a sandbox/container that forbids capture sockets | Run as root or with the packaged service's capabilities; on a restricted sandbox, live capture may be impossible by design — offline still works |
| Engine starts, sees nothing live | Wrong interface, or a switch port that carries no one else's traffic | Chapter 8's three checks; chapter 10 on mirror ports |
| Startup takes half a minute | The full ruleset is being compiled — measured here at ~30 s for 53,316 rules | Normal. Only chase it if restarts are frequent; rule count, not packet count, sets this cost |
| `stats.log` shows rising `capture.kernel_drops` in live runs | The engine is undersized for the traffic rate | More threads/cores, a busier runmode (chapter 8), or less traffic offered (a narrower mirror) |
| Disk fills with logs | `eve.json` on a busy sensor grows without mercy | Rotate and compress logs; keep `stats` and alerts long, bulk events shorter; the retention choice is yours to make deliberately |

One habit outranks every row: **change one
thing, then re-run the proven pair.** The
trigger/control captures of chapter 4 turn
most mysteries above into a five-second
experiment — if a fix is real, the trigger
still fires and the control still acquits.
