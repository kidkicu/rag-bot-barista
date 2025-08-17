import os, json, datetime as dt
import streamlit as st
from agent import run_agent

# -----------------------------
# Simple JSON persistence
# -----------------------------
HISTORY_FILE = "chat_history.json"

def _now():
    return dt.datetime.now().isoformat(timespec="seconds")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # sanity-check structure
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []  # empty history

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.toast(f"Failed to save history: {e}", icon="⚠️")

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Barista Bot", page_icon="☕")
st.title("☕ Barista Bot")

# Sidebar controls
with st.sidebar:
    st.markdown("### Chat controls")
    col_a, col_b = st.columns(2)
    if col_a.button("🗑️ Reset chat"):
        st.session_state.history = []
        save_history([])
        st.rerun()

    # Export history
    exported = json.dumps(load_history(), ensure_ascii=False, indent=2).encode("utf-8")
    col_b.download_button("⬇️ Export", exported, file_name="chat_history.json", mime="application/json")

    st.caption("History is saved to `chat_history.json` on the server.")

# Init state from disk
if "history" not in st.session_state:
    st.session_state.history = load_history()

# Replay chat
for msg in st.session_state.history:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    with st.chat_message(role):
        st.markdown(content)

# Input
user = st.chat_input("Ask about menu, allergens, or place an order…")
if user:
    # Append user message
    st.session_state.history.append({"role": "user", "content": user, "ts": _now()})
    save_history(st.session_state.history)

    # Get agent response
    with st.chat_message("assistant"):
        try:
            result = run_agent(user)
            answer = result.get("answer", "").strip() or "_(no response)_"
            st.markdown(answer)
            # Optional: show tool result for debugging
            if result.get("tool_result"):
                with st.expander("Tool result (debug)"):
                    st.json(result["tool_result"])
        except Exception as e:
            answer = f"Sorry, something went wrong: `{e}`"
            st.error(answer)

    # Append assistant message
    st.session_state.history.append({"role": "assistant", "content": answer, "ts": _now()})
    save_history(st.session_state.history)
