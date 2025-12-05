from project.common.cosmos_client import get_containers
from project.common.fraud_rules import high_value, odd_hour, fast_upi_sequences
import pandas as pd

def insert_upi(df):
    containers = get_containers()
    c_upi = containers["UPIEvents"]
    c_fraud = containers["FraudAlerts"]

    df['Timestamp'] = pd.to_datetime(df['Timestamp']).astype(str)
    fast_ids = set(fast_upi_sequences(df))

    for _, row in df.iterrows():
        tid = str(row["TransactionID"])
        customer = str(row["CustomerID"])
        amount = float(row["Amount"])
        ts = str(row["Timestamp"])

        flags = []
        if high_value(amount):
            flags.append("HighValue")
        if odd_hour(ts):
            flags.append("OddHour")
        if tid in fast_ids:
            flags.append("FastUPISequence")

        doc = {
            "id": tid,
            "TransactionID": tid,
            "CustomerID": customer,
            "Amount": amount,
            "Timestamp": ts,
            "Category": "UPI",
            "FraudFlags": flags,
            "isSuspicious": len(flags) > 0
        }

        c_upi.upsert_item(doc)
        if doc["isSuspicious"]:
            c_fraud.upsert_item({
                "id": tid,
                "TransactionID": tid,
                "CustomerID": customer,
                "Amount": amount,
                "Timestamp": ts,
                "FraudFlags": flags
            })
