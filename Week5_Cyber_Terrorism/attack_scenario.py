# Attack Scenario Design – Exercise 3
# CS 475 Week 5 – Mária Nyolcas
#
# A fictional but realistic attack scenario against a hospital network,
# mapped to the Lockheed Martin Cyber Kill Chain (7 stages).
# Each step includes a countermeasure and a framework reference.
#
# Target sector   : Hospital / emergency medical services network
# Threat actor    : "Iron Caduceus" (fictional, nation-state APT)
# Kill chain ref  : Lockheed Martin (https://www.lockheedmartin.com/cyber-kill-chain)

from dataclasses import dataclass


@dataclass
class ThreatActor:
    name: str
    actor_type: str
    motivation: str
    capability: str
    resources: str
    notes: str


@dataclass
class KillChainStep:
    stage_number: int
    stage_name: str          # Lockheed Martin stage label
    attacker_action: str
    technique_type: str      # general category, no specific tool required
    goal: str
    countermeasure: str
    framework_reference: str
    is_weakest_link: bool = False


ACTOR = ThreatActor(
    name="Iron Caduceus",
    actor_type="Nation-state APT",
    motivation=(
        "Political coercion – the sponsoring state aims to pressure a government "
        "into concessions during ongoing treaty negotiations by demonstrating the "
        "ability to disrupt emergency medical services."
    ),
    capability="Advanced",
    resources="State-level (dedicated operators, custom malware, SIGINT support)",
    notes=(
        "Iron Caduceus is entirely fictional and created for this exercise. "
        "Any similarity to documented groups is coincidental and unintentional."
    ),
)

KILL_CHAIN: list[KillChainStep] = [
    KillChainStep(
        stage_number=1,
        stage_name="Reconnaissance",
        attacker_action=(
            "Passive OSINT collection over 4-6 weeks: LinkedIn profiles of IT and "
            "clinical staff, hospital job postings revealing technology stack (specific "
            "EHR vendor named, VPN product referenced), public conference presentations "
            "by hospital CISO, domain registration and hosting data, social media posts "
            "by employees inadvertently disclosing system details."
        ),
        technique_type="Passive OSINT (no active scanning, no network contact)",
        goal=(
            "Build a detailed picture of the target's attack surface, personnel, "
            "technology stack, and likely patch levels without triggering any "
            "IDS alerts."
        ),
        countermeasure=(
            "Implement a staff social media policy that prohibits disclosure of "
            "internal technology names. Review public job postings to remove "
            "specific product names. Conduct periodic OSINT audits of your own "
            "organisation's public footprint."
        ),
        framework_reference="CIS Control 14 (Security Awareness and Skills Training); "
                            "ISO/IEC 27001 A.7.2.2 (Information Security Awareness)",
    ),
    KillChainStep(
        stage_number=2,
        stage_name="Weaponisation",
        attacker_action=(
            "Craft a spear-phishing email impersonating the EHR vendor's support team, "
            "referencing the specific product version identified in step 1. Attach a "
            "malicious Word document exploiting a known macro vulnerability in older "
            "Office versions, delivering a custom implant that beacons over HTTPS "
            "to attacker-controlled infrastructure."
        ),
        technique_type="Spear-phishing with malicious attachment (macro-based dropper)",
        goal=(
            "Prepare a highly targeted payload that is convincing enough that a "
            "busy clinical IT staff member will open it without suspicion."
        ),
        countermeasure=(
            "Disable Office macros by Group Policy for all users who do not "
            "require them. Enable Protected View. Deploy email sandboxing that "
            "detonates attachments before delivery."
        ),
        framework_reference="NIST CSF PR.AT-1 (Awareness and Training); "
                            "CIS Control 9 (Email and Web Browser Protections)",
        is_weakest_link=True,
    ),
    KillChainStep(
        stage_number=3,
        stage_name="Delivery",
        attacker_action=(
            "Send the phishing email to three IT administrators identified via LinkedIn, "
            "timing delivery for Monday morning when staff are busy catching up on weekend "
            "notifications. A second wave targets a procurement officer who regularly "
            "receives vendor documents."
        ),
        technique_type="Targeted email delivery (spear-phishing)",
        goal=(
            "Get at least one recipient to open the attachment in an environment "
            "where macros execute."
        ),
        countermeasure=(
            "Train staff to report suspicious emails rather than open them. "
            "Run regular phishing simulation exercises. Implement DMARC, DKIM, "
            "and SPF to reduce spoofed-sender success rate."
        ),
        framework_reference="NIST CSF PR.AT-1; CIS Control 9; ISO/IEC 27001 A.12.2.1",
    ),
    KillChainStep(
        stage_number=4,
        stage_name="Exploitation",
        attacker_action=(
            "The macro executes when the procurement officer enables editing. "
            "The implant uses a living-off-the-land technique: it invokes PowerShell "
            "via a spawned child process to download a second-stage payload from a "
            "domain registered the previous week, disguised as a CDN subdomain. "
            "The initial foothold runs entirely in memory to avoid file-based AV detection."
        ),
        technique_type="Macro-to-PowerShell dropper; in-memory execution; LOTL",
        goal=(
            "Establish a persistent, low-noise foothold on the procurement officer's "
            "workstation inside the hospital network perimeter."
        ),
        countermeasure=(
            "Deploy an EDR (Endpoint Detection and Response) solution that monitors "
            "process lineage – a Word process spawning PowerShell is a high-confidence "
            "detection signal. Enable PowerShell script block logging and constrained "
            "language mode."
        ),
        framework_reference="NIST CSF DE.CM-4 (Detection: Malicious Code); "
                            "CIS Control 10 (Malware Defences)",
    ),
    KillChainStep(
        stage_number=5,
        stage_name="Installation",
        attacker_action=(
            "The second-stage implant establishes persistence via a scheduled task "
            "and a registry Run key, both named to resemble legitimate system processes. "
            "It performs internal network reconnaissance using only built-in tools "
            "(net, ipconfig, arp) to map the EHR server subnet."
        ),
        technique_type="Scheduled task / registry persistence; passive internal recon (LOTL)",
        goal=(
            "Ensure the implant survives reboots and begin mapping the path to "
            "the EHR database servers and medical device network segments."
        ),
        countermeasure=(
            "Monitor scheduled task creation and registry Run key modification events "
            "via SIEM. Apply network segmentation so that a workstation in procurement "
            "cannot directly reach EHR servers without passing through a firewall."
        ),
        framework_reference="CIS Control 13 (Network Monitoring and Defence); "
                            "NIST CSF PR.AC-4 (Access Control: Least Privilege)",
    ),
    KillChainStep(
        stage_number=6,
        stage_name="Command and Control",
        attacker_action=(
            "The implant establishes a beaconing C2 channel over HTTPS to an "
            "attacker-controlled server, using a domain-fronting technique to disguise "
            "traffic as legitimate CDN requests. Beacon interval is randomised between "
            "15 and 45 minutes to evade time-based detection rules."
        ),
        technique_type="HTTPS C2 with domain fronting; jitter-based beaconing",
        goal=(
            "Maintain reliable, stealthy communication with the implant to issue "
            "commands and exfiltrate reconnaissance data."
        ),
        countermeasure=(
            "Implement TLS inspection on outbound traffic to detect unusual certificate "
            "chains characteristic of domain fronting. Use DNS-based threat intelligence "
            "feeds to flag newly registered domains. Alert on HTTPS connections to "
            "domains with no prior browsing history for that host."
        ),
        framework_reference="NIST CSF DE.CM-1 (Network Monitoring); "
                            "CIS Control 13 (Network Monitoring and Defence)",
    ),
    KillChainStep(
        stage_number=7,
        stage_name="Actions on Objectives",
        attacker_action=(
            "Using credentials harvested from the procurement workstation, the actor "
            "moves laterally to a clinical workstation with access to the EHR system. "
            "A wiper payload is staged on the EHR server file share. On a pre-selected "
            "date, the wiper executes, encrypting patient records and overwriting "
            "backups accessible from the domain. A ransom note is displayed, but no "
            "decryption key exists – the goal is disruption, not extortion."
        ),
        technique_type="Credential-based lateral movement; wiper deployment; backup destruction",
        goal=(
            "Cause maximum operational disruption to emergency medical services, "
            "forcing the hospital to revert to paper-based processes and demonstrating "
            "the capability to cause real-world harm."
        ),
        countermeasure=(
            "Maintain offline or immutable backups on a network segment unreachable "
            "from domain-joined systems (3-2-1 backup rule). Enforce privileged access "
            "workstations for EHR administration. Conduct tabletop exercises for "
            "the scenario of EHR unavailability."
        ),
        framework_reference="NIST CSF RC.RP-1 (Recovery Planning); "
                            "ISO/IEC 27001 A.17.1 (Business Continuity); "
                            "CIS Control 11 (Data Recovery)",
    ),
]



def print_actor(a: ThreatActor) -> None:
    print(f"\nactor: {a.name}  ({a.actor_type})")
    print(f"  capability : {a.capability}  |  resources: {a.resources}")
    print(f"  motivation : {a.motivation[:90]}")


def print_chain(chain: list[KillChainStep]) -> None:
    print(f"\nattack chain – Lockheed Martin Cyber Kill Chain")
    for step in chain:
        marker = "  <-- weakest link" if step.is_weakest_link else ""
        print(f"  {step.stage_number}. {step.stage_name}{marker}")
        print(f"     technique : {step.technique_type}")
        print(f"     counter   : {step.countermeasure[:80]}")
        print(f"     framework : {step.framework_reference.split(';')[0]}")


def print_weakest_link(chain: list[KillChainStep]) -> None:
    wl = next(s for s in chain if s.is_weakest_link)
    print(f"\nweakest link: step {wl.stage_number} – {wl.stage_name}")
    print("  if phishing is caught before the attachment opens, the chain collapses here.")
    print("  training + email filtering has the highest defensive ROI at this stage.")


if __name__ == "__main__":
    print("attack scenario design – week 5 lab")
    print("target: hospital / emergency medical services network")

    print_actor(ACTOR)
    print_chain(KILL_CHAIN)
    print_weakest_link(KILL_CHAIN)

    print(f"\n{'step':<5} {'stage':<22} {'weakest?':<10} framework")
    print(f"{'-'*4} {'-'*21} {'-'*9} {'-'*30}")
    for s in KILL_CHAIN:
        wl = "YES" if s.is_weakest_link else ""
        ref_short = s.framework_reference.split(";")[0]
        print(f"{s.stage_number:<5} {s.stage_name:<22} {wl:<10} {ref_short}")
    print()
