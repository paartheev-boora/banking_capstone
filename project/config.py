import os

# Storage (Blob + Queue) connection string
STORAGE_CONNECTION_STRING = os.environ["AzureWebJobsStorage"]

# Service Bus connection
SERVICE_BUS_CONNECTION = os.environ["ServiceBusConnection"]

# Cosmos DB connection
COSMOS_CONNECTION = os.environ["CosmosDBConnection"]
COSMOS_DB_NAME = os.environ["CosmosDatabaseName"]
