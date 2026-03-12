# Vulnerability Assessment – lab results parser
# CS 475 Week 3 – Mária Nyolcas
#
# This script encodes the top findings produced by running OpenVAS
# (Greenbone Community Edition) against Metasploitable 2 in the lab.
# Rather than re-running the scanner at report time, the findings are
# stored as structured data so we can query, sort, and display them.
#
# Each finding includes:
#   cve      – CVE identifier
#   cvss     – CVSS v3.1 base score (0.0 – 10.0)
#   severity – label derived from CVSS score bands
#   service  – affected service / port
#   title    – short description
#   what_it_allows – one-sentence attacker capability
#   remediation    – concrete fix
#
# CVSS severity bands (FIRST, 2023):
#   Critical 9.0-10.0 | High 7.0-8.9 | Medium 4.0-6.9 | Low 0.1-3.9

from dataclasses import dataclass, field
from typing import Optional


# data model

@dataclass
class Finding:
    cve: str
    cvss: float
    service: str
    port: int
    title: str
    what_it_allows: str
    remediation: str
    notes: str = ""

    @property
    def severity(self) -> str:
        if self.cvss >= 9.0:
            return "CRITICAL"
        elif self.cvss >= 7.0:
            return "HIGH"
        elif self.cvss >= 4.0:
            return "MEDIUM"
        elif self.cvss > 0:
            return "LOW"
        return "NONE"


# findings from OpenVAS scan of Metasploitable 2 (lab, 2026-03-10)


FINDINGS: list[Finding] = [

    Finding(
        cve="CVE-2011-2523",
        cvss=9.8,
        service="vsftpd",
        port=21,
        title="vsftpd 2.3.4 Backdoor Command Execution",
        what_it_allows=(
            "Attacker sends a specially crafted username containing ':)' which "
            "triggers a hardcoded backdoor in vsftpd 2.3.4, opening a root "
            "shell on port 6200 without any authentication."
        ),
        remediation=(
            "Immediately replace vsftpd 2.3.4 with version 3.0.5 or later "
            "(available via the distribution package manager). If FTP is not "
            "required, disable and remove the service entirely. Prefer SFTP "
            "over FTP for all file transfers."
        ),
        notes="Exploitable remotely with no credentials. CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    ),

    Finding(
        cve="CVE-2007-2447",
        cvss=9.8,
        service="Samba",
        port=445,
        title="Samba 3.0.20 Username map script – Remote Code Execution",
        what_it_allows=(
            "The 'username map script' parameter in smb.conf is evaluated as "
            "a shell command.  An unauthenticated remote attacker can inject "
            "arbitrary OS commands via the username field during MSRPC calls, "
            "gaining a root shell."
        ),
        remediation=(
            "Upgrade Samba to 3.0.25 or later (patched release). Remove or "
            "clear the 'username map script' directive from smb.conf if it is "
            "not in use. Restrict SMB access with firewall rules to trusted "
            "hosts only (port 445/tcp)."
        ),
        notes="One of the most commonly exploited vulnerabilities on Metasploitable 2.",
    ),

    Finding(
        cve="CVE-2012-1823",
        cvss=9.8,
        service="PHP CGI",
        port=80,
        title="PHP CGI Argument Injection – Remote Code Execution",
        what_it_allows=(
            "When PHP is configured as a CGI handler, query string parameters "
            "are passed directly to the PHP binary.  An attacker can inject "
            "command-line flags (e.g. -d allow_url_include=On) or source a "
            "remote file, leading to arbitrary code execution as the web "
            "server user."
        ),
        remediation=(
            "Upgrade PHP to 5.3.13 / 5.4.3 or any later release. Switch from "
            "CGI mode to PHP-FPM or mod_php. As a short-term workaround, add "
            "a rewrite rule to strip query strings that begin with '-' from "
            "PHP script URIs."
        ),
        notes="Affects PHP < 5.3.12 and < 5.4.2. CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    ),

    Finding(
        cve="CVE-2004-2761",
        cvss=5.3,
        service="Apache httpd",
        port=80,
        title="MD5 Collision in SSL/TLS Certificate Signatures",
        what_it_allows=(
            "MD5-signed certificates can be forged by an attacker with "
            "significant computation resources, enabling MITM attacks against "
            "HTTPS traffic."
        ),
        remediation=(
            "Reissue certificates using SHA-256 or later. Configure Apache "
            "SSLProtocol and SSLCipherSuite to disable MD5 and weak ciphers."
        ),
    ),

    Finding(
        cve="CVE-2008-0166",
        cvss=7.8,
        service="OpenSSL (Debian)",
        port=22,
        title="Debian OpenSSL Predictable PRNG – Weak SSH Keys",
        what_it_allows=(
            "Debian-derived systems running a patched OpenSSL (2006-2008) "
            "generated cryptographic keys with only 32,767 possible seeds. "
            "An attacker can pre-compute all possible key pairs and perform "
            "key-guessing to authenticate as any user whose SSH key was "
            "generated during that period."
        ),
        remediation=(
            "Regenerate all SSH host keys and user keys on affected systems. "
            "Upgrade OpenSSL to an unaffected version. Audit authorized_keys "
            "on all servers to remove compromised public keys."
        ),
    ),
]


# display

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "NONE": 4}


def print_findings(findings: list[Finding]) -> None:
    sorted_f = sorted(findings, key=lambda f: (SEVERITY_ORDER[f.severity], -f.cvss))

    print("\nvuln scan results – Metasploitable 2")
    print(f"  {'CVE':<18} {'CVSS':>5}  {'severity':<9} {'port':<6} title")
    print(f"  {'-'*17} {'-'*5}  {'-'*8} {'-'*5} {'-'*35}")

    for f in sorted_f:
        print(f"  {f.cve:<18} {f.cvss:>5.1f}  {f.severity:<9} {f.port:<6} {f.title}")

    print()
    for f in sorted_f:
        print(f"[{f.severity}] {f.cve} – {f.title}")
        print(f"  on: {f.service} (port {f.port})")
        print(f"  CVSS: {f.cvss}")
        print(f"  what it does: {f.what_it_allows}")
        print(f"  fix: {f.remediation}")
        if f.notes:
            print(f"  note: {f.notes}")
        print()


def top_n(findings: list[Finding], n: int = 3) -> list[Finding]:
    return sorted(findings, key=lambda f: -f.cvss)[:n]


if __name__ == "__main__":
    print_findings(FINDINGS)

    print(f"top 3 by CVSS (the ones to fix first):")
    for f in top_n(FINDINGS, 3):
        print(f"  {f.cve}  CVSS={f.cvss}  {f.title}")
