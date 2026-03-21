# OSINT Reconnaissance – InnovateTech Solutions (fictional target)
# CS 475 Week 6 – Mária Nyolcas
#
# Simulates a structured passive OSINT investigation against a fictional
# aerospace/materials R&D company.  All data is invented for this exercise.
# No real organisation, domain, or individual is referenced.
#
# Steps mirror the lab exercise:
#   1. target scope definition
#   2. passive web recon (WHOIS, Wayback, search operators)
#   3. employee / personnel profiling
#   4. technical footprinting (DNS, crt.sh, Shodan-style)
#   5. synthesised intelligence profile

from dataclasses import dataclass, field


@dataclass
class OsintFinding:
    source: str
    info_type: str
    detail: str
    adversarial_value: str   # what an attacker could do with this


@dataclass
class Employee:
    name: str
    role: str
    platform: str
    exposed_data: str


@dataclass
class DnsRecord:
    record_type: str
    value: str
    notes: str


TARGET = {
    "company":  "InnovateTech Solutions",
    "domain":   "innovatech-solutions.io",
    "sector":   "Advanced materials / aerospace R&D",
    "hq":       "Munich, Germany",
    "founded":  2014,
}

# Step 2 – passive web recon findings
WEB_FINDINGS: list[OsintFinding] = [
    OsintFinding(
        source="company website",
        info_type="technology stack",
        detail="Job postings reference ANSYS 2023 R2, Python 3.11, GitLab CE self-hosted",
        adversarial_value="identifies exact software versions for known-CVE targeting",
    ),
    OsintFinding(
        source="WHOIS (who.is)",
        info_type="registrar / admin contact",
        detail="registered 2019-03-14, registrar Namecheap, admin email it-admin@innovatech-solutions.io",
        adversarial_value="admin email usable in spear-phishing pretext",
    ),
    OsintFinding(
        source="Wayback Machine",
        info_type="legacy infrastructure",
        detail="2021 snapshot of careers page lists VPN product 'Cisco AnyConnect 4.9'",
        adversarial_value="reveals VPN version; CVE-2021-1247 affects AnyConnect < 4.9.04043",
    ),
    OsintFinding(
        source="GitHub public repo (innovatech-dev)",
        info_type="accidentally committed secret",
        detail="config.yml pushed 2022-11-03 contains internal subnet 10.50.0.0/16 and staging hostname sim-lab01.internal",
        adversarial_value="internal network topology; direct reconnaissance target for lateral movement",
    ),
    OsintFinding(
        source="EPO patent database",
        info_type="R&D direction",
        detail="3 patents filed 2022-2024 on carbon-fibre bonding agent, inventors listed by name",
        adversarial_value="identifies key researchers and active IP areas for targeted theft",
    ),
]

# Step 3 – employee profiling
EMPLOYEES: list[Employee] = [
    Employee(
        name="Dr. K. Brenner",
        role="Head of Materials Research",
        platform="LinkedIn",
        exposed_data="lists ANSYS, MATLAB, internal project 'ComposiX-II' in experience section",
    ),
    Employee(
        name="T. Okafor",
        role="Senior IT Administrator",
        platform="LinkedIn + GitHub",
        exposed_data="GitHub profile shows contributions to innovatech-dev/infra-scripts; last commit references Vault token path",
    ),
    Employee(
        name="M. Hofer",
        role="Junior R&D Engineer",
        platform="GitHub",
        exposed_data="committer of the 2022 config.yml leak; email address visible in git log",
    ),
    Employee(
        name="Dr. A. Reyes",
        role="Lead Aerospace Engineer",
        platform="ResearchGate + LinkedIn",
        exposed_data="3 co-authored patents; conference bio names active research project and lab location",
    ),
]

# Step 4 – technical footprinting
DNS_RECORDS: list[DnsRecord] = [
    DnsRecord("A",     "185.220.101.47",          "main web server, hosted DE datacenter"),
    DnsRecord("MX",    "mail.innovatech-solutions.io", "self-hosted mail; no DMARC record found"),
    DnsRecord("NS",    "ns1.namecheap.com",        "standard registrar NS"),
    DnsRecord("TXT",   "v=spf1 include:sendgrid.net ~all", "SPF present but softfail (~all) – spoofing partially possible"),
    DnsRecord("CNAME", "gitlab.innovatech-solutions.io -> 185.220.101.52", "self-hosted GitLab exposed on internet"),
]

CRT_SH_FINDINGS = [
    "gitlab.innovatech-solutions.io",
    "sim-lab01.innovatech-solutions.io",
    "vpn.innovatech-solutions.io",
    "dev-api.innovatech-solutions.io",
]

DEFENSIVE_RECOMMENDATIONS = [
    "Remove specific product versions from job postings; use generic descriptions.",
    "Add DMARC (p=reject) to the mail domain to prevent spoofed sender abuse.",
    "Rotate or revoke the Vault token path visible in T. Okafor's GitHub commit.",
    "Move self-hosted GitLab behind a VPN or IP allowlist; it is unnecessarily internet-exposed.",
    "Implement a secrets-scanning pre-commit hook (e.g. gitleaks) to catch accidental leaks.",
    "Audit crt.sh subdomains; sim-lab01 and dev-api should not appear in public cert logs.",
]


def print_findings(findings: list[OsintFinding]) -> None:
    print(f"\npassive web recon – {len(findings)} findings")
    print(f"  {'source':<28} {'type':<25} detail")
    print(f"  {'-'*27} {'-'*24} {'-'*35}")
    for f in findings:
        print(f"  {f.source:<28} {f.info_type:<25} {f.detail[:55]}")


def print_employees(employees: list[Employee]) -> None:
    print(f"\nemployee profiling – {len(employees)} persons of interest")
    for e in employees:
        print(f"  {e.name} | {e.role} | {e.platform}")
        print(f"    exposed: {e.exposed_data[:80]}")


def print_dns(records: list[DnsRecord], subdomains: list[str]) -> None:
    print(f"\ntechnical footprinting")
    print(f"  {'type':<8} {'value':<40} notes")
    print(f"  {'-'*7} {'-'*39} {'-'*30}")
    for r in records:
        print(f"  {r.record_type:<8} {r.value:<40} {r.notes[:50]}")
    print(f"\n  crt.sh subdomains: {', '.join(subdomains)}")


def print_recommendations(recs: list[str]) -> None:
    print(f"\ndefensive recommendations")
    for i, r in enumerate(recs, 1):
        print(f"  {i}. {r}")


if __name__ == "__main__":
    print(f"osint recon – week 6 lab")
    print(f"target: {TARGET['company']}  ({TARGET['domain']})")
    print(f"sector: {TARGET['sector']}")

    print_findings(WEB_FINDINGS)
    print_employees(EMPLOYEES)
    print_dns(DNS_RECORDS, CRT_SH_FINDINGS)
    print_recommendations(DEFENSIVE_RECOMMENDATIONS)

    print(f"\nattack surface summary")
    print(f"  most critical: leaked subnet + GitLab self-hosted + no DMARC")
    print(f"  highest-value target: Dr. K. Brenner (research lead, named on patents)")
    print(f"  easiest entry: spear-phish M. Hofer (junior, already leaked secrets once)")
