def format_transition_row(row):
    if row is None:
        return "No guidance found for this transition."
    out = f"**Transition:** {row['Previous_Cargo']} → {row['Next_Cargo']}\n"
    out += f"- **HM50 Code:** {row['HM50_Code']} ({row['HM50_Code_Description']})\n"
    out += f"- **HM50 Notes:** {row['HM50_Notes']}\n"
    out += f"- **Memo Methods:** {row['Memo_Methods']}\n"
    out += f"- **Memo Results:** {row['Memo_Results']}\n"
    out += f"- **Lessons Learned:** {row['Memo_Lessons']}\n"
    if row['Sensitive_Cargo_Flag']:
        out += f"- **Sensitive Cargo:** Yes\n"
    return out
