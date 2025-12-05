from project.common.cosmos_client import get_containers
from project.common.fraud_rules import high_value, odd_hour

def insert_atm(df):
    containers = get_containers()
    c_atm = containers["ATMTransactions"]
    c_fraud = containers["FraudAlerts"]

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

        doc = {
            "id": tid,
            "TransactionID": tid,
            "CustomerID": customer,
            "Amount": amount,
            "Timestamp": ts,
            "Category": "ATM",
            "FraudFlags": flags,
            "isSuspicious": len(flags) > 0
        }

        c_atm.upsert_item(doc)
        if doc["isSuspicious"]:
            c_fraud.upsert_item({
                "id": tid,
                "TransactionID": tid,
                "CustomerID": customer,
                "Amount": amount,
                "Timestamp": ts,
                "FraudFlags": flags
            })