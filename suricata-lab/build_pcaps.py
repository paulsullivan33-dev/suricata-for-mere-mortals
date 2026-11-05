#!/usr/bin/env python3
"""Build the lab's packet captures by synthesising complete TCP sessions.

The build sandbox forbids live capture (no CAP_NET_RAW: tcpdump gets
"Operation not permitted" even as root), so the captures are built with
scapy instead: full handshakes, real HTTP requests and responses whose
bodies are the fixture pages, correct checksums. Suricata reads packets,
not provenance, so offline analysis of these files exercises exactly the
same code paths as a tcpdump recording of the same conversation.
"""
from scapy.all import Ether, IP, TCP, Raw, wrpcap

CLIENT = "127.0.0.1"
SERVER = "127.0.0.1"
SPORT = 18085


def page(name):
    with open(f"fixture-www/{name}", "rb") as fh:
        return fh.read()


def session(sport, path, body, t):
    """One short HTTP conversation, as a list of packets."""
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {SERVER}:{SPORT}\r\n"
        "User-Agent: LabBrowser/1.0\r\n"
        "Accept: */*\r\n\r\n"
    ).encode()
    resp = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    ).encode() + body

    cseq, sseq = 1000, 5000
    pkts = []

    def pkt(src, dst, sp, dp, flags, seq, ack, payload=b""):
        p = (Ether(src="00:00:00:00:00:01", dst="00:00:00:00:00:02")
             / IP(src=src, dst=dst)
             / TCP(sport=sp, dport=dp, flags=flags, seq=seq, ack=ack))
        if payload:
            p = p / Raw(load=payload)
        p.time = t
        return p

    pkts.append(pkt(CLIENT, SERVER, sport, SPORT, "S", cseq, 0))
    pkts.append(pkt(SERVER, CLIENT, SPORT, sport, "SA", sseq, cseq + 1))
    cseq += 1
    sseq += 1
    pkts.append(pkt(CLIENT, SERVER, sport, SPORT, "A", cseq, sseq))
    pkts.append(pkt(CLIENT, SERVER, sport, SPORT, "PA", cseq, sseq, req))
    cseq += len(req)
    pkts.append(pkt(SERVER, CLIENT, SPORT, sport, "PA", sseq, cseq, resp))
    sseq += len(resp)
    pkts.append(pkt(CLIENT, SERVER, sport, SPORT, "A", cseq, sseq))
    pkts.append(pkt(CLIENT, SERVER, sport, SPORT, "FA", cseq, sseq))
    pkts.append(pkt(SERVER, CLIENT, SPORT, sport, "A", sseq, cseq + 1))
    return pkts


trigger = []
trigger += session(41001, "/", page("index.html"), 1_700_000_000)
trigger += session(41002, "/pangolin-survey.html",
                     page("pangolin-survey.html"), 1_700_000_005)
trigger += session(41003, "/field-notes.html",
                     page("field-notes.html"), 1_700_000_010)
wrpcap("trigger.pcap", trigger)

control = []
control += session(42001, "/", page("index.html"), 1_700_000_100)
control += session(42002, "/field-notes.html",
                     page("field-notes.html"), 1_700_000_105)
wrpcap("control.pcap", control)

print(f"trigger.pcap: {len(trigger)} packets")
print(f"control.pcap: {len(control)} packets")
