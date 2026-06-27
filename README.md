# Assistente RAG LexML

Este repositório contém a infraestrutura de engenharia de dados e o motor cognitivo RAG (Retrieval-Augmented Generation) desenvolvido para estruturar consultas inteligentes em documentos legislativos. O sistema utiliza Processamento de Linguagem Natural (NLP) e bancos de dados vetoriais para buscas semânticas de alta precisão.

---

## 🏗️ Arquitetura e Engenharia

A fundação do projeto segue padrões rigorosos de desenvolvimento e gestão de dados:

* **Gestão de Dependências:** Instalação e isolamento de ambiente otimizados com `uv` (Python 3.12).
* **Estruturação Modular:** Encapsulamento da lógica do motor RAG.
* **Data Pipeline:** Diretórios segmentados para o ciclo de vida dos dados (`data/raw`, `data/processed`, `models` e `notebooks`).
* **Motor Vetorial:** Indexação semântica validada com `FAISS` e embeddings do `HuggingFace` (`vector_store.py`).
* **Ingestão ETL:** Pipeline automatizado para extração e limpeza de textos a partir de documentos XML (`data_ingestion.py`).

---

## ✅ Status de Validação

**Última validação:** Junho de 2026
Infraestrutura homologada com sucesso:
* **Ingestão:** Processamento íntegro de arquivos XML mapeados em `data/raw`.
* **Indexação Vetorial:** Geração de índice FAISS com modelo `all-MiniLM-L6-v2`.
* **Busca Semântica:** Recuperação de contexto (retrieval) com alta precisão e relevância estrutural.

---

## ⚙️ Guia de Instalação e Configuração

Siga o fluxo abaixo utilizando o **Git Bash** (ou terminal equivalente).

**1. Clonar o repositório**
```bash
git clone [https://github.com/saimomgozn-collab/assistente-rag-hacarthon.git](https://github.com/saimomgozn-collab/assistente-rag-hacarthon.git)
cd assistente-rag-hacarthon
```

**2. Instalar o gestor de pacotes (`uv`)**
Via PowerShell (Windows):
```powershell
powershell -ExecutionPolicy Bypass -Command "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

**3. Sincronizar dependências**
```bash
uv sync
```

**4. Ativar o ambiente virtual**
```bash
.venv\Scripts\Activate.ps1
```

**5. Configurar variáveis de ambiente**
```bash
cp .env.example .env
```

---

## 👥 Equipe e Responsabilidades

O projeto é mantido por uma equipe enxuta e ágil:

| Membro | Foco de Atuação |
| :--- | :--- |
| **Saimom Goz Siebem** | Engenharia de Dados, Ingestão ETL (XML) e Arquitetura do RAG. |
| **Daniel Linhares** | Motor Cognitivo, Validação de Ambiente e Code Review. |

---

## 🚀 Guia de Colaboração (Git Flow)

Adotamos um fluxo de versionamento estruturado para garantir a integridade do código:

1. **Sync:** `git checkout main && git pull origin main`
2. **Branch:** `git checkout -b feat/nome-da-tarefa`
3. **Commit:** `git commit -m "feat: [descrição curta]"` (seguindo Conventional Commits).
4. **Push:** `git push origin feat/nome-da-tarefa`
5. **PR:** Abertura de Pull Request para revisão do par.

### Padrões de Ambiente

* **Execução:** Utilize sempre `uv run python [arquivo].py` para garantir o uso correto das dependências.
* **Dados Brutos:** Novos dumps devem ser alocados exclusivamente em `data/raw`.