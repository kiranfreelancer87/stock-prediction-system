from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

# Initialize model
model_local = ChatOllama(model="deepseek-r1:14b")

# The paragraph to work with
paragraph = """This python script was written by Mr. IPSIT KUMAR PANDA on 23rd Feb 2025. He is a software developer and Individual Freelancer from Hyderabad,India."""
# 1. Wrap the paragraph in a Document object
doc = Document(page_content=paragraph)

# 2. Split the document into chunks (although in this case it's just one small paragraph)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
doc_splits = text_splitter.split_documents([doc])  # Now passing a list of Document objects

# 3. Convert the document into embeddings and store them in a vector store
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OllamaEmbeddings(model='nomic-embed-text')
)

# 4. Create a retriever to fetch context from the vector store
retriever = vectorstore.as_retriever()

# 5. Define the template for after RAG (Retrieval-Augmented Generation)
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""

after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)

# 6. Define the function to retrieve the context and question, and then run the model
def get_answer_from_paragraph(question: str):
    # Retrieve the relevant documents (though there will only be one paragraph)
    context = retriever.invoke(question)

    # If no context is found (it shouldn't happen in this case)
    if not context:
        return f"No relevant data found for the paragraph."

    # Combine the context and question into the prompt
    prompt = after_rag_prompt.format(context="\n".join([doc.page_content for doc in context]), question=question)

    # Get the model's response based on the context and question
    answer = model_local.invoke(prompt)

    # Return only the content from the AI response
    return answer.content.strip()

# Example: Ask a question about the script author
question = "Who is IPSIT?"
answer = get_answer_from_paragraph(question)
print(answer)
