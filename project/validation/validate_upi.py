REQUIRED_UPI_COLS = ["TransactionID", "Timestamp", "CustomerID", "Amount"]

def validate_upi_schema(df):
    missing = [c for c in REQUIRED_UPI_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"UPI schema validation failed. Missing columns: {missing}")
