import os
import pymongo
from mixpeek.client import Mixpeek
from pydantic import BaseModel


def vector_search(ticker, query):
    CLUSTER_NAME = os.environ["CLUSTER_NAME"]
    DB_NAME = os.environ["DB_NAME"]
    COLLECTION_NAME = os.environ[ticker]
    client = pymongo.MongoClient(CLUSTER_NAME)
    database = client[DB_NAME]
    collection = database[COLLECTION_NAME]

    MIXPEEK_KEY = os.environ["MIXPEEK_KEY"]
    mixpeek = Mixpeek(api_key=MIXPEEK_KEY)
    embedding = mixpeek.embed(
        input=query, 
        model="nomic-ai/nomic-embed-text-v1"
    ).embedding
    chatbot(embedding)

    return


def chatbot(embedding):
    return


if __name__ == "__main__":
    vector_search("TSLA", "Hello")
