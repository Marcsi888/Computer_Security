# Week 11 - Computer Security Software

CS 475 · Introduction to Computer Security  
Schiller International University 
Student: Maria Nyolcas | May 2026


## Overview

This folder contains the Week 11 portfolio deliverable covering **Computer Security Software** - the practical layer that operationalises encryption, access control, and threat detection knowledge from earlier modules.


## Files

| File | Purpose |
|---|---|
| `security_software_taxonomy.py` | Part A theory: eight security software families mapped to NIST CSF functions, deployment layers, and defence-in-depth architecture |
| `tool_evaluation.py` | Part B lab: Windows Defender evaluation matrix, three EICAR-based detection tests, Windows Firewall audit, and advisory recommendations |
| `report_week11.tex` | LaTeX source for the 4-page A4 written report |
| `build_docx.py` | Generates `report_week11.docx` using python-docx (run once) |


## Running the Python Scripts

```bash
# Part A - security software taxonomy output
python security_software_taxonomy.py

# Part B - tool evaluation, lab results, advisory report
python tool_evaluation.py
```

## Building the DOCX Report

```bash
pip install python-docx   # only needed once
python build_docx.py
# output: report_week11.docx
```

## Compiling the PDF Report

```bash
pdflatex report_week11.tex
pdflatex report_week11.tex   # run twice to resolve cross-references
```


## Lab Methodology

All hands-on exercises used **safe test artefacts only**:

- **EICAR standard test file** - the canonical antivirus validation signature; not executable malware
- **Windows Firewall rule review** - passive audit of default rule set on a personal development system
- No real malware, no third-party targets, no production systems



## Assessment Structure

| Part | Weight | Topic |
|---|---|---|
| Part A (Theory) | 1 | Security software landscape and NIST CSF mapping |
| Part B (Lab) | 2 | Windows Defender evaluation + hands-on tests |
| Part C (Report) | 1 | Advisory report for non-technical stakeholder |
