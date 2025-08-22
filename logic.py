
# logic.py
import re

def _norm(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower().strip()
    # simple normalization (remove extra spaces and punctuation)
    s = re.sub(r"[^a-z0-9+/& ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def find_transition(transitions, prev_cargo, next_cargo):
    # Exact (case-insensitive) match first
    m = transitions[
        (transitions['Previous_Cargo'].str.lower() == prev_cargo.lower()) &
        (transitions['Next_Cargo'].str.lower() == next_cargo.lower())
    ]
    if not m.empty:
        return m.iloc[0]

    # Normalized match (handles small punctuation/name differences)
    pc = _norm(prev_cargo)
    nc = _norm(next_cargo)
    t = transitions.copy()
    t["_pc"] = t["Previous_Cargo"].map(_norm)
    t["_nc"] = t["Next_Cargo"].map(_norm)

    m2 = t[(t["_pc"] == pc) & (t["_nc"] == nc)]
    if not m2.empty:
        return m2.iloc[0]

    # Fallback: same next cargo, or same previous cargo
    m3 = t[(t["_nc"] == nc)]
    if not m3.empty:
        return m3.iloc[0]

    m4 = t[(t["_pc"] == pc)]
    if not m4.empty:
        return m4.iloc[0]

    return None

