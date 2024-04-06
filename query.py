import os
import pymongo
import requests
import json
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from langchain.vectorstores import MongoDBAtlasVectorSearch
from mixpeek.client import Mixpeek
from pydantic import BaseModel


def chatBot(ticker, query):
    CLUSTER_NAME = os.environ["CLUSTER_NAME"]
    DB_NAME = os.environ["DB_NAME"]
    COLLECTION_NAME = os.environ[ticker]
    client = pymongo.MongoClient(CLUSTER_NAME)
    database = client[DB_NAME]
    collection = database[COLLECTION_NAME]
    ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

    MIXPEEK_KEY = os.environ["MIXPEEK_KEY"]
    mixpeek = Mixpeek(api_key=MIXPEEK_KEY)

    embedding = mixpeek.embed(
        input=query, 
        model="nomic-ai/nomic-embed-text-v1"
    ).embedding

    vector_search = MongoDBAtlasVectorSearch(
        documents=query,
        embedding=embedding,
        collection=COLLECTION_NAME,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    llm = OpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
    )
    
    retriever = vector_search.as_retriever()
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    
    retriever_output = qa.run(query)

    return retriever_output
    
if __name__ == "__main__":
    print(chatBot("TSLA", "What is the projected growth for 2024?"))
