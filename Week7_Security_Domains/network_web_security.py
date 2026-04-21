# Week 7 - Part B: Network and Web Security
# CS 475 Introduction to Computer Security
#
# This script structures Deliverables B-1, B-2, and B-3.
# Targets and results are from local lab setup only (localhost / intentional practice app).

from dataclasses import dataclass


@dataclass
class PortFinding:
    port: int
    service: str
    version: str
    risk_commentary: str


@dataclass
class HeaderCheck:
    header: str
    present: bool
    risk_if_missing: str


@dataclass
class Mitigation:
    vulnerability: str
    root_cause: str
    technical_fix: str
    standard_mapping: str


B1_PORTS: list[PortFinding] = [
    PortFinding(
        port=22,
        service="ssh",
        version="OpenSSH 9.x",
        risk_commentary="Low risk with key-only auth and restricted source IPs; high risk with password auth.",
    ),
    PortFinding(
        port=80,
        service="http",
        version="Apache 2.4.x (DVWA local)",
        risk_commentary="Used for test app; plaintext transport enables interception if used beyond lab scope.",
    ),
    PortFinding(
        port=3306,
        service="mysql",
        version="MariaDB 10.x",
        risk_commentary="Database exposure can enable credential theft and data exfiltration if network-reachable.",
    ),
]


B2_SQLI = {
    "payload": "' OR '1'='1",
    "observation": (
        "Application returned records without valid user context, indicating unsanitized input "
        "was concatenated directly into SQL query logic."
    ),
    "why_it_exists": (
        "Server-side code builds SQL strings from raw user input instead of using parameterized "
        "queries and strict input validation."
    ),
}


B2_XSS = {
    "payload": "<script>alert('XSS proof of concept')</script>",
    "observation": "Browser executed injected JavaScript in reflected context (alert box shown).",
    "why_it_exists": "Application reflects unescaped user input into HTML response body.",
}


B2_HEADERS: list[HeaderCheck] = [
    HeaderCheck(
        header="Content-Security-Policy",
        present=False,
        risk_if_missing="No script execution policy boundary, so injected scripts are harder to contain.",
    ),
    HeaderCheck(
        header="X-Content-Type-Options",
        present=False,
        risk_if_missing="MIME sniffing can cause browser to interpret content as executable unexpectedly.",
    ),
    HeaderCheck(
        header="Strict-Transport-Security",
        present=False,
        risk_if_missing="Clients may downgrade to HTTP, enabling interception and manipulation.",
    ),
    HeaderCheck(
        header="X-Frame-Options",
        present=False,
        risk_if_missing="App can be embedded in attacker iframes, enabling clickjacking attacks.",
    ),
]


B3_MITIGATIONS: list[Mitigation] = [
    Mitigation(
        vulnerability="SQL Injection (OWASP A03:2021 Injection)",
        root_cause=(
            "String-concatenated SQL query construction with untrusted input from user-controlled "
            "request parameters."
        ),
        technical_fix=(
            "Replace dynamic SQL with parameterized prepared statements, enforce allow-list input "
            "validation, and apply least-privilege DB account permissions."
        ),
        standard_mapping="OWASP SQL Injection Prevention Cheat Sheet; CWE-89; NIST SP 800-53 SI-10",
    ),
    Mitigation(
        vulnerability="Reflected XSS (OWASP A03:2021 Injection)",
        root_cause=(
            "Output encoding is missing on reflected user-supplied values, allowing script context "
            "injection in browser responses."
        ),
        technical_fix=(
            "Apply contextual output encoding, server-side input validation, and add CSP to constrain "
            "script sources and inline execution."
        ),
        standard_mapping="OWASP XSS Prevention Cheat Sheet; CWE-79; NIST SP 800-53 SC-5/SC-7",
    ),
]


def print_b1(ports: list[PortFinding]) -> None:
    print("B-1: Port scan summary (local infrastructure)")
    print(f"  {'port':<6} {'service':<10} {'version':<24} risk commentary")
    print(f"  {'-'*5} {'-'*9} {'-'*23} {'-'*40}")
    for p in ports:
        print(f"  {p.port:<6} {p.service:<10} {p.version:<24} {p.risk_commentary}")


def print_b2() -> None:
    print("\nB-2: Web vulnerability analysis")
    print("  SQL Injection test")
    print(f"    payload      : {B2_SQLI['payload']}")
    print(f"    observation  : {B2_SQLI['observation']}")
    print(f"    root issue   : {B2_SQLI['why_it_exists']}")

    print("  Reflected XSS test")
    print(f"    payload      : {B2_XSS['payload']}")
    print(f"    observation  : {B2_XSS['observation']}")
    print(f"    root issue   : {B2_XSS['why_it_exists']}")

    print("\n  HTTP security headers")
    print(f"    {'header':<32} {'present':<8} risk if missing")
    print(f"    {'-'*31} {'-'*7} {'-'*40}")
    for h in B2_HEADERS:
        print(f"    {h.header:<32} {str(h.present):<8} {h.risk_if_missing}")


def print_b3(mitigations: list[Mitigation]) -> None:
    print("\nB-3: Mitigation proposals")
    for i, m in enumerate(mitigations, 1):
        print(f"  {i}. {m.vulnerability}")
        print(f"     root cause : {m.root_cause}")
        print(f"     fix        : {m.technical_fix}")
        print(f"     standard   : {m.standard_mapping}")


if __name__ == "__main__":
    print("week 7 - part b deliverables")
    print_b1(B1_PORTS)
    print_b2()
    print_b3(B3_MITIGATIONS)
