import os
import pymongo
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_nomic import NomicEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

def chatbot(ticker, query):
    '''
    Performs vector search on MongoDB Atlas vector store to retrieve relevant embeddings
    while filtering results based on ticker specified.
    Uses OpenAI's gpt-3.5-turbo to generate a response given the retrieved embeddings.

    Args:
        ticker (str): The stock ticker (e.g. AAPL) specified for filtering.
        query (str): The question inputted by the user.

    Returns:
        retriever_output (str): The chatbot's answer.
    '''
    CLUSTER_NAME = os.getenv("CLUSTER_NAME")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    client = pymongo.MongoClient(CLUSTER_NAME)
    database = client[DB_NAME]
    collection = database[COLLECTION_NAME]
    ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

    embeddings = NomicEmbeddings(
        nomic_api_key=os.getenv("NOMIC_API_KEY"),
        model='nomic-embed-text-v1.5',
    )

    # Define the filter based on the metadata field and value
    vector_search = MongoDBAtlasVectorSearch(
        embedding=embeddings,
        collection=collection,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    filter_dict = {"metadata.ticker": ticker}
    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )
    
    retriever = vector_search.as_retriever(filter=filter_dict)
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    
    retriever_output = qa.run(query)
    return retriever_output
    
if __name__ == "__main__":
    load_dotenv()
    print(chatbot("TSLA", "Is the market for energy storage products competitive?"))
