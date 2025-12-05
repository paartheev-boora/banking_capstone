from project.validation.validate_atm import validate_atm_schema
from project.containers.create_atm_transactions import insert_atm

def process_atm_df(df):
    validate_atm_schema(df)
    insert_atm(df)
