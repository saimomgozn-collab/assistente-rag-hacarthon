import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_car_documents(raw_dir="data/raw"):
    documents = []
    
    if not os.path.exists(raw_dir):
        return documents
        
    for filename in os.listdir(raw_dir):
        # Buscamos por arquivos .pdf
        if filename.endswith(".pdf"):
            filepath = os.path.join(raw_dir, filename)
            
            # Usando PyPDFLoader para extrair o texto de cada página
            loader = PyPDFLoader(filepath)
            pages = loader.load()
            
            # Adicionando o conteúdo de cada página como um documento separado
            for page in pages:
                page.metadata["source"] = filename
                documents.append(page)
                
    return documents

# Bloco de teste
if __name__ == "__main__":
    docs = load_car_documents()
    print(f"Sucesso! Foram carregados {len(docs)} documentos.")
    for doc in docs:
        print(f"Arquivo: {doc.metadata['source']}")