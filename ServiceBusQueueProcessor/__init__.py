import azure.functions as func
import json
import logging
from project.main import orchestrate_queue_event

def main(msg: func.ServiceBusMessage):
    logging.info("Service Bus QueueProcessor triggered")

    payload = json.loads(msg.get_body().decode())
    orchestrate_queue_event(payload)

    logging.info("QueueProcessor completed")
