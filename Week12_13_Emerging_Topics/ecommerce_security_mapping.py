# Week 12-13 - Lesson 2: E-commerce Security Mapping
# CS 475 Introduction to Computer Security

from dataclasses import dataclass


@dataclass
class EcommerceRisk:
    risk: str
    attack_surface: str
    impact: str
    practical_control: str
    syllabus_link: str


RISKS: list[EcommerceRisk] = [
    EcommerceRisk(
        risk="Card-not-present fraud",
        attack_surface="Checkout API + weak transaction risk scoring",
        impact="Chargebacks, direct financial loss, account takeover disputes",
        practical_control="3-D Secure 2, velocity checks, device fingerprinting",
        syllabus_link="Authentication protocols + anomaly detection",
    ),
    EcommerceRisk(
        risk="Credential stuffing",
        attack_surface="Login endpoint with reused credentials from prior breaches",
        impact="Account takeover, gift-card abuse, fraudulent orders",
        practical_control="MFA, adaptive rate-limits, breached-password blocking",
        syllabus_link="Threats, attacks, and defenses",
    ),
    EcommerceRisk(
        risk="Session hijacking",
        attack_surface="Weak cookie flags or token leakage",
        impact="Unauthorized purchases and profile changes",
        practical_control="Secure/HttpOnly/SameSite cookies, short token lifetime",
        syllabus_link="Network and web security",
    ),
    EcommerceRisk(
        risk="Supply-chain compromise",
        attack_surface="Third-party JS in checkout pages",
        impact="Skimming payment data (Magecart style)",
        practical_control="Subresource Integrity, CSP, dependency governance",
        syllabus_link="Malware + web application security",
    ),
]


def print_matrix() -> None:
    print("Lesson 2: E-commerce risk-to-control matrix")
    print(f"  {'risk':<24} {'impact':<40} control")
    print(f"  {'-'*23} {'-'*39} {'-'*40}")
    for r in RISKS:
        print(f"  {r.risk:<24} {r.impact:<40} {r.practical_control}")


if __name__ == "__main__":
    print_matrix()
