# project/common/utils.py
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential
from io import BytesIO
import pandas as pd
import logging

def download_blob_to_df(blob_url: str) -> pd.DataFrame:
    try:
        credential = DefaultAzureCredential()  # This is where the error happens—fix auth first
        blob_client = BlobClient.from_blob_url(blob_url, credential=credential)
        download_stream = blob_client.download_blob()
        bytes_data = download_stream.readall()
        df = pd.read_csv(BytesIO(bytes_data))
        logging.info(f"Loaded DataFrame with {len(df)} rows")
        return df
    except Exception as e:
        logging.error(f"Failed to download blob: {e}")
        raise