# Week 2 – Security Models and Policy Issues

## Files
- `blp_model.py` – Bell-LaPadula confidentiality model
- `biba_model.py` – Biba integrity model
- `screenshots/` – evidence for code execution, DAC experiment, and PoLP audit

## How to run
```bash
python3 blp_model.py
python3 biba_model.py
```

## Notes

These scripts were created for the Week 2 Computer Security lab assignment.
They simulate formal security model rules and print allowed/denied decisions with explanations.

## Screenshots index

| File | Task | Description |
|------|------|-------------|
| `screenshots/blp_output.png` | B.1 | Terminal output from running `blp_model.py` |
| `screenshots/biba_output.png` | B.1 | Terminal output from running `biba_model.py` |
| `screenshots/dac_setup.png` | B.2 | Creating test users and files (`useradd`, `chmod`, `chown`) |
| `screenshots/dac_denied.png` | B.2 | Cross-user access attempt denied by the kernel |
| `screenshots/dac_ls.png` | B.2 | `ls -l` showing ownership and permission bits |
| `screenshots/polp_id.png` | B.3 | Output of `id` and `groups` commands |
| `screenshots/polp_sudo.png` | B.3 | Output of `sudo -l` listing available sudo privileges |
