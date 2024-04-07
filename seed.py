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
    """
    Seed the MongoDB collection with documents extracted from the given URL.

    Args:
        url (str): The URL from which to extract documents.
        cname (str): The name of the company associated with the documents.

    Returns:
        None
    """
    # r = requests.get(url)
    # with open("docs.html", "w") as f:
    #     f.write(r.text)

    loader = UnstructuredHTMLLoader(url)
    data = loader.load()

    # Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=500)
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
    seeder("Dataset/tsla-20231231.html", "APPL")
    print("Seeding complete.")
