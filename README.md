# Mango10K

<img src="https://github.com/Chubbyman2/Mango10K/blob/main/docs/demo.PNG">

## Introduction
Your friendly neighbourhood vector search-based chatbot, here to help retail investors navigate the complex and tedious task of analyzing company 10K and 10Q filings!

## Getting Started
To get started, you'll need a MongoDB Atlas cluster, OpenAI API key, Langchain API key, and a Nomic API key. See [.env.example](https://github.com/Chubbyman2/Mango10K/blob/main/.env.example) for more information.
### Vector Search Index
Once you have your MongoDB Atlas cluster, database, and collection, you'll need to apply a vector search index to it. See [these instructions](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/) for the exact steps. We used the following configuration:
```
{
  "fields": [
    {
      "numDimensions": 768,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

### Prerequisites
```
gradio==4.25.0
langchain==0.1.14
langchain-community==0.0.31
langchain-nomic==0.0.2
openai==1.16.2
pydantic==2.6.4
pymongo==4.6.3
python-dotenv==1.0.1
sec_cik_mapper==2.1.0
```

### Embeddings and Vector Search
To try an example, run [seed.py](https://github.com/Chubbyman2/Mango10K/blob/main/seed.py) to generate and store the vector embeddings from the most recent 10K's and 10Q's from AAPL and TSLA. Make sure you have your vector search index configured! Then, you can run [frontend.py](https://github.com/Chubbyman2/Mango10K/blob/main/frontend.py) to launch the Gradio web app, and ask some questions regarding the financials of Tesla and Apple!

## Technologies
### MongoDB Atlas
MongoDB Atlas was used to store the vector embeddings generated, as well as return results from vector search.

### OpenAI
OpenAI's gpt-3.5-turbo was used to generate coherent responses based on the retrieved embeddings from MongoDB Atlas, in order to answer the user's question.

### Nomic
Nomic's model was used for the actual vector embeddings. Specifically, we used the nomic-embed-text-v1.5 model.

### LangChain
LangChain was used to load the HTML documents, perform the vector store and vector search, as well as generate the actual response. The backend model was OpenAI's, but the module used was LangChain.

### Gradio
Gradio was used to create the web app which users can interact with in order to use our application.

## Code
### seed.py
This code snippet is a function called seeder that seeds a MongoDB collection with documents extracted from a given URL. It splits the text into smaller chunks, adds metadata to each chunk, and then uses NomicEmbeddings to generate embeddings for the chunks. Finally, it uses MongoDBAtlasVectorSearch to store the embeddings in the MongoDB collection.

- Inputs
    - url (str): The URL from which to extract documents.
    - cname (str): The name of the company associated with the documents.
- Flow
    - Load the HTML content from the given URL using UnstructuredHTMLLoader.
    - Split the text into smaller chunks using RecursiveCharacterTextSplitter.
    - Add metadata to each chunk, including the source URL and company ticker.
    - Generate embeddings for the chunks using NomicEmbeddings.
    - Store the embeddings in the MongoDB collection using MongoDBAtlasVectorSearch.

### edgar_scraper.py
The code snippet is a function called 'edgar_scraper' that scrapes data from the SEC (Securities and Exchange Commission) website for a given company ticker. It uses a StockMapper object to map the ticker to the corresponding CIK (Central Index Key) value. It then constructs a URL using the CIK value and sends a GET request to retrieve the JSON response. The response is then pretty-printed and saved to a file with the ticker name as the filename.

- Inputs
    - The input to the function is the ticker name of a company.

- Flow
    - Create a StockMapper object.
    - Get the CIK value for the given ticker from the StockMapper object.
    - Format the CIK value as a 10-digit string.
    - Construct the URL for the SEC API using the CIK value.
    - Set the User-Agent header to avoid a 401 response.
    - Send a GET request to the SEC API and retrieve the JSON response.
    - Pretty-print the JSON response.
    - Save the pretty-printed response to a file with the ticker name as the filename.

### query.py
The code snippet is a function called chatbot that takes in a ticker and a query as inputs. It connects to a MongoDB database, retrieves the necessary data based on the ticker, and performs a retrieval-based question answering using OpenAI's language model. The function returns the output of the question answering process.

- Inputs
    - ticker: A string representing the ticker symbol of a company.
    - query: A string representing the question/query to be answered.
- Flow
    - The code imports necessary libraries and modules.
    - It retrieves environment variables for the MongoDB connection and OpenAI API key.
    - It establishes a connection to the MongoDB database using the provided environment variables.
    - It initializes the NomicEmbeddings object for text embeddings using the Nomic API key.
    - It creates a MongoDBAtlasVectorSearch object for vector-based search using the initialized embeddings and the MongoDB collection.
    - It defines a filter dictionary based on the ticker input.
    - It initializes the OpenAI language model for language generation using the OpenAI API key.
    - It creates a RetrievalQA object for question answering using the initialized language model and the vector search retriever.
    - It runs the question answering process using the provided query.
    - It returns the output of the question answering process.

### frontend.py
The code snippet is a function called 'main' that serves as the entry point for a chatbot application. It takes three inputs: 'message', 'history', and 'ticker'. The function loads environment variables using the 'load_dotenv' function from the 'dotenv' module. It then calls the 'chatbot' function from the 'query' module, passing the 'ticker' and 'message' as arguments. The output of the 'chatbot' function is returned as the output of the 'main' function. Finally, the 'main' function is used as the callback function for a Gradio ChatInterface, which launches the chatbot application.

- Inputs
    - message: A string representing the user's message.
    - history: A string representing the chat history.
    - ticker: A string representing the ticker symbol.
- Flow
    - The 'load_dotenv' function is called to load environment variables.
    - The 'chatbot' function is called with the 'ticker' and 'message' as arguments, and the output is stored in the 'output' variable.
    - The 'output' variable is returned as the output of the 'main' function.
    - The 'main' function is used as the callback function for a Gradio ChatInterface.
    - The Gradio ChatInterface is launched, allowing users to interact with the chatbot.
 
## Team
Special thanks to Daniel, Shah, Somyaranjan, Calvin, and Charles.

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/Mango10K/blob/main/LICENSE">LICENSE</a> file for details.
