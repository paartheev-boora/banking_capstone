REQUIRED_CUSTOMER_COLS = ["CustomerID", "AccountNumber", "Name", "City"]

def validate_customer_schema(df):
    missing = [c for c in REQUIRED_CUSTOMER_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Customer schema validation failed. Missing columns: {missing}")
