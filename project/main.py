import logging
import pandas as pd
from project.common.utils import download_blob_to_df
from project.validation.validate_atm import validate_atm_schema
from project.validation.validate_upi import validate_upi_schema
from project.validation.validate_customers import validate_customer_schema
from project.containers.create_account_profile import insert_account_profile
from project.containers.create_atm_transactions import insert_atm
from project.containers.create_upi_events import insert_upi


def orchestrate_queue_event(event):
    blob_url = event.get("blob_url")

    if not blob_url:
        logging.error("Missing blob_url in event")
        return

    logging.info(f"Processing blob: {blob_url}")

    # Convert to lowercase for easy matching
    path = blob_url.lower()

    # -----------------------------------------------------
    # 1. DOWNLOAD FILE
    # -----------------------------------------------------
    df = download_blob_to_df(blob_url)
    logging.info(f"Loaded {len(df)} rows")

    # -----------------------------------------------------
    # 2. ROUTE BY FOLDER STRUCTURE
    # -----------------------------------------------------

    # ATM  (Azure storage or your local folder)
    if "/raw/atm/" in path or "bank_delta/csv/atm_" in path:
        validate_atm_schema(df)
        insert_atm(df)
        logging.info("ATM file processed")
        return

    # UPI
    if "/raw/upi/" in path or "bank_delta/csv/upi_" in path:
        validate_upi_schema(df)
        insert_upi(df)
        logging.info("UPI file processed")
        return

    # CUSTOMERS
    if "/raw/customers/" in path or "bank_delta/customer/" in path:
        validate_customer_schema(df)
        insert_account_profile(df)
        logging.info("Customer file processed")
        return

    logging.warning(f"No matching category found for path: {blob_url}")