import re
import gradio as gr
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from chromadb.config import Settings
from chromadb import Client
from langchain.document_loaders import CSVLoader

loader = CSVLoader("csv_files/overview.csv")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents=documents)

# Initialize Ollama embeddings using DeepSeek-R1
embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")


# Parallelize embedding generation
def generate_embedding(chunk):
    print(chunk)
    print("...")
    return embedding_function.embed_query(chunk.page_content)


with ThreadPoolExecutor() as executor:
    embeddings = list(executor.map(generate_embedding, chunks))

# Initialize Chroma client and create/reset the collection
client = Client(Settings())
# client.delete_collection(name="foundations_of_llms")  # Delete existing collection (if any)
collection = client.create_collection(name="foundations_of_llms")

# Add documents and embeddings to Chroma
for idx, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        metadatas=[{'id': idx}],
        embeddings=[embeddings[idx]],
        ids=[str(idx)]  # Ensure IDs are strings
    )

# Initialize retriever using Ollama embeddings for queries
retriever = Chroma(collection_name="foundations_of_llms", client=client,
                   embedding_function=embedding_function).as_retriever()


def retrieve_context(question):
    # Retrieve relevant documents
    results = retriever.invoke(question)
    # Combine the retrieved content
    context = "\n\n".join([doc.page_content for doc in results])
    return context


def query_deepseek(question, context):
    # Format the input prompt
    formatted_prompt = f"Question: {question}. Answer from the context only.\n\nContext: {context}. You need to analyze all stocks in the document provided and answer based on that. And understand the each column in the csv too with respective values."

    # Query DeepSeek-R1 using OllamaLLM with `.invoke()`
    ollama = OllamaLLM(model="deepseek-r1:1.5b")
    response = ollama.invoke(input=formatted_prompt)  # Use invoke instead of chat

    # Clean and return the response
    response_content = response
    final_answer = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
    return final_answer


def ask_question(question):
    # Retrieve context and generate an answer using RAG
    context = retrieve_context(question)
    answer = query_deepseek(question, context)
    return answer


# Set up the Gradio interface
interface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="RAG Chatbot: Foundations of LLMs",
    description="Ask any question about the Foundations of LLMs book. Powered by DeepSeek-R1."
)
interface.launch()
