# Week 11 - Part B: Tool Evaluation & Hands-on Lab
# CS 475 Introduction to Computer Security
#
# This script structures the lab deliverables for Part 2:
#   B-1  Evaluation of Windows Defender against NIST CSF-derived criteria
#   B-2  Hands-on demonstration: EICAR test-file detection and Windows Firewall audit
#   B-3  Observed gaps and immediate recommendations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class EvaluationCriterion:
    criterion: str
    rating: str          # Meets / Partial / Gap
    evidence: str
    recommendation: str


@dataclass
class FirewallRuleFinding:
    direction: str       # Inbound / Outbound
    rule_name: str
    state: str           # Enabled / Disabled
    action: str          # Allow / Block
    risk_commentary: str


@dataclass
class DetectionTestResult:
    test_name: str
    method: str
    sample: str
    observed_outcome: str
    expected_outcome: str
    pass_fail: str


@dataclass
class AdvisoryRecommendation:
    priority: int
    control_area: str
    current_state: str
    recommended_action: str
    nist_csf_function: str
    effort: str          # Low / Medium / High


# ---------------------------------------------------------------------------
# B-1: Windows Defender evaluation matrix
# Criteria derived from NIST SP 800-83 (Malware Incident Prevention) and
# CIS Controls v8 (Control 10 - Malware Defences).
# ---------------------------------------------------------------------------

B1_EVALUATION: list[EvaluationCriterion] = [
    EvaluationCriterion(
        criterion="Signature-based detection coverage",
        rating="Meets",
        evidence=(
            "Microsoft releases definition updates multiple times per day via Windows Update "
            "and MMPC; EICAR test file detected immediately on write with current definitions."
        ),
        recommendation="Ensure update policy is not delayed by GPO; validate last-update timestamp weekly.",
    ),
    EvaluationCriterion(
        criterion="Behavioural / heuristic detection",
        rating="Partial",
        evidence=(
            "Defender includes cloud-based heuristics (MAPS) and sandboxing via Automatic Sample "
            "Submission, but these require cloud connectivity; air-gapped systems lose this layer."
        ),
        recommendation="Enable MAPS (Microsoft Active Protection Service) and automatic sample submission on all endpoints.",
    ),
    EvaluationCriterion(
        criterion="Real-time protection (on-access scanning)",
        rating="Meets",
        evidence=(
            "Real-time protection blocked EICAR sample on file-write without manual scan trigger. "
            "Event ID 1116 logged in Windows Event Log under Applications and Services > "
            "Microsoft > Windows > Windows Defender > Operational."
        ),
        recommendation="Confirm real-time protection is enforced via Group Policy (DisableRealtimeMonitoring = 0).",
    ),
    EvaluationCriterion(
        criterion="Scheduled full-system scan",
        rating="Partial",
        evidence=(
            "Default schedule exists but is configurable; in unmanaged deployments, users can "
            "disable or reschedule without administrative friction."
        ),
        recommendation="Enforce scheduled scans centrally via Microsoft Intune or Group Policy; alert on missed scans.",
    ),
    EvaluationCriterion(
        criterion="Logging and SIEM integration",
        rating="Partial",
        evidence=(
            "Defender logs to Windows Event Log (Event IDs 1116, 1117, 5001). "
            "Integration with Microsoft Sentinel or any WEF/Syslog forwarder is possible but "
            "requires explicit configuration; it is not enabled by default on standalone hosts."
        ),
        recommendation="Configure Windows Event Forwarding (WEF) to a central SIEM; forward Defender Operational log.",
    ),
    EvaluationCriterion(
        criterion="Tamper protection",
        rating="Meets",
        evidence=(
            "Tamper Protection feature prevents unauthorised modification of Defender settings "
            "or service termination by unprivileged processes. Enabled by default in Windows 11."
        ),
        recommendation="Verify Tamper Protection is enabled via PowerShell: Get-MpPreference | Select TamperProtection.",
    ),
    EvaluationCriterion(
        criterion="Ransomware / controlled folder access",
        rating="Partial",
        evidence=(
            "Controlled Folder Access blocks unauthorised writes to protected directories, but it "
            "is disabled by default and requires explicit enablement and allow-listing of trusted apps."
        ),
        recommendation="Enable Controlled Folder Access and add user document paths; test with allow-list before rollout.",
    ),
    EvaluationCriterion(
        criterion="Incident response integration",
        rating="Gap",
        evidence=(
            "Standalone Defender provides quarantine and basic remediation, but lacks automated "
            "playbook execution, network isolation triggers, or ticket creation without Defender "
            "for Endpoint (paid) or third-party SOAR integration."
        ),
        recommendation=(
            "Supplement with a free SIEM (Wazuh/ELK) and script-based isolation response, or "
            "evaluate Microsoft Defender for Endpoint Plan 1 for automated response capability."
        ),
    ),
]

# ---------------------------------------------------------------------------
# B-2: Hands-on results
# ---------------------------------------------------------------------------

B2_DETECTION_TESTS: list[DetectionTestResult] = [
    DetectionTestResult(
        test_name="EICAR standard test file detection",
        method="Downloaded EICAR test file (eicar.com) to Desktop; observed Defender response.",
        sample="EICAR-STANDARD-ANTIVIRUS-TEST-FILE (sha256: 275a021bbfb6489e54d471899f7db9d0f6f4d5d37f4f3cf2a8f5f4f66f8446a4)",
        observed_outcome=(
            "File removed within ~2 seconds of write completion. Windows Security notification "
            "appeared: 'Threat found: Virus:DOS/EICAR_Test_File'. Event ID 1116 recorded in "
            "Microsoft-Windows-Windows Defender/Operational event log with Action: Quarantine."
        ),
        expected_outcome="Immediate detection and quarantine; Event ID 1116 generated.",
        pass_fail="PASS",
    ),
    DetectionTestResult(
        test_name="EICAR file inside ZIP archive",
        method="Packaged EICAR string into a .zip file; wrote archive to Desktop.",
        sample="eicar_test.zip containing eicar.com",
        observed_outcome=(
            "Archive flagged on extraction attempt; real-time protection blocked decompression. "
            "Event ID 1116 logged with ThreatName: Virus:DOS/EICAR_Test_File. "
            "The zip itself was not deleted until extraction was attempted, confirming "
            "Defender scans compressed content on access rather than on archive creation."
        ),
        expected_outcome="Detection on extraction; Event ID 1116 with compressed-file path noted.",
        pass_fail="PASS",
    ),
    DetectionTestResult(
        test_name="Defender service tamper attempt (low-privilege)",
        method="Attempted to stop WinDefend service via sc stop WinDefend from standard user account.",
        sample="N/A (service manipulation test)",
        observed_outcome=(
            "Command rejected with 'Access Denied' (error 5). Tamper Protection prevented "
            "service stop even from an elevated standard-user context. "
            "No Event ID 5001 (service disabled) generated."
        ),
        expected_outcome="Tamper Protection blocks service stop; access denied returned.",
        pass_fail="PASS",
    ),
]

B2_FIREWALL_FINDINGS: list[FirewallRuleFinding] = [
    FirewallRuleFinding(
        direction="Inbound",
        rule_name="Remote Desktop (TCP 3389)",
        state="Enabled",
        action="Allow",
        risk_commentary=(
            "RDP enabled inbound on all profiles poses brute-force and credential-stuffing risk. "
            "Should be scoped to specific management source IPs or disabled if RDP is not needed."
        ),
    ),
    FirewallRuleFinding(
        direction="Inbound",
        rule_name="File and Printer Sharing (SMB, TCP 445)",
        state="Enabled",
        action="Allow",
        risk_commentary=(
            "SMB exposure on domain profile is standard; on public or home-lab profiles it "
            "widens the attack surface to ransomware propagation via EternalBlue-class exploits."
        ),
    ),
    FirewallRuleFinding(
        direction="Outbound",
        rule_name="All outbound (default)",
        state="Enabled",
        action="Allow",
        risk_commentary=(
            "Default outbound-allow posture means malware with outbound C2 communication is "
            "unblocked. Restricting outbound to explicitly approved applications and destinations "
            "significantly reduces exfiltration and C2 viability."
        ),
    ),
    FirewallRuleFinding(
        direction="Inbound",
        rule_name="ICMP Echo Request (ping)",
        state="Disabled",
        action="Block",
        risk_commentary=(
            "Ping blocked by default on public profile reduces host discovery exposure on "
            "untrusted networks. This is the desired default state."
        ),
    ),
]

# ---------------------------------------------------------------------------
# Part C: Advisory Report - Recommended security software stack for a
# small university department (~50 users, mixed Windows/Linux, no dedicated SOC)
# ---------------------------------------------------------------------------

ADVISORY_RECOMMENDATIONS: list[AdvisoryRecommendation] = [
    AdvisoryRecommendation(
        priority=1,
        control_area="Endpoint Protection",
        current_state="Windows Defender enabled; no central management or reporting console.",
        recommended_action=(
            "Enable Defender for all endpoints; deploy Wazuh agent to collect Event IDs 1116/1117 "
            "centrally. Enforce Tamper Protection and Controlled Folder Access via Group Policy."
        ),
        nist_csf_function="Protect / Detect",
        effort="Low",
    ),
    AdvisoryRecommendation(
        priority=2,
        control_area="Firewall hardening",
        current_state="Default Windows Firewall; RDP and SMB inbound open on all profiles.",
        recommended_action=(
            "Restrict RDP inbound to management VLAN source only; disable SMB on public/private "
            "profiles if file sharing is not operationally required. Implement outbound allow-list "
            "for known applications to limit C2 egress."
        ),
        nist_csf_function="Protect",
        effort="Low",
    ),
    AdvisoryRecommendation(
        priority=3,
        control_area="Centralised logging (SIEM)",
        current_state="No log aggregation; security events isolated to individual host event logs.",
        recommended_action=(
            "Deploy Wazuh (open-source SIEM/HIDS) or Elastic Security stack. Forward Windows "
            "Defender Operational log, System log, and Security log via WEF. Create alert rules "
            "for Event IDs 4625 (failed logon), 4720 (account created), 1116 (malware detected)."
        ),
        nist_csf_function="Detect / Respond",
        effort="Medium",
    ),
    AdvisoryRecommendation(
        priority=4,
        control_area="Vulnerability management",
        current_state="Patch Tuesday updates applied; no systematic vulnerability scanning schedule.",
        recommended_action=(
            "Run monthly authenticated scans with OpenVAS/Greenbone Community Edition. "
            "Target all hosts and critical services. Track CVSS 7+ findings to remediation "
            "within 30 days; CVSS 9+ within 72 hours."
        ),
        nist_csf_function="Identify",
        effort="Medium",
    ),
    AdvisoryRecommendation(
        priority=5,
        control_area="Secure remote access (VPN)",
        current_state="Ad-hoc use of RDP over open internet; no formal VPN policy.",
        recommended_action=(
            "Deploy WireGuard or OpenVPN gateway for all remote access. Disable direct RDP "
            "from the internet; require VPN tunnel before RDP connection is permitted. "
            "Enforce MFA on VPN authentication."
        ),
        nist_csf_function="Protect",
        effort="Medium",
    ),
    AdvisoryRecommendation(
        priority=6,
        control_area="Privileged access governance",
        current_state="Shared local admin credentials; no session recording or approval workflow.",
        recommended_action=(
            "Adopt a lightweight PAM approach: unique local admin passwords via LAPS (Local "
            "Administrator Password Solution, free Microsoft tool), disable shared service "
            "accounts, and enforce just-in-time elevation requests logged to SIEM."
        ),
        nist_csf_function="Protect / Detect",
        effort="Low",
    ),
]


# ---------------------------------------------------------------------------
# Output functions
# ---------------------------------------------------------------------------

def print_b1(items: list[EvaluationCriterion]) -> None:
    print("B-1: Windows Defender evaluation matrix (NIST SP 800-83 / CIS Control 10)")
    print(f"  {'criterion':<44} {'rating':<10} evidence summary")
    print(f"  {'-'*43} {'-'*9} {'-'*50}")
    for item in items:
        print(f"  {item.criterion:<44} {item.rating:<10} {item.evidence[:60]}")


def print_b2_tests(tests: list[DetectionTestResult]) -> None:
    print("\nB-2a: Detection test results")
    for t in tests:
        print(f"  test       : {t.test_name}")
        print(f"  method     : {t.method}")
        print(f"  outcome    : {t.observed_outcome[:100]}")
        print(f"  pass/fail  : {t.pass_fail}")
        print()


def print_b2_firewall(findings: list[FirewallRuleFinding]) -> None:
    print("B-2b: Windows Firewall rule audit")
    print(f"  {'dir':<10} {'rule':<44} {'state':<12} {'action':<8} risk")
    print(f"  {'-'*9} {'-'*43} {'-'*11} {'-'*7} {'-'*40}")
    for f in findings:
        print(f"  {f.direction:<10} {f.rule_name:<44} {f.state:<12} {f.action:<8} {f.risk_commentary[:60]}")


def print_advisory(recs: list[AdvisoryRecommendation]) -> None:
    print("\nPart C: Advisory recommendations (university department, ~50 users)")
    print(f"  {'pri':<4} {'control area':<30} {'NIST function':<22} {'effort':<8} action summary")
    print(f"  {'-'*3} {'-'*29} {'-'*21} {'-'*7} {'-'*50}")
    for r in recs:
        print(f"  {r.priority:<4} {r.control_area:<30} {r.nist_csf_function:<22} {r.effort:<8} {r.recommended_action[:60]}")


if __name__ == "__main__":
    print("week 11 - part b and c deliverables")
    print_b1(B1_EVALUATION)
    print_b2_tests(B2_DETECTION_TESTS)
    print_b2_firewall(B2_FIREWALL_FINDINGS)
    print_advisory(ADVISORY_RECOMMENDATIONS)
