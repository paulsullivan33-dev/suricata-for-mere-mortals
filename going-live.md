# Going Live

**(Documented — not run on the build machine.**
Its sandbox refuses to open a capture socket,
for Suricata exactly as for `tcpdump`:
`af-packet: lo: failed to create AF_PACKET
socket: Operation not permitted`. This chapter
is taught from the shipped configuration, the
engine's own runmode list, and the manual.
The offline chapters, by contrast, were run.)

Everything so far replayed recordings. Live
mode is the same engine with a different
packet source: an interface, watched as
traffic flows. The command grows by one flag:

```
$ sudo suricata -i eth0 -c /etc/suricata/suricata.yaml
```

`-i` names the interface; add `-l` to steer
the logs, and run it as a service
(`systemctl start suricata`, in distributions
that package one) once the foreground version
behaves. On Linux the default capture
mechanism is **AF_PACKET** — the kernel hands
Suricata copies of packets straight from the
interface, which is the "beside the road"
posture of chapter 1: the original traffic
flows on untouched, and a crashed or
restarting Suricata loses eyesight, not
connectivity. That asymmetry is why detection
is the safe first live step.

## Runmodes: who does the work

One interface can outrun one thread, so
Suricata splits labour. The engine lists its
arrangements itself (`suricata --list-runmodes`);
the three you will meet:

| Runmode | Shape | When it fits |
|---|---|---|
| `single` | One thread does everything | Learning, tiny networks, debugging — the offline default too |
| `autofp` | Capture threads hand flows to detection threads; a flow always lands on the same detect thread | The usual live default: several cores, state kept straight |
| `workers` | Every thread is a full pipeline, capture to logging; flows are spread across them | The modern favourite on multi-queue network cards |

The idea to keep is the middle column of
`autofp`: Suricata's verdicts depend on whole
conversations, so whatever else scales, **one
flow must stay on one thread**. Sizing —
threads per mode, CPU affinity, ring sizes —
lives in the configuration's capture sections
and the `threading` settings, and honest
sizing depends on *your* traffic rate, which
no guide can measure for you. The discipline
that transfers: watch `stats.log` for the
`capture.kernel_drops` counter family. Packets
the kernel dropped before Suricata saw them
are holes in the evidence; a rising drop count
is the engine telling you it is undersized,
in its own numbers, before any user notices.

## Before you trust a live sensor

Three checks, in order, all cheap:

1. **It sees.** Generate traffic you control —
   fetch a page from a machine the sensor
   watches — and find the `http` event in
   `eve.json`. No event, no eyesight: wrong
   interface, wrong side of a NAT, or traffic
   that never crosses the watched wire
   (chapter 10's placement problem).
2. **It judges.** Replay your proven lab rule
   locally first (chapter 7), then enable it
   live and make the same fetch. The alert
   should arrive wearing `action: allowed`.
3. **It reconciles.** After an hour, compare
   `stats.log` counters: packets seen versus
   flows closed versus kernel drops. A sensor
   that cannot account for its packets is a
   diary with pages missing.

Permissions deserve their sentence: live
capture needs privilege — root, or the
`CAP_NET_RAW`/`CAP_NET_ADMIN` capabilities the
package's systemd unit grants — because
reading everyone's packets *is* the privilege.
The build machine's refusal, quoted at the
top, is that machinery working as designed.

**Check:** a live deployment is ready when
all three checks pass on traffic you made
yourself. Only then do the 53,316 rules of
chapter 5 start earning their keep — and only
then does chapter 9's question, whether the
watcher may also *stop* traffic, deserve an
answer.
