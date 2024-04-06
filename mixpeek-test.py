import os
import pymongo
from mixpeek.client import Mixpeek
from pydantic import BaseModel

CLUSTER_NAME = os.environ["CLUSTER_NAME"]
DB_NAME = os.environ["DB_NAME"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
client = pymongo.MongoClient(CLUSTER_NAME)
database = client[DB_NAME]
collection = database[COLLECTION_NAME]
collection.delete_many(filter={})

MIXPEEK_KEY = os.environ["MIXPEEK_KEY"]
mixpeek = Mixpeek(api_key=MIXPEEK_KEY)

class PaperDetails(BaseModel):
    output: str

response = mixpeek.generate(
    model={"provider":"GPT", "model":"gpt-3.5-turbo"},
    response_format=PaperDetails,
    context="What is the shape of the Earth?", # Pls don't say "flat"
    messages=[],
    settings={"temperature":0.5},
).response

print(response)

embedding = mixpeek.embed(
    input="hello world", 
    model="nomic-ai/nomic-embed-text-v1"
).embedding

print(len(embedding))