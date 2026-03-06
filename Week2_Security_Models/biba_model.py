# Biba integrity model simulation
# CS 475 Week 2 - Maria Nyolcas
#
# Biba is basically the mirror of BLP but for integrity instead of confidentiality.
# The idea is that low-trust data shouldn't contaminate high-trust data.
# Two rules:
#   no read down  -> a high-integrity process shouldn't read low-integrity data
#   no write up   -> a low-integrity source can't write to a high-integrity object

# integrity levels - higher means more trusted
LEVELS = {
    "Untrusted": 0,  # e.g. raw web input
    "Low":       1,
    "Medium":    2,
    "High":      3,  # e.g. verified audit records
}

LEVEL_NAMES = {v: k for k, v in LEVELS.items()}

# subjects and their integrity level
SUBJECTS = {
    "AuditSystem": LEVELS["High"],      # automated auditor, very trusted
    "DBAdmin":     LEVELS["Medium"],
    "AppProcess":  LEVELS["Low"],       # app server, limited trust
    "WebInput":    LEVELS["Untrusted"], # user submitted data
}

# objects and how much integrity they need to maintain
OBJECTS = {
    "AuditLog.db":        LEVELS["High"],
    "FinancialLedger.db": LEVELS["Medium"],
    "AppCache.json":      LEVELS["Low"],
    "UserSubmission.txt": LEVELS["Untrusted"],
}


def can_read(subject, obj):
    # no read down: subject integrity must be <= object integrity
    # (you can only read data that is at least as trusted as you are)
    s = SUBJECTS[subject]
    o = OBJECTS[obj]
    if s <= o:
        return True, f"ALLOW | READ  | {subject} ({LEVEL_NAMES[s]}) reads '{obj}' ({LEVEL_NAMES[o]})"
    else:
        return False, f"DENY  | READ  | {subject} ({LEVEL_NAMES[s]}) cannot read '{obj}' ({LEVEL_NAMES[o]}) -- no read down"


def can_write(subject, obj):
    # no write up: subject integrity must be >= object integrity
    # (you can only write to objects at or below your trust level)
    s = SUBJECTS[subject]
    o = OBJECTS[obj]
    if s >= o:
        return True, f"ALLOW | WRITE | {subject} ({LEVEL_NAMES[s]}) writes to '{obj}' ({LEVEL_NAMES[o]})"
    else:
        return False, f"DENY  | WRITE | {subject} ({LEVEL_NAMES[s]}) cannot write to '{obj}' ({LEVEL_NAMES[o]}) -- no write up"


def check(subject, obj, op):
    if op == "read":
        _, msg = can_read(subject, obj)
    else:
        _, msg = can_write(subject, obj)
    print("  " + msg)


if __name__ == "__main__":
    print("Biba Integrity Model - CS 475 Week 2")
    print("=" * 60)

    print("\nLevels:", " | ".join(f"{k}={v}" for k, v in LEVELS.items()))
    print("Subjects:", ", ".join(f"{k} ({LEVEL_NAMES[v]})" for k, v in SUBJECTS.items()))
    print("Objects:",  ", ".join(f"{k} ({LEVEL_NAMES[v]})" for k, v in OBJECTS.items()))

    print("\n--- test cases ---\n")

    # same level read -> fine
    print("1. DBAdmin reads FinancialLedger (both Medium):")
    check("DBAdmin", "FinancialLedger.db", "read")

    # high reads high -> fine
    print("2. AuditSystem reads AuditLog (both High):")
    check("AuditSystem", "AuditLog.db", "read")

    # no read down -> AuditSystem would be contaminated by untrusted data
    print("3. AuditSystem (High) tries to read UserSubmission (Untrusted):")
    check("AuditSystem", "UserSubmission.txt", "read")

    # no read down -> DBAdmin can't read low-integrity cache
    print("4. DBAdmin (Medium) tries to read AppCache (Low):")
    check("DBAdmin", "AppCache.json", "read")

    # write at same level -> fine
    print("5. DBAdmin writes to FinancialLedger (both Medium):")
    check("DBAdmin", "FinancialLedger.db", "write")

    # high writing down -> allowed
    print("6. AuditSystem (High) writes to AppCache (Low):")
    check("AuditSystem", "AppCache.json", "write")

    # no write up -> web input can't touch the financial ledger
    print("7. WebInput (Untrusted) tries to write to FinancialLedger (Medium):")
    check("WebInput", "FinancialLedger.db", "write")

    # no write up -> app process can't corrupt the audit log
    print("8. AppProcess (Low) tries to write to AuditLog (High):")
    check("AppProcess", "AuditLog.db", "write")

    # untrusted reading untrusted -> that's fine
    print("9. WebInput reads UserSubmission (both Untrusted):")
    check("WebInput", "UserSubmission.txt", "read")

    # even writing to Low from Untrusted is blocked
    print("10. WebInput (Untrusted) tries to write to AppCache (Low):")
    check("WebInput", "AppCache.json", "write")

    print("\n" + "=" * 60)
    print("Done.")
