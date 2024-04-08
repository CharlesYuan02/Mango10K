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
unstructured==0.13.2
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

## Team
Special thanks to Daniel, Shah, Somyaranjan, Calvin, and Charles of team MangoDB!

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/Mango10K/blob/main/LICENSE">LICENSE</a> file for details.
