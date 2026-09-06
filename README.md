# Enterprise Knowledge Assistant — Advanced RAG

A production-oriented employee knowledge assistant using local company documents.

## Features

- Local TXT, PDF and DOCX document ingestion
- Recursive chunking
- OpenAI embeddings
- Local FAISS vector database
- BM25 keyword retrieval
- Hybrid retrieval using Reciprocal Rank Fusion
- Semantic embedding-based reranking
- Conversational query rewriting and memory
- Grounded LLM answers
- Source citations
- Hallucination mitigation
- Streamlit chat UI
- Clear/reset conversation
- Retrieved-context inspection
- Basic error handling

## Project structure

enterprise_knowledge_assistant/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── Leave_Policy.txt
│   ├── IT_Policy.txt
│   ├── Travel_Policy.txt
│   ├── Employee_Handbook.txt
│   ├── Benefits.txt
│   └── Code_of_Conduct.txt
└── src/
    ├── config.py
    ├── document_loader.py
    ├── ingestion.py
    ├── retriever.py
    ├── reranker.py
    ├── memory.py
    ├── models.py
    └── qa.py

## Setup in VS Code — Windows

Open the project folder in VS Code.

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure API key

Copy `.env.example` to `.env` and add your OpenAI API key.

Example:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6-luna
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

If your account exposes a different model name, use that model name.

### 5. Run Streamlit

```powershell
streamlit run app.py
```

The browser will open the application.

## Using the application

1. Put your company TXT/PDF/DOCX files into `data/`.
2. Open the Streamlit app.
3. Click **Build / Rebuild Index**.
4. Ask questions.
5. Review the displayed source documents.
6. Open **Retrieved / reranked context** to inspect what was supplied to the LLM.
7. Use **Clear Conversation** to reset memory.

## Example questions

- What is the leave policy?
- What about carry-forward?
- How should I report a phishing message?
- What is required for business travel?
- Who should I contact about benefit eligibility?

## RAG pipeline

Documents
→ Loaders
→ Chunking
→ OpenAI Embeddings
→ FAISS

Query
→ Query Rewrite using conversation history
→ Vector Search
→ BM25 Search
→ Reciprocal Rank Fusion
→ Semantic Reranking
→ Relevant Context
→ Grounded LLM
→ Answer + Sources

## Hallucination handling

The system prompt explicitly instructs the LLM to:
- use only retrieved company-document context;
- avoid unsupported claims;
- say when information cannot be found;
- preserve conversation context for follow-up questions.

## Notes

The vector index is generated locally under `vector_store/` after indexing. The source documents remain local; only their text chunks are sent to the configured embedding/LLM API when processing questions.




# License

# This project is intended for POC  purposes and demonstrates enterprise-grade multimodal AI workflow design using Large Language Models.   By Sumeet Kumar 