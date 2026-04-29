import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    # allow_dangerous_deserialization is safe for your local index
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vector_db.as_retriever(search_kwargs={"k": 5})

def retrieve_context(query):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

def generate_rationale(query, context):
    # Using the Gemini 3 Flash Lite model which showed success in your test
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.0, # Zero temperature is safer for factual compliance
        convert_system_message_to_human=True
    )

   # Inside src/retrieval.py -> generate_rationale()

    system_prompt = (
    "You are an expert BIS Compliance Officer. "
    "STRICT RULE: Your response must be in plain MARKDOWN text only. "
    "DO NOT return JSON, dictionaries, or 'type/text' keys. "
    "Format as follows:\n"
    "### 📍 Relevant Standards\n"
    "* **IS Number**: 1-sentence rationale.\n"
    "* **IS Number**: 1-sentence rationale."
)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"Context: {context}\n\nProduct: {query}")
    ])

    chain = prompt | llm
    try:
        response = chain.invoke({"context": context, "query": query})
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"