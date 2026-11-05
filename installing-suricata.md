# Installing Suricata

On Debian and Ubuntu, Suricata is one package:

```
$ sudo apt-get install suricata
```

That is how this guide's copy arrived: Suricata
**7.0.3**, Ubuntu package `1:7.0.3-1build3`.
Other doors in: the Open Information Security
Foundation (OISF), which maintains Suricata,
publishes packages and source at
suricata.io; Windows and macOS builds exist but
are the minority path — the project's home
ground is Linux, and everything in this guide
was run there. Version note: there is no
`--version` flag; `suricata -V` prints the
version, and bare `suricata` prints usage.

**Check:** the version and what your build can
do:

```
$ suricata -V
This is Suricata version 7.0.3 RELEASE

$ suricata --build-info | head -3
This is Suricata version 7.0.3 RELEASE
Features: NFQ PCAP_SET_BUFF AF_PACKET HAVE_PACKET_FANOUT
LIBCAP_NG ... PCRE_JIT HAVE_NSS HTTP2_DECOMPRESSION
HAVE_LUA HAVE_LUAJIT ... TLS ... MAGIC RUST
```

Read the feature string as a capability list:
`AF_PACKET` and `NFQ` mean this build can do
live capture and inline blocking on Linux;
`RUST` marks the parts of the engine rewritten
in Rust; `PCRE_JIT` means rule patterns run
through a just-in-time compiler. Your build's
list will differ in detail — that is normal,
and it is why the command exists.

## The files it lays down

Everything lives in two places:

| Path | What it holds |
|---|---|
| `/etc/suricata/suricata.yaml` | The one configuration file: 2,173 lines, about 85 KB as shipped |
| `/etc/suricata/rules/` | 22 small rule files of the engine's own event rules (decoder and protocol anomalies) |
| `/etc/suricata/classification.config` | The list of alert categories and their default priorities |
| `/etc/suricata/reference.config` | Where rule references (CVE numbers, links) point |
| `/etc/suricata/threshold.config` | Suppressions and rate limits you may add |
| `/var/lib/suricata/rules/` | Where downloaded rulesets are merged — **empty on a fresh install** |
| `/var/log/suricata/` | The default home of `eve.json`, `fast.log`, `stats.log` |

## The fresh-install surprise

Test the configuration of a brand-new install:

```
$ sudo suricata -T -c /etc/suricata/suricata.yaml
i: suricata: This is Suricata version 7.0.3 RELEASE running in SYSTEM mode
W: detect: No rule files match the pattern /var/lib/suricata/rules/suricata.rules
W: detect: No rule files match the pattern /var/lib/suricata/rules/suricata.rules
(exit code 1)
```

The engine is installed and healthy; it simply
has **no detection rules yet**. The package
deliberately ships none of the big rulesets —
they change daily, so they are fetched
separately, by `suricata-update` (chapter 5).
Until then, `suricata -T` fails with the
warning above. Remember this moment: it is the
cleanest proof in the whole guide that in
Suricata, the engine and the knowledge are
separate things. Chapter 5 fetches the
knowledge; the same test then answers:

```
i: suricata: Configuration provided was successfully loaded. Exiting.
(exit code 0)
```

**Check:** you are ready to continue when
`ls /etc/suricata/` matches the table above
and `suricata -T` fails *only* with the
"no rule files" warning. Any other complaint
is a real problem, and chapter 12 is the place
to take it.
