# ☕ Barista Bot — RAG + Gemini

An AI-powered Barista Bot built with **Streamlit**, **Gemini API**, and **RAG (Retrieval Augmented Generation)**.  
The bot can:
- Show the café menu, ingredients, allergens, and prices.
- Take orders (cart system).
- Suggest upsells (e.g. pastries).
- Remember conversation history across sessions.

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/kidkicu/rag-bot-barista.git
cd rag-bot-barista
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # on Linux/Mac
.venv\Scripts\activate      # on Windows (PowerShell)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variable
```bash
GEMINI_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### 5. Build knowledge base
```bash
python ingest.py
```

### 6. run your app
```bash
streamlit run app.py
```

# 🧩 Example Usage
- "menu please" → shows drinks + prices.
- "what ingredients in oat latte" → grounded answer from recipes.md.
- "add 2 cappuccinos" → adds to cart.
- "show cart" → displays cart + total.

# 🛡️ Notes
- History is saved to chat_history.json (ignored in git).
- To reset history, use the sidebar Reset chat button.
- To add more items (like pastries), update data/menu.json and rerun python ingest.py.