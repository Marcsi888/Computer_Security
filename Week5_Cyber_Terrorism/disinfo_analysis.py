# Disinformation Analysis – Operation Secondary Infektion
# CS 475 Week 5 – Mária Nyolcas
#
# Exercise 2: structured analysis of a documented information operations
# campaign. Primary source: Stanford Internet Observatory / EU DisinfoLab
# joint investigation (2020) at https://secondaryinfektion.org
#
# The script encodes the campaign anatomy, the OSINT tool findings, and
# a reusable red-flag indicator table that could be applied to other cases.

from dataclasses import dataclass


@dataclass
class CampaignFact:
    attribute: str
    value: str


@dataclass
class Indicator:
    number: int
    name: str
    description: str
    how_to_check: str
    confidence: str   # High / Medium / Low


@dataclass
class OsintFinding:
    tool: str
    why_chosen: str
    query: str
    output_summary: str
    what_it_shows: str
    limitations: str


CAMPAIGN = {
    "name": "Operation Secondary Infektion",
    "source": "Stanford Internet Observatory + EU DisinfoLab (2020), https://secondaryinfektion.org",
    "active_period": "2014 – 2020 (at least)",
    "platforms_affected": "300+ across Reddit, Facebook, Twitter, Medium, Blogspot, "
                          "Wikipedia, fringe forums, and mainstream European news comments",
    "languages": "English, German, French, Spanish, Ukrainian, Russian, Arabic",
    "fabricated_content": [
        "Forged documents attributed to real EU and NATO officials",
        "Fake news articles mimicking established outlet formatting",
        "Fabricated quotes placed in the mouths of named politicians",
        "Manipulated images with false captions",
    ],
    "laundering_platforms": [
        "Newly registered domains impersonating legitimate news outlets",
        "Reddit accounts with low karma used as 'primary sources'",
        "Facebook pages with purchased followers for credibility",
    ],
    "amplification": [
        "Coordinated posting of identical content across multiple accounts within minutes",
        "Cross-referencing between fake sites to create illusion of independent corroboration",
        "Seeding on fringe forums, then citing those posts as 'community concern'",
    ],
    "target_audiences": [
        "Ukrainian population (anti-EU and anti-NATO narratives)",
        "German and French publics (distrust of government institutions)",
        "English-speaking audiences (NATO cohesion narratives)",
    ],
    "desired_cognitive_effects": [
        "Distrust of Western governments and NATO institutions",
        "Amplification of existing political divisions",
        "Undermining of specific policy decisions (e.g., sanctions regimes)",
    ],
    "exposure_indicators": [
        "Repeated document templates with shared metadata signatures",
        "Consistent linguistic fingerprints across supposedly unrelated accounts",
        "Infrastructure clustering: multiple fake sites sharing hosting IPs",
        "Account creation timestamps clustered around specific events",
        "Identical image files posted by accounts claiming independent discovery",
    ],
}

INDICATORS: list[Indicator] = [
    Indicator(
        number=1,
        name="Coordinated posting timing",
        description=(
            "Multiple accounts post identical or near-identical content within "
            "a very short window (minutes), suggesting automated or coordinated "
            "rather than organic sharing."
        ),
        how_to_check=(
            "Search the claim across platforms and sort by time. "
            "Bot-detection tools like Botometer can flag high-automation accounts."
        ),
        confidence="High",
    ),
    Indicator(
        number=2,
        name="Domain registration anomaly",
        description=(
            "The publishing domain was registered close to (or after) the event "
            "it claims to report on, or it mimics a legitimate outlet name with "
            "a slight variation (typosquatting)."
        ),
        how_to_check=(
            "WHOIS / DNS lookup (lookup.icann.org). Compare registration date "
            "with the date of the first article. Check for look-alike domain names."
        ),
        confidence="High",
    ),
    Indicator(
        number=3,
        name="Document metadata mismatch",
        description=(
            "Forged official documents often carry metadata (author field, "
            "creation software, edit timestamps) inconsistent with the claimed "
            "institution or date of origin."
        ),
        how_to_check=(
            "Download the document and inspect metadata with exiftool or "
            "a PDF properties viewer. Compare software version and locale settings "
            "with the purported issuing organisation."
        ),
        confidence="High",
    ),
    Indicator(
        number=4,
        name="Cross-platform self-citation loop",
        description=(
            "Content appears first on a low-credibility source, which is then "
            "cited by a second source as 'independent confirmation', creating a "
            "circular chain of apparent corroboration with no external anchor."
        ),
        how_to_check=(
            "Trace the content back to its earliest appearance using Google "
            "reverse image search or archive.org. Check whether all citing "
            "sources trace back to a single origin."
        ),
        confidence="Medium",
    ),
    Indicator(
        number=5,
        name="Linguistic inconsistency",
        description=(
            "Text attributed to a native speaker of one language contains "
            "idiom errors, unusual phrasing, or syntactic structures characteristic "
            "of machine translation from another language."
        ),
        how_to_check=(
            "Read the text carefully for unnatural phrasing. Tools like "
            "Google Translate (back-translation) or native speaker review can "
            "surface translation artefacts. Consistent errors across multiple "
            "accounts strengthen the signal."
        ),
        confidence="Medium",
    ),
    Indicator(
        number=6,
        name="Infrastructure clustering",
        description=(
            "Multiple seemingly unrelated fake news domains resolve to the same "
            "hosting IP addresses or share SSL certificate issuer patterns, "
            "suggesting they were set up by the same actor."
        ),
        how_to_check=(
            "DNS A-record and reverse-IP lookup (Shodan, SecurityTrails, or "
            "Censys). Compare hosting providers and certificate transparency logs "
            "across suspicious domains."
        ),
        confidence="High",
    ),
]

OSINT_FINDING = OsintFinding(
    tool="WHOIS / DNS lookup (lookup.icann.org)",
    why_chosen=(
        "WHOIS is the simplest, most universally available OSINT tool for "
        "infrastructure analysis. Since the Secondary Infektion report explicitly "
        "names fake domains, a direct registration lookup is the most "
        "targeted and reproducible check I could run."
    ),
    query=(
        "WHOIS lookup on a domain cited in the Secondary Infektion report "
        "as a fake news outlet (domain name withheld here to avoid amplification). "
        "Looked up via lookup.icann.org."
    ),
    output_summary=(
        "Registration date: approximately two weeks before the first article "
        "attributed to that outlet appeared. Registrant: privacy-shielded through "
        "a domain reseller in a jurisdiction with no public WHOIS requirements. "
        "Name server: shared with two other domains identified in the same report. "
        "Hosting IP: resolves to a VPS provider commonly used for anonymous hosting."
    ),
    what_it_shows=(
        "The domain was purpose-built for this operation rather than being a "
        "pre-existing outlet. The shared name server is the single most useful "
        "finding: it links three apparently independent 'news sites' to the same "
        "underlying infrastructure, consistent with a single actor managing them."
    ),
    limitations=(
        "WHOIS data alone cannot prove intent or attribution to a specific actor. "
        "Privacy shielding is legal and used by many legitimate publishers. The "
        "shared name server is suggestive but could be coincidental (e.g., same "
        "hosting reseller used independently). Full attribution would require "
        "corroborating network traffic analysis, malware forensics, or HUMINT."
    ),
)



def print_campaign() -> None:
    c = CAMPAIGN
    print(f"\ncase: {c['name']}")
    print(f"  source        : {c['source']}")
    print(f"  active period : {c['active_period']}")
    print(f"  languages     : {c['languages']}")
    print(f"  fabricated content:")
    for item in c["fabricated_content"]:
        print(f"    - {item}")
    print(f"  laundering:")
    for item in c["laundering_platforms"]:
        print(f"    - {item}")
    print(f"  amplification:")
    for item in c["amplification"]:
        print(f"    - {item}")
    print(f"  targets:")
    for item in c["target_audiences"]:
        print(f"    - {item}")
    print(f"  exposure indicators:")
    for item in c["exposure_indicators"]:
        print(f"    - {item}")


def print_indicators() -> None:
    print(f"\nred-flag indicators")
    print(f"  {'#':<3} {'indicator':<35} confidence")
    print(f"  {'-'*2} {'-'*34} {'-'*10}")
    for ind in INDICATORS:
        print(f"  {ind.number:<3} {ind.name:<35} {ind.confidence}")


def print_osint() -> None:
    f = OSINT_FINDING
    print(f"\nOSINT tool: {f.tool}")
    print(f"  query     : {f.query[:80]}")
    print(f"  output    : {f.output_summary[:80]}")
    print(f"  conclusion: {f.what_it_shows[:80]}")
    print(f"  limits    : {f.limitations[:80]}")


if __name__ == "__main__":
    print("disinformation analysis – week 5 lab")

    print_campaign()
    print_osint()
    print_indicators()
