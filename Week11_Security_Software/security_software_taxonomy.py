# Week 11 - Part A: Security Software Taxonomy
# CS 475 Introduction to Computer Security
#
# This script structures the theory deliverable for Part 1:
# major families of computer security software mapped to the threats they address
# and their alignment with the NIST Cybersecurity Framework (CSF) functions.

from dataclasses import dataclass


@dataclass
class SecuritySoftwareCategory:
    category: str
    acronym: str
    problem_solved: str
    deployment_layer: str
    nist_csf_functions: list[str]
    representative_tools: list[str]
    key_limitation: str


@dataclass
class DepthLayer:
    layer_name: str
    software_categories: list[str]
    rationale: str


TAXONOMY: list[SecuritySoftwareCategory] = [
    SecuritySoftwareCategory(
        category="Antivirus / Endpoint Detection and Response",
        acronym="AV/EDR",
        problem_solved=(
            "Detects, quarantines, and remediates malicious code on individual hosts using "
            "signature databases, heuristics, and behavioural analysis."
        ),
        deployment_layer="Host (workstation, server, mobile device)",
        nist_csf_functions=["Protect", "Detect", "Respond"],
        representative_tools=["Windows Defender", "ClamAV", "CrowdStrike Falcon (EDR)"],
        key_limitation=(
            "Signature-dependent engines miss novel threats until definitions update; "
            "EDR improves coverage via behaviour but adds performance overhead."
        ),
    ),
    SecuritySoftwareCategory(
        category="Firewall (Host-based and Network)",
        acronym="FW",
        problem_solved=(
            "Enforces access control policies on network traffic by inspecting packet headers "
            "(stateless) or tracking connection state (stateful); next-gen firewalls add "
            "application-layer inspection and threat intelligence."
        ),
        deployment_layer="Perimeter and host (network edge, cloud security groups, OS)",
        nist_csf_functions=["Protect"],
        representative_tools=["Windows Firewall", "iptables/nftables", "pfSense", "Palo Alto NGFW"],
        key_limitation=(
            "A firewall only controls what is explicitly ruled; misconfigured or over-permissive "
            "rulesets provide a false sense of protection. Encrypted tunnels can bypass inspection."
        ),
    ),
    SecuritySoftwareCategory(
        category="Intrusion Detection / Prevention System",
        acronym="IDS/IPS",
        problem_solved=(
            "Monitors network traffic or host activity for indicators of attack. IDS raises alerts; "
            "IPS additionally blocks or resets suspicious connections in real time."
        ),
        deployment_layer="Network tap / inline (IPS), host agent (HIDS)",
        nist_csf_functions=["Detect", "Respond"],
        representative_tools=["Snort", "Suricata", "OSSEC (HIDS)", "Zeek"],
        key_limitation=(
            "Rule-based systems generate false positives; tuning requires ongoing operational "
            "expertise. Encrypted traffic limits depth of inspection without TLS interception."
        ),
    ),
    SecuritySoftwareCategory(
        category="Virtual Private Network Client / Gateway",
        acronym="VPN",
        problem_solved=(
            "Provides confidentiality and integrity for data in transit by creating an authenticated, "
            "encrypted tunnel between endpoint and a trusted gateway. Operationalises cryptographic "
            "knowledge against eavesdropping and man-in-the-middle threats on untrusted networks."
        ),
        deployment_layer="Network (client software + gateway appliance/service)",
        nist_csf_functions=["Protect"],
        representative_tools=["OpenVPN", "WireGuard", "IPsec/IKEv2", "Cisco AnyConnect"],
        key_limitation=(
            "A VPN protects the tunnel, not the endpoint or destination. Misconfigured split-tunneling "
            "can route sensitive traffic outside the protected path."
        ),
    ),
    SecuritySoftwareCategory(
        category="Security Information and Event Management",
        acronym="SIEM",
        problem_solved=(
            "Aggregates and correlates log data from firewalls, endpoints, identity providers, and "
            "applications to support threat detection, incident investigation, and compliance reporting "
            "from a central console."
        ),
        deployment_layer="Enterprise-wide (log aggregation platform, cloud or on-premises)",
        nist_csf_functions=["Identify", "Detect", "Respond", "Recover"],
        representative_tools=["Splunk (free tier)", "Elastic Security (ELK Stack)", "Wazuh", "Microsoft Sentinel"],
        key_limitation=(
            "Usefulness depends entirely on log quality and coverage; misconfigured log sources "
            "produce blind spots. High alert volume without tuning leads to analyst fatigue."
        ),
    ),
    SecuritySoftwareCategory(
        category="Data Loss Prevention",
        acronym="DLP",
        problem_solved=(
            "Identifies and controls the movement of sensitive data (PII, IP, financial records) "
            "to prevent accidental or malicious exfiltration via email, cloud storage, USB, or "
            "web upload channels."
        ),
        deployment_layer="Endpoint agent + network proxy",
        nist_csf_functions=["Protect", "Detect"],
        representative_tools=["Symantec DLP", "Forcepoint DLP", "Microsoft Purview DLP"],
        key_limitation=(
            "Relies on accurate data classification; unclassified or mislabelled data evades "
            "controls entirely. High false-positive rates disrupt legitimate workflows."
        ),
    ),
    SecuritySoftwareCategory(
        category="Vulnerability Scanner",
        acronym="VA",
        problem_solved=(
            "Systematically enumerates known vulnerabilities in software versions, configurations, "
            "and services across hosts and applications, prioritising remediation by CVSS severity."
        ),
        deployment_layer="Network-facing (authenticated or unauthenticated scans against targets)",
        nist_csf_functions=["Identify"],
        representative_tools=["OpenVAS / Greenbone", "Nessus Essentials", "Nikto (web)", "Lynis (host)"],
        key_limitation=(
            "Scans reflect a point-in-time snapshot; new vulnerabilities emerge continuously. "
            "Unauthenticated scans miss host-level issues only visible with OS credentials."
        ),
    ),
    SecuritySoftwareCategory(
        category="Privileged Access Management",
        acronym="PAM",
        problem_solved=(
            "Controls, audits, and time-limits the use of elevated credentials (root, admin, service "
            "accounts) to reduce insider threat and credential theft blast radius."
        ),
        deployment_layer="Identity layer (credential vault + session recording)",
        nist_csf_functions=["Protect", "Detect"],
        representative_tools=["CyberArk PAM", "HashiCorp Vault", "Teleport (open-source)"],
        key_limitation=(
            "PAM is as strong as its onboarding process; accounts never enrolled into the vault "
            "remain uncontrolled. Complex deployments see shadow admin accounts bypass controls."
        ),
    ),
]

DEFENCE_IN_DEPTH: list[DepthLayer] = [
    DepthLayer(
        layer_name="Perimeter",
        software_categories=["Firewall (NGFW)", "IPS (inline)", "VPN gateway"],
        rationale="Controls what traffic enters and leaves the organisation; forms the outermost boundary.",
    ),
    DepthLayer(
        layer_name="Network internal",
        software_categories=["IDS (tap)", "SIEM log ingestion", "Network DLP proxy"],
        rationale="Detects lateral movement and data exfiltration attempts after perimeter bypass.",
    ),
    DepthLayer(
        layer_name="Host",
        software_categories=["AV/EDR", "Host firewall", "HIDS", "VA scanner (authenticated)"],
        rationale="Last-resort detection and containment at the point where malicious code executes.",
    ),
    DepthLayer(
        layer_name="Identity",
        software_categories=["PAM", "MFA enforced by IAM tooling"],
        rationale="Limits credential-based lateral movement and insider privilege escalation.",
    ),
    DepthLayer(
        layer_name="Data",
        software_categories=["DLP", "Encryption at rest (OS/application layer)"],
        rationale="Protects the asset itself even when all other layers have been breached.",
    ),
]

NIST_CSF_SUMMARY = {
    "Identify":  "Understand assets, risks, and vulnerabilities before controls are placed.",
    "Protect":   "Implement safeguards to limit the impact of a potential event.",
    "Detect":    "Develop activities to identify the occurrence of a security event.",
    "Respond":   "Take action regarding a detected security incident.",
    "Recover":   "Restore capabilities impaired by the security event.",
}


def print_taxonomy(items: list[SecuritySoftwareCategory]) -> None:
    print("Part A-1: Security Software Taxonomy")
    print(f"  {'acronym':<8} {'category':<44} {'NIST CSF functions':<34} key limitation")
    print(f"  {'-'*7} {'-'*43} {'-'*33} {'-'*42}")
    for item in items:
        funcs = ", ".join(item.nist_csf_functions)
        print(f"  {item.acronym:<8} {item.category:<44} {funcs:<34} {item.key_limitation[:60]}")


def print_defence_in_depth(layers: list[DepthLayer]) -> None:
    print("\nPart A-2: Defence-in-Depth mapping")
    for layer in layers:
        cats = ", ".join(layer.software_categories)
        print(f"  [{layer.layer_name}]")
        print(f"    Software : {cats}")
        print(f"    Rationale: {layer.rationale}")


def print_nist_csf() -> None:
    print("\nPart A-3: NIST CSF function alignment reference")
    for fn, desc in NIST_CSF_SUMMARY.items():
        print(f"  {fn:<10}: {desc}")


if __name__ == "__main__":
    print("week 11 - part a: security software landscape (theory)")
    print_taxonomy(TAXONOMY)
    print_defence_in_depth(DEFENCE_IN_DEPTH)
    print_nist_csf()
