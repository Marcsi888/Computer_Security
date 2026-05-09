# Week 12-13 - Part A: Blockchain and DApp Concepts
# CS 475 Introduction to Computer Security

from dataclasses import dataclass


@dataclass
class Concept:
    topic: str
    plain_explanation: str
    security_problem_solved: str
    what_it_does_not_solve: str


@dataclass
class ComparisonRow:
    criterion: str
    blockchain: str
    dapp: str


CONCEPTS: list[Concept] = [
    Concept(
        topic="Blockchain",
        plain_explanation=(
            "An append-only ledger where each block contains a hash of the previous block, "
            "so history tampering is detectable."
        ),
        security_problem_solved=(
            "Reduces single-point trust by allowing many participants to verify the same state "
            "with a shared consensus rule."
        ),
        what_it_does_not_solve=(
            "Does not guarantee input truth (garbage in, garbage forever) and does not stop "
            "application logic bugs in smart contracts."
        ),
    ),
    Concept(
        topic="Consensus",
        plain_explanation=(
            "A rule for deciding which version of the ledger is valid when nodes disagree."
        ),
        security_problem_solved=(
            "Prevents easy double-spend and inconsistent state by making attackers pay a large "
            "resource cost (hashpower, stake, or validator reputation)."
        ),
        what_it_does_not_solve=(
            "Cannot fully prevent majority attacks when one entity controls enough validating power."
        ),
    ),
    Concept(
        topic="DApp",
        plain_explanation=(
            "An application where core state transition logic executes in smart contracts on-chain, "
            "while user interfaces usually remain off-chain."
        ),
        security_problem_solved=(
            "Limits operator-side tampering with core business logic because contract rules are public "
            "and state updates are auditable."
        ),
        what_it_does_not_solve=(
            "Front-end phishing, wallet theft, and malicious dependency supply-chain attacks still apply."
        ),
    ),
]

BLOCKCHAIN_VS_DAPP: list[ComparisonRow] = [
    ComparisonRow(
        criterion="What it is",
        blockchain="Data structure plus consensus rule",
        dapp="Application architecture using blockchain as trust backend",
    ),
    ComparisonRow(
        criterion="Main security primitive",
        blockchain="Hash chaining plus distributed validation",
        dapp="Deterministic contract execution plus public state auditability",
    ),
    ComparisonRow(
        criterion="Typical attack focus",
        blockchain="Consensus capture, network partition, key theft",
        dapp="Smart contract bugs, oracle manipulation, wallet phishing",
    ),
    ComparisonRow(
        criterion="Upgrade difficulty",
        blockchain="Protocol hard forks or validator governance",
        dapp="Proxy patterns, migration contracts, governance vote",
    ),
]

UNIQUE_SMART_CONTRACT_RISKS = [
    "Reentrancy",
    "Integer/precision logic errors in token math",
    "Oracle manipulation and price feed dependency",
]

HARD_TO_FIX_NON_UNIQUE_RISKS = [
    "Access-control misconfiguration",
    "Input validation bugs",
    "Denial-of-service by resource exhaustion",
]


def print_concepts() -> None:
    print("Part A-1: Core concepts")
    for c in CONCEPTS:
        print(f"\nTopic: {c.topic}")
        print(f"  Explanation : {c.plain_explanation}")
        print(f"  Solves      : {c.security_problem_solved}")
        print(f"  Does not    : {c.what_it_does_not_solve}")


def print_comparison() -> None:
    print("\nPart A-2: Blockchain vs DApp")
    print(f"  {'criterion':<28} {'blockchain':<42} dapp")
    print(f"  {'-'*27} {'-'*41} {'-'*40}")
    for r in BLOCKCHAIN_VS_DAPP:
        print(f"  {r.criterion:<28} {r.blockchain:<42} {r.dapp}")


def print_risks() -> None:
    print("\nPart A-3: Smart-contract risk classes")
    print("  Unique / amplified in smart contracts:")
    for item in UNIQUE_SMART_CONTRACT_RISKS:
        print(f"    - {item}")

    print("  Not unique, but harder to fix after deployment:")
    for item in HARD_TO_FIX_NON_UNIQUE_RISKS:
        print(f"    - {item}")


if __name__ == "__main__":
    print("week 12-13 - part a theory")
    print_concepts()
    print_comparison()
    print_risks()
