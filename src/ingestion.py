import fitz  # PyMuPDF
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
def extract_smart_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    
    # Senior Tip: Extracting text while preserving basic structure
    for page in doc:
        full_text += page.get_text("text") + "\n"
    
    # We want chunks big enough to hold a full standard description
    # but small enough to stay relevant.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\nIS ", "\nSection", "\n\n", "\n", " "]
    )
    
    chunks = text_splitter.split_text(full_text)
    
    # Convert to LangChain Document objects
    documents = [Document(page_content=chunk, metadata={"source": "BIS_SP_21"}) for chunk in chunks]
    
    print(f"✅ Extracted {len(documents)} chunks from PDF.")
    return documents



def build_vector_db(documents):
    model_name = "BAAI/bge-small-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True} 

    # Fix the name here:
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'}, 
        encode_kwargs=encode_kwargs
    )
    # ... rest of your code ...

    print("⏳ Generating embeddings (this might take a minute)...")
    vector_db = FAISS.from_documents(documents, embeddings)
    
    # Save it locally so we can load it in the UI and inference scripts
    vector_db.save_local("faiss_index")
    print("✅ Vector database saved to 'faiss_index' folder.")

# Update your main block to run this
if __name__ == "__main__":
    pdf_docs = extract_smart_chunks("data/dataset.pdf")
    build_vector_db(pdf_docs)
