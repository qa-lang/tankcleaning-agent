
# data_loader.py
import os
import pandas as pd
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
XLSX_PATH = os.path.join(DATA_DIR, 'Tank_cleaning.xlsx')

def _clean_text(s):
    if pd.isna(s):
        return ""
    # Remove Excel's CR markers and newlines, normalize spaces
    return (
        str(s)
        .replace("_x000D_", " ")
        .replace("\r", " ")
        .replace("\n", " ")
        .strip()
    )

def _first_col_with(df, substring):
    """Return first column whose name contains substring (case-insensitive), else None."""
    substring = substring.lower()
    for c in df.columns:
        if c and substring in str(c).lower():
            return c
    return None

def load_transitions():
    """
    Load transitions from Tank_cleaning.xlsx where each memo is stored as rows:
    ITEMNAME = field label, BLOB_VALUE = value, grouped by IDTAB.
    We pivot to wide format and then map to the app's schema.
    """
    if not os.path.exists(XLSX_PATH):
        raise FileNotFoundError(f"Excel file not found at: {XLSX_PATH}")

    # Read the first sheet. Your file uses columns like BLOB_VALUE, ITEMNAME, IDTAB. [1](https://siriusshippingeu-my.sharepoint.com/personal/torbjorn_karlsson_siriusshipping_eu/_layouts/15/download.aspx?UniqueId=2a6559e8-d456-4b01-8908-1108cd5d7012&Translate=false&tempauth=v1.eyJzaXRlaWQiOiJmMzlmZGMwOS0wNzVkLTQ4YmMtYTVjZi0yNjUyOGNiOTZhNzUiLCJhcHBfZGlzcGxheW5hbWUiOiJPZmZpY2UgMzY1IFNlYXJjaCBTZXJ2aWNlIiwiYXBwaWQiOiI2NmE4ODc1Ny0yNThjLTRjNzItODkzYy0zZThiZWQ0ZDY4OTkiLCJhdWQiOiIwMDAwMDAwMy0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvc2lyaXVzc2hpcHBpbmdldS1teS5zaGFyZXBvaW50LmNvbUA5ODk4OTc4Ni1iNzRhLTQwMzMtYjgxMC02Mjc0Y2NhNDhjZmUiLCJleHAiOiIxNzU1ODcyNDA3In0.CkAKDGVudHJhX2NsYWltcxIwQ0tYWm9jVUdFQUFhRmpSblZuTjZObTVhZUZWMVpUZEpPRU10TTBwM1FVRXFBQT09CjIKCmFjdG9yYXBwaWQSJDAwMDAwMDAzLTAwMDAtMDAwMC1jMDAwLTAwMDAwMDAwMDAwMAoKCgRzbmlkEgI2NBILCJj4q9qU4rA-EAUaDDQwLjEyNi41My4yNSosY2xIMjU0OTlKVEZyVndqVFZiNDFBVVpIYm5sdTFjelprMGtUeG5GSTJiVT0wrwE4AUIQob5ByaZQANCYugaQ0MCXtkoQaGFzaGVkcHJvb2Z0b2tlblIIWyJrbXNpIl1qJDAwNWQ5MTM5LWY0MjQtNzhhMi1kNWEwLWYwZjJiYWEzMWNhN3IpMGguZnxtZW1iZXJzaGlwfDEwMDMyMDAwOTFhNzVlY2JAbGl2ZS5jb216ATKCARIJhpeYmEq3M0ARuBBidMykjP6SAQlUb3JiasO2cm6aAQhLYXJsc3NvbqIBI3RvcmJqb3JuLmthcmxzc29uQHNpcml1c3NoaXBwaW5nLmV1qgEQMTAwMzIwMDA5MUE3NUVDQrIBOmdyb3VwLnJlYWQgYWxsZmlsZXMucmVhZCBhbGxwcm9maWxlcy5yZWFkIGFsbHByb2ZpbGVzLnJlYWTIAQE.BU7Q0ydAwcZItAh8shGtCrHsNeBdJRkws0ak2lz2r9E&ApiVersion=2.0&web=1)
    df_raw = pd.read_excel(XLSX_PATH, sheet_name=0, engine="openpyxl")

    # Try to normalize column names if they differ in capitalization/order
    cols = list(df_raw.columns)
    # Best-effort rename of first three columns to expected names
    rename_map = {}
    if len(cols) >= 3:
        # Heuristics if names aren’t exact
        for c in cols:
            lc = str(c).lower()
            if "blob" in lc and "value" in lc:
                rename_map[c] = "BLOB_VALUE"
            elif "item" in lc and "name" in lc:
                rename_map[c] = "ITEMNAME"
            elif "idtab" in lc or lc in ("id",):
                rename_map[c] = "IDTAB"
        if rename_map:
            df_raw = df_raw.rename(columns=rename_map)

    required = {"BLOB_VALUE", "ITEMNAME", "IDTAB"}
    if not required.issubset(set(df_raw.columns)):
        raise ValueError(
            f"Unexpected Excel format. Found columns {list(df_raw.columns)}; "
            "expected at least BLOB_VALUE, ITEMNAME, IDTAB."
        )

    # Keep only the essential columns and clean text
    df_kv = (
        df_raw[["IDTAB", "ITEMNAME", "BLOB_VALUE"]]
        .dropna(subset=["ITEMNAME", "IDTAB"], how="any")
        .assign(
            ITEMNAME=lambda d: d["ITEMNAME"].astype(str).str.strip(),
            BLOB_VALUE=lambda d: d["BLOB_VALUE"].map(_clean_text),
            IDTAB=lambda d: d["IDTAB"].astype(str).str.strip(),
        )
    )

    # Pivot key–value to one row per memo (IDTAB)
    df_wide = (
        df_kv.pivot_table(
            index="IDTAB", columns="ITEMNAME", values="BLOB_VALUE", aggfunc="first"
        )
        .reset_index()
    )

    # Find likely columns for the fields we need
    prev_col   = _first_col_with(df_wide, "cleaning from")
    next_col   = _first_col_with(df_wide, "cleaning to")
    method_col = _first_col_with(df_wide, "method")
    result_col = _first_col_with(df_wide, "cleaning results")
    comm_col   = _first_col_with(df_wide, "comments")
    matrix_col = _first_col_with(df_wide, "matrix")

    # Build the standardized transitions DataFrame
    df_out = pd.DataFrame({
        "Transition_ID": range(1, len(df_wide) + 1),
        "Previous_Cargo": df_wide.get(prev_col, pd.Series("", index=df_wide.index)).fillna(""),
        "Next_Cargo": df_wide.get(next_col, pd.Series("", index=df_wide.index)).fillna(""),
        "HM50_Code": "N/A",
        "HM50_Code_Description": "N/A",
        "HM50_Notes": "N/A",
        "Memo_Count": 1,
        "Memo_Methods": df_wide.get(method_col, pd.Series("", index=df_wide.index)).fillna(""),
        "Memo_Results": df_wide.get(result_col, pd.Series("", index=df_wide.index)).fillna(""),
        "Memo_Lessons": (
            df_wide.get(comm_col, pd.Series("", index=df_wide.index)).fillna("")
            .astype(str)
            + " "
            + df_wide.get(matrix_col, pd.Series("", index=df_wide.index)).fillna("").astype(str)
        ).str.strip(),
        "Similar_Transitions": "",
        "Suggested_Best_Practice": "",
        "Sensitive_Cargo_Flag": False,
        "Source_HM50": "",
        "Source_Memo_IDs": df_wide["IDTAB"],
        "Last_Updated": date.today().isoformat(),
    })

    # Basic cleanup: remove empty rows where both cargos are missing
    mask_nonempty = df_out["Previous_Cargo"].str.strip().ne("") | df_out["Next_Cargo"].str.strip().ne("")
    df_out = df_out.loc[mask_nonempty].reset_index(drop=True)

    # Normalize cargo names a bit (trim, remove extra spaces)
    for col in ["Previous_Cargo", "Next_Cargo"]:
        df_out[col] = (
            df_out[col]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    return df_out

