# Stock Prediction System Using DeepSeek-R1

## Overview
The stock prediction system leverages DeepSeek-R1 to analyze technical and fundamental data, identifying potential positive stocks. It integrates structured financial data and live news feeds for enhanced prediction accuracy.

## Key Features
- **Fundamental & Technical Data Analysis**
- **Live News Integration**
- **Retrieval-Augmented Generation (RAG) for Context Retrieval**
- **Parallelized Embedding Generation**
- **ChromaDB for Vector Storage**
- **Gradio-Based User Interface**

## Data Sources
The system processes structured financial data from multiple categories:
- **Overview**
- **Performance**
- **Valuation**
- **Dividends**
- **Profitability**
- **Income Statement**
- **Balance Sheet**
- **Cash Flow**

## Implementation Details
### 1. Data Loading & Preprocessing# Stock Prediction System Using DeepSeek-R1

## Overview
The stock prediction system analyzes technical and fundamental data to identify positive stocks using the DeepSeek-R1 model. It processes financial data and integrates live news feeds for enhanced accuracy.

## Key Features
- Fundamental & Technical Data Analysis
- Live News Integration
- Retrieval-Augmented Generation (RAG)
- Parallelized Embedding Generation
- ChromaDB for Vector Storage
- Gradio-Based User Interface

## Data Sources
The system processes structured data from multiple categories including:
- Overview
- Performance
- Valuation
- Dividends
- Profitability
- Income Statement
- Balance Sheet
- Cash Flow

## Implementation

### 1. Data Loading & Preprocessing
```python
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = CSVLoader("csv_files/overview.csv")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents=documents)
```

### 2. Embedding Generation
```python
from concurrent.futures import ThreadPoolExecutor
from langchain_ollama import OllamaEmbeddings

embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")

def generate_embedding(chunk):
    return embedding_function.embed_query(chunk.page_content)

with ThreadPoolExecutor() as executor:
    embeddings = list(executor.map(generate_embedding, chunks))
```

### 3. ChromaDB Storage
```python
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings())
collection = client.create_collection(name="stock_analysis")
for idx, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        metadatas=[{'id': idx}],
        embeddings=[embeddings[idx]],
        ids=[str(idx)]
    )
```

### 4. Context Retrieval & Model Querying
```python
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

def retrieve_context(question):
    retriever = Chroma(collection_name="stock_analysis", client=client, embedding_function=embedding_function).as_retriever()
    results = retriever.invoke(question)
    return "\n\n".join([doc.page_content for doc in results])

def query_deepseek(question, context):
    formatted_prompt = f"Question: {question}. Answer from the context only.\n\nContext: {context}."
    ollama = OllamaLLM(model="deepseek-r1:1.5b")
    return ollama.invoke(input=formatted_prompt).strip()
```

### 5. Gradio Interface
```python
import gradio as gr

def ask_question(question):
    context = retrieve_context(question)
    return query_deepseek(question, context)

interface = gr.Interface(fn=ask_question, inputs="text", outputs="text",
                         title="Stock Prediction Chatbot",
                         description="Ask about stock trends based on fundamental & technical data.")
interface.launch()
```

## Future Enhancements
- Real-time Data Updates
- Sentiment Analysis
- Advanced Technical Indicators
- Multi-Model Support

## Conclusion
The system combines structured financial data, real-time news, and DeepSeek-R1 for precise stock predictions, leveraging RAG techniques for enhanced insights.


CSV files containing stock-related data are loaded and split into manageable chunks for processing.
```python
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = CSVLoader("csv_files/overview.csv")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents=documents)
```

### 2. Embedding Generation
Parallelized embeddings are generated using DeepSeek-R1.
```python
from concurrent.futures import ThreadPoolExecutor
from langchain_ollama import OllamaEmbeddings

embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")

def generate_embedding(chunk):
    return embedding_function.embed_query(chunk.page_content)

with ThreadPoolExecutor() as executor:
    embeddings = list(executor.map(generate_embedding, chunks))
```

### 3. Storing Embeddings in ChromaDB
ChromaDB is used for efficient vector storage and retrieval.
```python
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings())
collection = client.create_collection(name="stock_analysis")
for idx, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        metadatas=[{'id': idx}],
        embeddings=[embeddings[idx]],
        ids=[str(idx)]
    )
```

### 4. Context Retrieval & Model Querying
Relevant financial data is retrieved using RAG and passed to DeepSeek-R1 for response generation.
```python
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

def retrieve_context(question):
    retriever = Chroma(collection_name="stock_analysis", client=client, embedding_function=embedding_function).as_retriever()
    results = retriever.invoke(question)
    return "\n\n".join([doc.page_content for doc in results])

def query_deepseek(question, context):
    formatted_prompt = f"Question: {question}. Answer from the context only.\n\nContext: {context}."
    ollama = OllamaLLM(model="deepseek-r1:1.5b")
    return ollama.invoke(input=formatted_prompt).strip()
```

### 5. Gradio User Interface
A simple web interface using Gradio for user interaction.
```python
import gradio as gr

def ask_question(question):
    context = retrieve_context(question)
    return query_deepseek(question, context)

interface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="Stock Prediction Chatbot",
    description="Ask about stock trends based on fundamental & technical data."
)
interface.launch()
```

## Future Enhancements
- **Real-time Data Updates**
- **Sentiment Analysis for News Data**
- **Integration of Advanced Technical Indicators**
- **Multi-Model Support for Enhanced Predictions**

## Conclusion
This system integrates structured financial data, real-time news, and DeepSeek-R1 to provide accurate stock predictions using RAG techniques. It efficiently retrieves and analyzes financial parameters, ensuring data-driven stock trend insights.
