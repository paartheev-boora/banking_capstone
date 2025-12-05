from project.validation.validate_customers import validate_customer_schema
from project.containers.create_account_profile import insert_account_profile

def process_customers_df(df):
    validate_customer_schema(df)
    insert_account_profile(df)
