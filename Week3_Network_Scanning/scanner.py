# Network Scanner – lab simulation
# CS 475 Week 3 – Mária Nyolcas
# This script simulates a host discovery + port scan workflow against a
# controlled lab target (Metasploitable 2, 192.168.56.101).  It wraps
# subprocess calls to nmap so the logic is easy to read and the output
# is parsed into structured Python dicts for later analysis.
# Two scan modes are demonstrated:
#   SYN scan  (-sS)  – half-open, less noisy, requires root/CAP_NET_RAW
#   Version   (-sV)  – full connect + banner grab, identifies service versions

import subprocess
import re
import sys


TARGET = "192.168.56.101"      # Metasploitable 2 lab VM
SUBNET = "192.168.56.0/24"    # isolated host-only network


# helpers

def run(cmd: list[str]) -> str:
    """Run a command, return stdout as a string."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def parse_ports(nmap_output: str) -> list[dict]:
    """
    Extract open-port lines from nmap plain-text output.
    Returns a list of dicts with keys: port, protocol, state, service, version.
    """
    ports = []
    for line in nmap_output.splitlines():
        # nmap open-port lines look like:
        #   21/tcp   open  ftp         vsftpd 2.3.4
        m = re.match(
            r"(\d+)/(tcp|udp)\s+(open(?:\|filtered)?)\s+(\S+)\s*(.*)", line
        )
        if m:
            ports.append({
                "port":     int(m.group(1)),
                "protocol": m.group(2),
                "state":    m.group(3),
                "service":  m.group(4),
                "version":  m.group(5).strip(),
            })
    return ports


# Step 1 –> host discovery

def host_discovery(subnet: str) -> list[str]:
    """Ping sweep to find live hosts."""
    print(f"\npinging {subnet} to see what's alive  (nmap -sn)")
    out = run(["nmap", "-sn", subnet])
    print(out)

    live = re.findall(r"Nmap scan report for (.+)", out)
    print(f"live hosts: {live}")
    return live


# Step 2 –> port scans

def syn_scan(target: str) -> list[dict]:
    """SYN / stealth scan – faster, half-open."""
    print(f"\nrunning SYN scan on {target}  (nmap -sS -p- --open)")
    out = run(["nmap", "-sS", "-p-", "--open", "-T4", target])
    print(out)
    ports = parse_ports(out)
    return ports


def version_scan(target: str) -> list[dict]:
    """Version detection scan – slower but reveals service banners."""
    print(f"\nrunning version scan on {target}  (nmap -sV, common ports only)")
    # Scanning only common interesting ports to keep lab time reasonable
    interesting = "21,22,23,25,80,111,139,445,3306,5432,6667,8180"
    out = run(["nmap", "-sV", "-p", interesting, target])
    print(out)
    ports = parse_ports(out)
    return ports


# Step 3 –> print comparison table

def print_table(ports: list[dict], title: str) -> None:
    print(f"\n{title}")
    print(f"  {'port':<8} {'proto':<6} {'state':<8} {'service':<16} version")
    print(f"  {'-'*7} {'-'*5} {'-'*7} {'-'*15} {'-'*20}")
    for p in ports:
        print(f"  {p['port']:<8} {p['protocol']:<6} {p['state']:<8} "
              f"{p['service']:<16} {p['version'][:40]}")



if __name__ == "__main__":
    print(f"network scanner – week 3 lab")
    print(f"target: {TARGET}  |  subnet: {SUBNET}")
    print("reminder: lab network only, don't point this anywhere else\n")
    # A: find live hosts
    live_hosts = host_discovery(SUBNET)

    if TARGET not in " ".join(live_hosts):
        print(f"[!] {TARGET} didn't show up in the sweep – check your network config.")
        sys.exit(1)

    # B: two different scan types
    syn_ports     = syn_scan(TARGET)
    version_ports = version_scan(TARGET)

    # C: side-by-side summary
    print_table(syn_ports,     "SYN Scan Results")
    print_table(version_ports, "Version Scan Results")

    # D: quick attack surface summary
    print(f"\nSYN scan found {len(syn_ports)} open ports")
    print(f"version scan found {len(version_ports)} open ports")

    risky = [p for p in version_ports if p["port"] in (21, 23, 512, 513, 514, 1099, 6667)]
    if risky:
        print("\nlegacy/high-risk services worth flagging:")
        for p in risky:
            print(f"    {p['port']} ({p['service']}) – {p['version']}")

    print("\ndone – see the report for the full analysis.")
