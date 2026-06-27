from assistente_rag_lexml.data_ingestion import load_car_documents
from assistente_rag_lexml.vector_store import create_or_load_vector_store

# 1. Carrega os PDFs
docs = load_car_documents()

# 2. Cria o índice (isso pode demorar uns segundos por causa dos 316 documentos)
create_or_load_vector_store(documents=docs)

print("Índice FAISS criado e salvo com sucesso!")