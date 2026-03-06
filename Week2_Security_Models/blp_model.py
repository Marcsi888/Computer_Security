# Bell-LaPadula model simulation
# CS 475 Week 2 – Mária Nyolcas
#
# BLP is about confidentiality. The two main rules are:
#   no read up   – you can't read a file classified above your clearance
#   no write down – you can't write to a file classified below your clearance
# This stops secret data leaking downward.

# security levels as numbers so we can compare them easily
LEVELS = {
    "Unclassified": 0,
    "Confidential": 1,
    "Secret": 2,
    "TopSecret": 3,
}

# reverse lookup so we can print names from numbers
LEVEL_NAMES = {v: k for k, v in LEVELS.items()}

# subjects = users/processes and their clearance level
SUBJECTS = {
    "Alice": LEVELS["TopSecret"],    # senior analyst
    "Bob":   LEVELS["Secret"],
    "Carol": LEVELS["Confidential"], # contractor
    "Dave":  LEVELS["Unclassified"], # external visitor
}

# objects = files and their classification
OBJECTS = {
    "TacticalPlan.pdf":   LEVELS["TopSecret"],
    "IntelReport.docx":   LEVELS["Secret"],
    "BudgetSummary.xlsx": LEVELS["Confidential"],
    "PublicBrochure.pdf": LEVELS["Unclassified"],
}


def can_read(subject, obj):
    # no read up: clearance must be >= classification
    s = SUBJECTS[subject]
    o = OBJECTS[obj]
    if s >= o:
        return True, f"ALLOW | READ  | {subject} ({LEVEL_NAMES[s]}) reads '{obj}' ({LEVEL_NAMES[o]})"
    else:
        return False, f"DENY  | READ  | {subject} ({LEVEL_NAMES[s]}) cannot read '{obj}' ({LEVEL_NAMES[o]}) -- no read up"


def can_write(subject, obj):
    # no write down: clearance must be <= classification
    s = SUBJECTS[subject]
    o = OBJECTS[obj]
    if s <= o:
        return True, f"ALLOW | WRITE | {subject} ({LEVEL_NAMES[s]}) writes to '{obj}' ({LEVEL_NAMES[o]})"
    else:
        return False, f"DENY  | WRITE | {subject} ({LEVEL_NAMES[s]}) cannot write to '{obj}' ({LEVEL_NAMES[o]}) -- no write down"


def check(subject, obj, op):
    if op == "read":
        _, msg = can_read(subject, obj)
    else:
        _, msg = can_write(subject, obj)
    print("  " + msg)


if __name__ == "__main__":
    print("Bell-LaPadula Model – CS 475 Week 2")
    print("=" * 60)

    print("\nLevels:", " | ".join(f"{k}={v}" for k, v in LEVELS.items()))
    print("Subjects:", ", ".join(f"{k} ({LEVEL_NAMES[v]})" for k, v in SUBJECTS.items()))
    print("Objects:",  ", ".join(f"{k} ({LEVEL_NAMES[v]})" for k, v in OBJECTS.items()))

    print("\n--- test cases ---\n")

    # same level read – should be fine
    print("1. Bob reads IntelReport (both Secret):")
    check("Bob", "IntelReport.docx", "read")

    # higher clearance reading down -> allowed
    print("2. Alice (TopSecret) reads BudgetSummary (Confidential):")
    check("Alice", "BudgetSummary.xlsx", "read")

    # no read up violation
    print("3. Dave (Unclassified) tries to read IntelReport (Secret):")
    check("Dave", "IntelReport.docx", "read")

    # another no read up
    print("4. Carol (Confidential) tries to read TacticalPlan (TopSecret):")
    check("Carol", "TacticalPlan.pdf", "read")

    # write to same level -> fine
    print("5. Bob writes to IntelReport (both Secret):")
    check("Bob", "IntelReport.docx", "write")

    # write up -> allowed under BLP
    print("6. Carol (Confidential) writes to IntelReport (Secret):")
    check("Carol", "IntelReport.docx", "write")

    # no write down violation -> Alice can't write down to Confidential
    print("7. Alice (TopSecret) tries to write to BudgetSummary (Confidential):")
    check("Alice", "BudgetSummary.xlsx", "write")

    # no write down -> Bob writing to public doc
    print("8. Bob (Secret) tries to write to PublicBrochure (Unclassified):")
    check("Bob", "PublicBrochure.pdf", "write")

    # lowest level user reads public file -> should work
    print("9. Dave reads PublicBrochure:")
    check("Dave", "PublicBrochure.pdf", "read")

    # Dave writing to public -> same level so allowed
    print("10. Dave writes to PublicBrochure:")
    check("Dave", "PublicBrochure.pdf", "write")

    print("\n" + "=" * 60)
    print("Done.")
