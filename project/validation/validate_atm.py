REQUIRED_ATM_COLS = [
    "TransactionID",
    "Timestamp",
    "CustomerID",
    "Amount"
]

def validate_atm_schema(df):
    missing = [c for c in REQUIRED_ATM_COLS if c not in df.columns]
    if missing:
        raise Exception(f"ATM file missing columns: {missing}")