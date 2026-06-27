from assistente_rag_lexml.data_ingestion import load_car_documents
from assistente_rag_lexml.vector_store import create_or_load_vector_store

def main():
    print("🚀 Iniciando o Assistente TrilhaCAR...")

    # 1. Carregar documentos (usando nossa nova função)
    print("📂 Carregando documentos da base ambiental...")
    docs = load_car_documents("data/raw")
    
    if not docs:
        print("⚠️ Nenhum documento PDF encontrado. Verifique a pasta data/raw.")
        return

    # 2. Carregar banco vetorial existente (o que treinamos no passo anterior)
    print("🧠 Carregando índice treinado...")
    vector_store = create_or_load_vector_store(index_path="models/faiss_index")
    
    # 3. Teste de consulta sobre o CAR
    query = "qual a metragem de proteção para um rio?"
    results = vector_store.similarity_search(query, k=1)
    
    print(f"\n✅ Sistema pronto!")
    print(f"Pergunta: {query}")
    print(f"Fonte encontrada: {results[0].metadata.get('source')}")
    print(f"Trecho relevante: {results[0].page_content[:200]}...")

if __name__ == "__main__":
    main()