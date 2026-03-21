# Threat Actor Mapping – MITRE ATT&CK
# CS 475 Week 5 – Mária Nyolcas
#
# Exercise 1: maps selected techniques for Sandworm Team and Lazarus Group,
# then compares the two to explore attribution difficulty.
#
# Data drawn from MITRE ATT&CK Enterprise Matrix v15 (https://attack.mitre.org).
# This is a structured representation of publicly available threat intelligence,
# not a live API call – keeping it reproducible without network access.

from dataclasses import dataclass, field


@dataclass
class Technique:
    tid: str
    name: str
    tactic: str
    tactic_id: str
    category: str       # "destruction", "espionage", or "information warfare"
    description: str    # plain-language explanation


@dataclass
class ThreatActor:
    name: str
    aliases: list[str]
    attribution: str    # country / organisation
    motivation: str
    primary_targets: list[str]
    techniques: list[Technique]


SANDWORM = ThreatActor(
    name="Sandworm Team",
    aliases=["APT44", "Voodoo Bear", "IRIDIUM", "Telebots"],
    attribution="Russian GRU – Unit 74455 (Main Centre for Special Technologies)",
    motivation="Destructive attacks and sabotage in support of Russian geopolitical objectives",
    primary_targets=[
        "Energy and power grid operators",
        "Government agencies (Ukraine, EU, US)",
        "Media and telecommunications",
        "Transportation and logistics",
    ],
    techniques=[
        Technique(
            tid="T1486",
            name="Data Encrypted for Impact",
            tactic="Impact",
            tactic_id="TA0040",
            category="destruction",
            description=(
                "Sandworm deploys ransomware-style wipers (NotPetya, BadRabbit) that "
                "encrypt or destroy data with no recovery path. The encryption is a "
                "cover for destruction rather than extortion – victims cannot buy a "
                "decryption key because none exists."
            ),
        ),
        Technique(
            tid="T1059.003",
            name="Command and Scripting Interpreter: Windows Command Shell",
            tactic="Execution",
            tactic_id="TA0002",
            category="destruction",
            description=(
                "The group uses cmd.exe to run batch scripts that disable Windows "
                "Defender, stop backup services, and stage wiper payloads. Using the "
                "built-in shell reduces the need to drop additional tools that might "
                "trigger AV signatures."
            ),
        ),
        Technique(
            tid="T1078",
            name="Valid Accounts",
            tactic="Defence Evasion / Persistence",
            tactic_id="TA0005",
            category="espionage",
            description=(
                "Sandworm harvests and reuses legitimate credentials to move laterally "
                "and maintain persistence. Logging in with real accounts makes the "
                "activity harder to distinguish from normal user behaviour in SIEM logs."
            ),
        ),
        Technique(
            tid="T1071.001",
            name="Application Layer Protocol: Web Protocols",
            tactic="Command and Control",
            tactic_id="TA0011",
            category="information warfare",
            description=(
                "C2 traffic is tunnelled over HTTP/HTTPS, blending with normal web "
                "browsing. This makes it difficult for network defenders to block C2 "
                "without also blocking legitimate web access."
            ),
        ),
        Technique(
            tid="T1561.002",
            name="Disk Structure Wipe",
            tactic="Impact",
            tactic_id="TA0040",
            category="destruction",
            description=(
                "Industroyer2 and the CaddyWiper family overwrite the MBR and partition "
                "tables, making systems unbootable. This is Sandworm's most aggressive "
                "technique – recovery requires full OS reinstallation, causing maximum "
                "operational downtime."
            ),
        ),
    ],
)

LAZARUS = ThreatActor(
    name="Lazarus Group",
    aliases=["APT38", "Hidden Cobra", "ZINC", "Guardians of Peace"],
    attribution="DPRK – Reconnaissance General Bureau (RGB)",
    motivation="Financial theft to fund state programmes; occasional destructive attacks for coercion",
    primary_targets=[
        "Banks and financial institutions",
        "Cryptocurrency exchanges",
        "Defence contractors",
        "Media organisations (destructive campaigns)",
    ],
    techniques=[
        Technique(
            tid="T1486",
            name="Data Encrypted for Impact",
            tactic="Impact",
            tactic_id="TA0040",
            category="destruction",
            description=(
                "Used in the Sony Pictures attack (2014) and WannaCry (2017). Like "
                "Sandworm, Lazarus deploys destructive payloads, though the motivation "
                "here is coercion and distraction rather than pure sabotage."
            ),
        ),
        Technique(
            tid="T1078",
            name="Valid Accounts",
            tactic="Defence Evasion / Persistence",
            tactic_id="TA0005",
            category="espionage",
            description=(
                "Lazarus uses stolen SWIFT operator credentials to authorise fraudulent "
                "bank transfers (Bangladesh Bank heist, 2016). The technique is the same "
                "as Sandworm's – abuse legitimate access – but the goal is financial "
                "rather than destructive."
            ),
        ),
        Technique(
            tid="T1071",
            name="Application Layer Protocol",
            tactic="Command and Control",
            tactic_id="TA0011",
            category="information warfare",
            description=(
                "ELECTRICFISH and other Lazarus implants use custom TCP tunnels "
                "disguised as standard protocols for C2 communication, similar in "
                "principle to Sandworm's HTTP-based C2 channels."
            ),
        ),
    ],
)



def print_actor(actor: ThreatActor) -> None:
    print(f"\n{actor.name}  ({', '.join(actor.aliases[:2])})")
    print(f"  attribution : {actor.attribution}")
    print(f"  motivation  : {actor.motivation}")
    print(f"  targets     : {', '.join(actor.primary_targets)}")
    print(f"  techniques  :")
    for t in actor.techniques:
        print(f"    [{t.tid}] {t.name}  |  {t.tactic}  |  {t.category}")


def compare_actors(a: ThreatActor, b: ThreatActor) -> None:
    tids_a = {t.tid for t in a.techniques}
    tids_b = {t.tid for t in b.techniques}
    shared = tids_a & tids_b
    only_a = tids_a - tids_b
    only_b = tids_b - tids_a

    print(f"\noverlap: {a.name} vs {b.name}")
    print(f"  shared    : {', '.join(sorted(shared))}")
    print(f"  only {a.name[:8]:<8}: {', '.join(sorted(only_a))}")
    print(f"  only {b.name[:8]:<8}: {', '.join(sorted(only_b))}")
    print("  note: shared TTPs do not imply same actor – they are just common techniques")


if __name__ == "__main__":
    print("threat actor mapping – week 5 lab")

    print_actor(SANDWORM)
    print_actor(LAZARUS)
    compare_actors(SANDWORM, LAZARUS)

    print(f"\n{'actor':<18} {'tid':<12} {'tactic':<28} category")
    print(f"{'-'*17} {'-'*11} {'-'*27} {'-'*15}")
    for actor in (SANDWORM, LAZARUS):
        for t in actor.techniques:
            print(f"{actor.name:<18} {t.tid:<12} {t.tactic:<28} {t.category}")
    print()
