import os
from azure.cosmos import CosmosClient

def get_cosmos_client():
    conn = os.getenv("CosmosDBConnection")
    if not conn:
        raise Exception("CosmosDBConnection not set in environment")
    return CosmosClient.from_connection_string(conn)

def get_database(dbname=None):
    client = get_cosmos_client()
    if not dbname:
        dbname = os.getenv("CosmosDatabaseName")
    return client.get_database_client(dbname)

def get_containers():
    db = get_database()
    return {
        "AccountProfile": db.get_container_client("AccountProfile"),
        "ATMTransactions": db.get_container_client("ATMTransactions"),
        "UPIEvents": db.get_container_client("UPIEvents"),
        "FraudAlerts": db.get_container_client("FraudAlerts")
    }
