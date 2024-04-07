# Mango10K

## Introduction
Your friendly neighbourhood vector search-based chatbot, here to help retail investors navigate the complex and tedious task of analyzing company 10K and 10Q filings!

## Technologies
- MongoDB Atlas Vector Search
- OpenAI
- Nomic Embedding Model
- LangChain
- Gradio 

## Team
Special thanks to Daniel, Shah, Somyaranjan, Calvin, and Charles.

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