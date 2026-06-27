import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_or_load_vector_store(documents=None, index_path="models/faiss_index"):
    embeddings = get_embeddings()
    
    if documents:
        # Aqui está o segredo: dividir documentos grandes em blocos de 500 caracteres com sobreposição
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs_splitted = text_splitter.split_documents(documents)
        
        vector_store = FAISS.from_documents(docs_splitted, embeddings)
        vector_store.save_local(index_path)
        return vector_store
        
    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
    raise FileNotFoundError("Índice FAISS não encontrado.")