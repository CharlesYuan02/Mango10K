from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_nomic import NomicEmbeddings
import requests


import os
from dotenv import load_dotenv

load_dotenv()
# os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

# Connect to MongoDB Atlas cluster
client = MongoClient(os.getenv("MONGO_URI"))

DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]


sc_url = "https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm"
r = requests.get(sc_url)
with open("tsla.html", "w") as f:
    f.write(r.text)

loader = UnstructuredHTMLLoader("tsla.html")
data = loader.load()
print(data)


# Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(data)

embeddings = NomicEmbeddings(
    nomic_api_key=os.getenv("NOMIC_API_KEY"),
    model='nomic-embed-text-v1.5',
)

vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=texts,
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)
