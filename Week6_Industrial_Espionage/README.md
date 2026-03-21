# Week 6 – Industrial Espionage in Cyberspace

CS 475 · Introduction to Computer Security · Mária Nyolcas

## Files

| File | Purpose |
|------|---------|
| `osint_recon.py` | Structured passive OSINT profile of fictional target InnovateTech Solutions |
| `espionage_lifecycle.py` | Five-phase AeroTech GmbH case study with ATT&CK mappings and discussion answers |
| `build_docx.py` | Generates `report_week6.docx` via python-docx |
| `report_week6.tex` | LaTeX source for the final 4-page PDF report |
| `report_week6.docx` | Pre-built Word version |

## Lab target

InnovateTech Solutions (`innovatech-solutions.io`) — fictional aerospace / advanced
materials R&D company. All data is invented for this exercise.

## Running the scripts

```bash
python3 osint_recon.py          # prints OSINT findings and attack surface summary
python3 espionage_lifecycle.py  # prints 5-phase lifecycle + discussion answers
python3 build_docx.py           # regenerates report_week6.docx
```

## Building the PDF

Open `report_week6.tex` in VS Code with LaTeX Workshop (pdflatex recipe).

## Connections to other weeks

- Week 2 (Bell-LaPadula / least privilege): least privilege directly limits lateral movement in Phase 3.
- Week 4 (Nmap / CVE analysis): the same CVE classes used in vulnerability assessment appear as espionage entry points (AnyConnect, PDF reader).
- Week 7 (next): OSINT profile feeds into security domains and technologies countermeasure analysis.
