from project.common.cosmos_client import get_containers

def insert_account_profile(df):
    c = get_containers()["AccountProfile"]
    for _, row in df.iterrows():
        doc = {
            "id": str(row["CustomerID"]),
            "CustomerID": str(row["CustomerID"]),
            "AccountNumber": str(row.get("AccountNumber","")),
            "Name": row.get("Name"),
            "City": row.get("City")
        }
        c.upsert_item(doc)
