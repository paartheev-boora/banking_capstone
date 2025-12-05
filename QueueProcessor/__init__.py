import azure.functions as func
import json
import logging
from project.main import orchestrate_queue_event   # UPDATED IMPORT

def main(queueItem: func.QueueMessage):
    logging.info("QueueProcessor triggered")

    payload = json.loads(queueItem.get_body().decode())
    orchestrate_queue_event(payload)

    logging.info("QueueProcessor completed")
