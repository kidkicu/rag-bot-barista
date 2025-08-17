import os, json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from rag import build_context
import tools
import google.generativeai as genai

load_dotenv()

# ---------- Gemini setup ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Put it in .env")

genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# System instruction helps keep answers consistent
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    system_instruction=(
        "You are Barista Bot. Be concise, friendly, and ALWAYS ground answers "
        "in provided context if available. If the user seems to be ordering, "
        "confirm size, milk, sweetness, and temperature. Offer ONE tasteful upsell."
    )
)

def _gchat(prompt: str) -> str:
    resp = model.generate_content(prompt)
    # Gemini may return None if blocked; guard:
    return (resp.text or "").strip()

SYSTEM_TOOLS = {
    "add_to_cart": tools.add_to_cart,
    "show_cart": tools.show_cart,
    "clear_cart": tools.clear_cart,
    "check_inventory": tools.check_inventory,
    "suggest_upsell": tools.suggest_upsell
}

def plan_tools(user_msg: str):
    """
    Light planner: ask Gemini to output a single JSON object with tool and args.
    """
    ctx, hits = build_context(user_msg, k=4)

    tool_hint = f"""
You may call at most one tool from:
- add_to_cart(item_id, name, qty, price)
- show_cart()
- clear_cart()
- check_inventory(item, need)
- suggest_upsell(base)

If the user explicitly asks to order/add/show/clear or to check stock, propose the ONE best tool call as JSON ONLY:
{{"tool":"NAME","args":{{...}}}}
If not needed, return {{}}

User: {user_msg}

Context:
{ctx}

JSON only:
"""
    raw = _gchat(tool_hint)
    try:
        plan = json.loads(raw) if raw.strip().startswith("{") else {}
    except Exception:
        plan = {}
    return plan, ctx

def run_agent(user_msg: str) -> Dict[str, Any]:
    plan, ctx = plan_tools(user_msg)
    tool_result = None

    # Execute the single selected tool, if any
    if isinstance(plan, dict) and plan.get("tool") in SYSTEM_TOOLS:
        fn = SYSTEM_TOOLS[plan["tool"]]
        args = plan.get("args", {}) or {}
        try:
            tool_result = fn(**args)
        except TypeError:
            tool_result = {"error": "bad args", "got": args}

    # Final grounded answer
    answer_prompt = f"""
Use the context and (if present) tool_result to answer.
- Be friendly, concise; if ordering, confirm size, milk, sweetness, temperature.
- Cite specific items/prices/allergens from context if asked.
- Offer ONE tasteful upsell when it makes sense.

User: {user_msg}

Context:
{ctx}

Tool result:
{tool_result}
"""
    answer = _gchat(answer_prompt)
    return {"answer": answer, "tool_result": tool_result}
