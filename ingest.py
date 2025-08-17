import json, glob, os
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "chroma_db"

def load_docs():
    docs=[]
    # markdown/text
    for path in glob.glob("data/*.md"):
        docs += TextLoader(path, encoding="utf-8").load()
    # menu.json -> text
    with open("data/menu.json","r",encoding="utf-8") as f:
        menu = json.load(f)
    menu_text = "\n".join([f"{m['name']}: ${m['price']} | tags={m.get('tags',[])} | allergens={m.get('allergens',[])}" for m in menu])
    docs.append(Document(page_content=menu_text, metadata={"source":"menu.json"}))
    return docs

def main():
    os.makedirs(DB_DIR, exist_ok=True)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(load_docs())
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(chunks, embed, persist_directory=DB_DIR)
    print("Built vector store at", DB_DIR)

if __name__=="__main__":
    main()
