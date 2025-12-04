import logging
import azure.functions as func
import json
import pandas as pd
from azure.storage.blob import BlobClient
from azure.cosmos import CosmosClient, exceptions
import io
import os


def main(queueItem: func.QueueMessage):

    logging.info("Queue Trigger Function started processing.")

    # --------------------------
    # 1. Read queue message
    # --------------------------
    message = json.loads(queueItem.get_body().decode())
    blob_url = message["blob_url"]

    # --------------------------
    # 2. Download Blob content
    # --------------------------
    blob_client = BlobClient.from_blob_url(blob_url)
    blob_data = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(blob_data))

    logging.info(f"Loaded file: {blob_url}")
    logging.info(f"Record count: {len(df)}")

    # --------------------------
    # 3. Schema Validation
    # --------------------------
    required = ["TransactionID", "Amount", "Timestamp", "CustomerID", "Type"]
    for col in required:
        if col not in df.columns:
            raise Exception(f"Schema Error: Missing column {col}")

    # --------------------------
    # 4. Deduplication
    # --------------------------
    df = df.drop_duplicates(subset=["TransactionID"])

    # --------------------------
    # 5. Classification
    # --------------------------
    df["Category"] = df["Type"].apply(categorize_transaction)

    # --------------------------
    # 6. Suspicious Pattern Rule
    # Example: High amount > 50,000
    # --------------------------
    df["isSuspicious"] = df["Amount"].apply(lambda x: x > 50000)

    # --------------------------
    # 7. Connect to Cosmos DB
    # --------------------------
    cosmos_url = os.getenv("CosmosDBConnection")
    database_name = os.getenv("CosmosDatabaseName")

    cosmos = CosmosClient.from_connection_string(cosmos_url)
    db = cosmos.get_database_client(database_name)

    containers = {
        "ATM": db.get_container_client("ATMTransactions"),
        "UPI": db.get_container_client("UPIEvents"),
        "NEFT": db.get_container_client("NEFTTransactions"),
        "IMPS": db.get_container_client("IMPSTransactions")
    }

    fraud_container = db.get_container_client("FraudAlerts")

    # --------------------------
    # 8. Write rows into Cosmos
    # --------------------------
    for _, row in df.iterrows():

        record = {
            "TransactionID": row["TransactionID"],
            "CustomerID": row["CustomerID"],
            "Amount": float(row["Amount"]),
            "Timestamp": str(row["Timestamp"]),
            "Type": row["Type"],
            "Category": row["Category"],
            "isSuspicious": bool(row["isSuspicious"])
        }

        # Choose correct container
        category = record["Category"]
        if category in containers:
            containers[category].upsert_item(record)

        # If suspicious, also insert into FraudAlerts
        if record["isSuspicious"]:
            fraud_doc = {
                "id": record["TransactionID"],
                "TransactionID": record["TransactionID"],
                "CustomerID": record["CustomerID"],
                "Amount": record["Amount"],
                "Timestamp": record["Timestamp"],
                "Reason": "High value transaction > 50,000"
            }
            fraud_container.upsert_item(fraud_doc)

    logging.info("Writing to Cosmos DB completed successfully.")


def categorize_transaction(t):
    t = str(t).lower()

    if "atm" in t: return "ATM"
    if "upi" in t: return "UPI"
    if "neft" in t: return "NEFT"
    if "imps" in t: return "IMPS"
    return "UNKNOWN"
