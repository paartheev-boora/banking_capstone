import pandas as pd
import io
import os
from azure.storage.blob import BlobClient

def download_blob_to_df(path):
    # CASE 1: Local file (bank_delta path)
    if path.startswith("bank_delta") or "/" in path and not path.startswith("http"):
        return pd.read_csv(path)

    # CASE 2: Azure Blob Storage URL
    blob = BlobClient.from_blob_url(path)
    data = blob.download_blob().readall()

    # Try CSV then JSONL
    try:
        return pd.read_csv(io.BytesIO(data))
    except:
        try:
            return pd.read_json(io.BytesIO(data), lines=True)
        except:
            raise Exception("Unable to parse blob file")