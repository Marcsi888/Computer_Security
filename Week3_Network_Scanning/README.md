# Week 3 – Network Scanning, Attack Classification & Vulnerability Analysis

**CS 475: Introduction to Computer Security**
Mária Nyolcas | March 2026

---

## Overview

This folder contains the lab code, data, and report for Week 3 of the
continuous project.  The practical work focuses on:

- Host discovery and port scanning against an intentionally vulnerable VM
- Attack classification using MITRE ATT&CK
- Vulnerability assessment with CVE/CVSS data

All exercises were performed in an **isolated Hyper-V host-only network**
(`192.168.56.0/24`) with no internet exposure.  Target: **Metasploitable 2**
(`192.168.56.101`).  Attacker: **Kali Linux 2024.3** (`192.168.56.100`).

---

## Files

| File | Purpose |
|------|---------|
| `scanner.py` | Nmap wrapper: host discovery, SYN scan, version scan, result parsing |
| `attack_classification.py` | MITRE ATT&CK mapping for three attack scenarios on discovered services |
| `vuln_assessment.py` | Structured CVE/CVSS findings from the OpenVAS scan; remediation data |
| `report_week3.tex` | Full 4-page LaTeX report (compile to PDF with `pdflatex`) |
| `screenshots/` | Evidence screenshots from the lab exercises |

---

## How to Run the Scripts

> These scripts are designed to be read alongside the report. `scanner.py`
> requires Nmap installed and root/sudo privileges. The other two scripts
> have no external dependencies beyond Python 3.10+.

```bash
# Port scanner (requires nmap and root, run inside the lab VM only)
sudo python3 scanner.py

# Attack classification report (no dependencies)
python3 attack_classification.py

# Vulnerability assessment summary (no dependencies)
python3 vuln_assessment.py
```

---

## Compile the Report to PDF

```bash
pdflatex report_week3.tex
pdflatex report_week3.tex   # run twice for correct page references
```

Requires a standard TeX Live / MiKTeX installation with the packages:
`geometry`, `booktabs`, `tabularx`, `parskip`, `titlesec`,
`hyperref`, `enumitem`, `microtype`, `fancyhdr`.

---

## Screenshots Index

| File | Content |
|------|---------|
| `screenshots/host_discovery.png` | `nmap -sn` ping sweep output showing live hosts |
| `screenshots/syn_scan.png` | SYN scan results (12 open ports) |
| `screenshots/version_scan.png` | Version scan with service banners |
| `screenshots/openvas_summary.png` | OpenVAS findings dashboard |
| `screenshots/openvas_top3.png` | Detail view of top 3 CVSS findings |

---

## Connection to Previous Work

The Week 2 Bell-LaPadula and Biba simulations modelled what *should* be
enforced.  This week's scan results demonstrate what *actually runs* on a
real (albeit intentionally vulnerable) system and how easily those formal
guarantees are undermined by unpatched software and misconfigured services.
