
# utils.py
def _line(label, value):
    v = ("" if value is None else str(value)).strip()
    if v and v.upper() != "N/A":
        return f"- **{label}:** {v}\n"
    return ""

def format_transition_row(row):
    if row is None:
        return "No guidance found for this transition."
    out  = f"**Transition:** {row['Previous_Cargo']} → {row['Next_Cargo']}\n"
    out += _line("HM50 Code", f"{row.get('HM50_Code','')} ({row.get('HM50_Code_Description','')})")
    out += _line("HM50 Notes", row.get('HM50_Notes', ''))
    out += _line("Memo Methods", row.get('Memo_Methods', ''))
    out += _line("Memo Results", row.get('Memo_Results', ''))
    out += _line("Lessons Learned", row.get('Memo_Lessons', ''))
    if bool(row.get('Sensitive_Cargo_Flag', False)):
        out += "- **Sensitive Cargo:** Yes\n"
    out += _line("Source Memo ID(s)", row.get('Source_Memo_IDs', ''))
    return out
