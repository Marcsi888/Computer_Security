# Espionage Attack Lifecycle – AeroTech GmbH case study
# CS 475 Week 6 – Mária Nyolcas
#
# Encodes the 5-phase composite case study from the module brief
# (fictional, synthesised from documented incidents).
# Maps each phase to ATT&CK tactics, defensive controls, and
# answers the three discussion questions from Section 6.

from dataclasses import dataclass


@dataclass
class Phase:
    number: int
    name: str
    what_happened: str
    attck_tactic: str
    attck_technique: str
    defensive_control: str
    human_factor: str          # role of human behaviour at this phase


PHASES: list[Phase] = [
    Phase(
        number=1,
        name="Reconnaissance",
        what_happened=(
            "Adversary maps AeroTech via LinkedIn, conference programmes, "
            "job postings (engineering sim platform version), EPO patent filings. "
            "A GitHub search finds a config file with internal IP ranges."
        ),
        attck_tactic="Reconnaissance (TA0043)",
        attck_technique="T1591 – Gather Victim Org Info / T1593 – Search Open Websites",
        defensive_control="OSINT hygiene: strip product versions from job posts, secrets scanning on git",
        human_factor="Junior engineer committed config to public repo without malicious intent.",
    ),
    Phase(
        number=2,
        name="Initial Access",
        what_happened=(
            "Researcher receives spear-phishing email impersonating a conference organiser. "
            "Attached PDF exploits an unpatched PDF reader (known CVE) to execute a payload."
        ),
        attck_tactic="Initial Access (TA0001)",
        attck_technique="T1566.001 – Spear-Phishing Attachment",
        defensive_control="Patch PDF reader; email sandboxing; phishing simulation training",
        human_factor="Researcher opened attachment without verifying sender domain.",
    ),
    Phase(
        number=3,
        name="Persistence and Lateral Movement",
        what_happened=(
            "Scheduled task mimicking a Windows maintenance process installed for persistence. "
            "Over 4 weeks attacker pivots through the network using harvested credentials, "
            "reaching the R&D file server."
        ),
        attck_tactic="Persistence (TA0003) + Lateral Movement (TA0008)",
        attck_technique="T1053.005 – Scheduled Task / T1078 – Valid Accounts",
        defensive_control="Network segmentation; least privilege; EDR monitoring process lineage",
        human_factor="Shared service accounts with overly broad access enabled free lateral movement.",
    ),
    Phase(
        number=4,
        name="Collection and Exfiltration",
        what_happened=(
            "~40 GB of technical specs and unpublished research staged in encrypted archives, "
            "exfiltrated over HTTPS to a cloud storage endpoint."
        ),
        attck_tactic="Collection (TA0009) + Exfiltration (TA0010)",
        attck_technique="T1560 – Archive Collected Data / T1567.002 – Exfiltration to Cloud Storage",
        defensive_control="DLP rules on large outbound transfers; TLS inspection; cloud-app controls",
        human_factor="No human detection during this phase; fully automated exfiltration.",
    ),
    Phase(
        number=5,
        name="Detection (Eventual)",
        what_happened=(
            "Breach discovered 6 months later by a security analyst reviewing historical logs "
            "during a routine audit; noticed anomalously large HTTPS transfers to unknown domain."
        ),
        attck_tactic="N/A (defender action)",
        attck_technique="N/A",
        defensive_control="SIEM correlation rules for volume-based anomalies; regular log audits",
        human_factor="Detection relied entirely on analyst intuition during a manual audit.",
    ),
]

# Discussion question answers
DISCUSSION = {
    "Q1_best_disruption_phase": (
        "Phase 2 (Initial Access). Blocking the phishing email or preventing the PDF exploit "
        "from executing stops the attacker before any foothold is established. At every later "
        "phase the defender is playing catch-up inside an already compromised environment. "
        "Specific controls: email gateway sandboxing, mandatory PDF reader patching, and "
        "phishing simulation exercises."
    ),
    "Q2_least_privilege_impact": (
        "If least privilege had been enforced, the procurement workstation would have had no "
        "path to the R&D file server. Lateral movement (Phase 3) would have stalled at the "
        "first network segment boundary, limiting the blast radius to a single low-value host "
        "even after successful initial access."
    ),
    "Q3_human_behaviour": (
        "No phase was purely technical. Phase 1 depended on a junior engineer committing "
        "secrets; Phase 2 on a researcher opening an attachment; Phase 3 on administrators "
        "sharing service accounts; Phase 5 on an analyst reviewing logs manually. "
        "Technology failed at every step because it was misconfigured or absent --- "
        "human decisions created each gap."
    ),
}


def print_lifecycle(phases: list[Phase]) -> None:
    print(f"\nespionage attack lifecycle – AeroTech GmbH (fictional)")
    print(f"  {'#':<3} {'phase':<32} ATT&CK tactic")
    print(f"  {'-'*2} {'-'*31} {'-'*30}")
    for p in phases:
        print(f"  {p.number:<3} {p.name:<32} {p.attck_tactic}")

    print()
    for p in phases:
        print(f"  phase {p.number} – {p.name}")
        print(f"    tactic    : {p.attck_tactic}")
        print(f"    technique : {p.attck_technique}")
        print(f"    defence   : {p.defensive_control}")
        print(f"    human     : {p.human_factor}")


def print_discussion(d: dict) -> None:
    print(f"\ndiscussion answers")
    labels = {
        "Q1_best_disruption_phase": "Q1 – best disruption point",
        "Q2_least_privilege_impact": "Q2 – least privilege impact",
        "Q3_human_behaviour": "Q3 – human behaviour across phases",
    }
    for key, label in labels.items():
        print(f"\n  {label}:")
        text = d[key]
        words = text.split()
        line, col = "    ", 4
        for w in words:
            if col + len(w) + 1 > 72:
                print(line)
                line, col = "    " + w, 4 + len(w)
            else:
                line += (" " if col > 4 else "") + w
                col += len(w) + 1
        print(line)


if __name__ == "__main__":
    print("espionage lifecycle – week 6 lab")
    print_lifecycle(PHASES)
    print_discussion(DISCUSSION)
