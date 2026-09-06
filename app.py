import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from src.config import DATA_DIR, validate_config
from src.ingestion import build_index, load_index
from src.qa import KnowledgeAssistant
from src.memory import SessionMemory

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

BILLING_URL = "https://platform.openai.com/settings/organization/billing/"


def format_api_error(prefix: str, error: Exception) -> str:
    """Return an actionable message for common OpenAI API failures."""
    error_text = str(error)

    def contains_quota_error(value) -> bool:
        if isinstance(value, dict):
            return any(contains_quota_error(item) for item in value.values())
        if isinstance(value, (list, tuple)):
            return any(contains_quota_error(item) for item in value)
        return any(
            phrase in str(value).lower()
            for phrase in ("insufficient_quota", "credit_balance_exhausted")
        )

    quota_exhausted = contains_quota_error(error_text)
    for attribute in ("code", "body", "response", "message"):
        if contains_quota_error(getattr(error, attribute, None)):
            quota_exhausted = True
            break

    if quota_exhausted:
        return (
            f"{prefix}: insufficient_quota. OpenAI API credits are exhausted. "
            f"Add credits to continue: {BILLING_URL}"
        )

    return f"{prefix}: {error_text}"


st.title("📚 Enterprise Knowledge Assistant")
st.caption("Advanced RAG: FAISS + BM25 Hybrid Search + Reranking + Conversation Memory")

try:
    validate_config()
except Exception as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "assistant" not in st.session_state:
    st.session_state.assistant = None

with st.sidebar:
    st.header("Knowledge Base")

    files = [
        p.name for p in sorted(DATA_DIR.iterdir())
        if p.is_file() and p.suffix.lower() in {".txt", ".pdf", ".docx"}
    ] if DATA_DIR.exists() else []

    st.write(f"Documents in `data/`: **{len(files)}**")

    if files:
        with st.expander("Available documents"):
            for name in files:
                st.write(f"• {name}")

    if st.button("🔄 Build / Rebuild Index", use_container_width=True):
        with st.spinner("Loading, chunking, embedding and indexing documents..."):
            try:
                doc_count, chunk_count = build_index(DATA_DIR)
                st.session_state.assistant = KnowledgeAssistant(load_index())
                st.success(
                    f"Indexed {doc_count} documents into {chunk_count} chunks."
                )
            except Exception as e:
                st.error(format_api_error("Indexing failed", e))

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.info(
        "Supported files: TXT, PDF, DOCX\n\n"
        "Pipeline: Vector Search + BM25 → Hybrid RRF → Semantic Reranking → LLM"
    )

# Try loading an existing index automatically.
if st.session_state.assistant is None:
    try:
        st.session_state.assistant = KnowledgeAssistant(load_index())
    except Exception:
        pass

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📄 Sources used"):
                for source in message["sources"]:
                    st.write(f"• {source}")

query = st.chat_input("Ask a question about company policies...")

if query:
    if st.session_state.assistant is None:
        st.error("No knowledge base index is available. Build the index first.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    history = st.session_state.messages[:-1]

    with st.chat_message("assistant"):
        with st.spinner("Searching company knowledge..."):
            try:
                memory = SessionMemory(st.session_state.messages)
                response = st.session_state.assistant.ask(
                    query,
                    memory.get()
                )
                st.markdown(response.answer)

                with st.expander("📄 Sources used"):
                    for source in response.sources:
                        st.write(f"• {source}")

                with st.expander("🔎 Retrieved / reranked context"):
                    for i, chunk in enumerate(response.retrieved_chunks, 1):
                        st.markdown(
                            f"**{i}. {chunk.source}** — "
                            f"{chunk.retrieval_method} — "
                            f"score: {chunk.score:.4f}"
                        )
                        st.caption(chunk.text[:700])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.answer,
                    "sources": response.sources,
                })

            except Exception as e:
                st.error(format_api_error("Unable to answer the question", e))
