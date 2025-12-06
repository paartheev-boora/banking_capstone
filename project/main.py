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
    try:
        blob_url = event.get("blob_url")
        if not blob_url:
            logging.error("Missing blob_url in event payload")
            return

        logging.info(f"Processing blob: {blob_url}")

        # Normalize path
        path = blob_url.lower()

        # ----------------------------------------
        # 1. LOAD DATAFRAME FROM BLOB
        # ----------------------------------------
        df = download_blob_to_df(blob_url)
        logging.info(f"Loaded dataframe with {len(df)} rows")

        # ----------------------------------------
        # 2. ROUTE BASED ON RAW FOLDER STRUCTURE
        # ----------------------------------------

        # ATM Transactions
        if "/raw/atm/" in path:
            logging.info("Detected ATM transactions file")
            validate_atm_schema(df)
            insert_atm(df)
            logging.info("ATM ingestion completed")
            return

        # UPI Events
        if "/raw/upi/" in path:
            logging.info("Detected UPI events file")
            validate_upi_schema(df)
            insert_upi(df)
            logging.info("UPI ingestion completed")
            return

        # CUSTOMER PROFILE (exclude KYC docs)
        if "/raw/customers/" in path and "/kyc_docs/" not in path:
            logging.info("Detected customer profile file")
            validate_customer_schema(df)
            insert_account_profile(df)
            logging.info("Customer profile ingestion completed")
            return

        # No matching route
        logging.warning(f"No routing rule matched for: {blob_url}")

    except Exception as e:
        logging.error(f"Error processing event: {str(e)}")
        raise  # Allow Service Bus retry mechanism
