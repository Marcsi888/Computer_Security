# Week 5 – Cyber Terrorism and Information Warfare

CS 475: Introduction to Computer Security | Mária Nyolcas

---

## Contents

| File | Purpose |
|------|---------|
| `report_week5.tex` | 4-page LaTeX report (compile with `pdflatex`) |
| `lab5_journal.txt` | Lab journal covering all three exercises |
| `threat_actor_mapping.py` | Exercise 1: Sandworm vs Lazarus ATT&CK mapping |
| `disinfo_analysis.py` | Exercise 2: Operation Secondary Infektion anatomy + OSINT |
| `attack_scenario.py` | Exercise 3: Hospital attack chain + countermeasures |

---

## Running the scripts

```bash
python3 threat_actor_mapping.py
python3 disinfo_analysis.py
python3 attack_scenario.py
```

No external dependencies required.

---

## Exercises covered

**Exercise 1 – Threat Actor Mapping**
Sandworm Team (APT44, Russian GRU) – 5 techniques mapped.
Lazarus Group (APT38, DPRK RGB) – 3 techniques compared.
Attribution challenge discussed via TTP overlap analysis.

**Exercise 2 – Disinformation Analysis**
Case: Operation Secondary Infektion (Stanford IO / EU DisinfoLab, 2020).
OSINT tool: WHOIS/DNS lookup on a cited domain.
Output: 6-indicator red-flag table.

**Exercise 3 – Attack Scenario**
Target: hospital / EMS network.
Actor: Iron Caduceus (fictional nation-state APT).
7-step Lockheed Martin Kill Chain with countermeasures and weakest-link analysis.

---

## References

Primary sources cited in the report:
- MITRE ATT&CK Enterprise Matrix v15: https://attack.mitre.org
- Operation Secondary Infektion: https://secondaryinfektion.org
- CISA NotPetya Advisory AA22-057A: https://www.cisa.gov
- NATO CCDCOE Tallinn Manual 2.0: https://ccdcoe.org
- Lockheed Martin Cyber Kill Chain: https://www.lockheedmartin.com/cyber-kill-chain
