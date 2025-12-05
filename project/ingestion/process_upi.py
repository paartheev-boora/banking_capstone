from project.validation.validate_upi import validate_upi_schema
from project.containers.create_upi_events import insert_upi

def process_upi_df(df):
    validate_upi_schema(df)
    insert_upi(df)
