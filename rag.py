import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

DB_DIR="chroma_db"

_embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_vs = Chroma(persist_directory=DB_DIR, embedding_function=_embed)

def retrieve(query:str, k:int=4):
    docs = _vs.similarity_search(query, k=k)
    return [{"text": d.page_content, "source": d.metadata.get("source","unknown")} for d in docs]

def build_context(query:str, k:int=4):
    hits = retrieve(query, k)
    ctx = "\n\n".join([f"[{i+1}] {h['text']}" for i,h in enumerate(hits)])
    return ctx, hits
