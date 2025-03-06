from fastapi import FastAPI
import logging

app = FastAPI()


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    return {
        "context": context,
        "event": event
    }
