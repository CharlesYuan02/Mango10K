from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import UnstructuredHTMLLoader
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_nomic import NomicEmbeddings
import requests


import os
from dotenv import load_dotenv

load_dotenv()

## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

# Connect to MongoDB Atlas cluster
client = MongoClient(os.getenv("MONGO_URI"))

DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

def seeder(url, cname):
    # r = requests.get(url)
    # with open("docs.html", "w") as f:
    #     f.write(r.text)

    loader = UnstructuredHTMLLoader("Dataset/tsla-20231231.html")
    # cname = loader.metadata["cname"]
    data = loader.load()

    # Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(data)

    embeddings = NomicEmbeddings(
        nomic_api_key=os.getenv("NOMIC_API_KEY"),
        model='nomic-embed-text-v1.5',
    )
    
    for i in range(len(texts)):
        texts[i].metadata["source"] = url
        texts[i].metadata["ticker"] = cname

    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=texts,
        embedding=embeddings,
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )
    
if __name__ == "__main__":
    seeder("https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm", "TSLA")
    print("Seeding complete.")
