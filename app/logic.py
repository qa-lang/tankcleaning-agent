
def find_transition(transitions, prev_cargo, next_cargo):
    match = transitions[
        (transitions['Previous_Cargo'].str.lower() == prev_cargo.lower()) &
        (transitions['Next_Cargo'].str.lower() == next_cargo.lower())
    ]
    if not match.empty:
        return match.iloc[0]
    else:
        # Fallback: find similar transitions (simplified for starter)
        similar = transitions[transitions['Next_Cargo'].str.lower() == next_cargo.lower()]
        return similar.iloc[0] if not similar.empty else None
