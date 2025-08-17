from typing import List, Dict

_CART: List[Dict] = []
_INVENTORY = {"espresso": 1000, "milk": 100, "oat_milk": 60, "chocolate": 40}

def add_to_cart(item_id: str, name: str, qty: int, price: float):
    _CART.append({"item_id": item_id, "name": name, "qty": qty, "price": price})
    return {"ok": True, "cart": _CART, "total": sum(i["qty"]*i["price"] for i in _CART)}

def show_cart():
    return {"cart": _CART, "total": sum(i["qty"]*i["price"] for i in _CART)}

def clear_cart():
    _CART.clear()
    return {"ok": True}

def check_inventory(item:str, need:int=1):
    have = _INVENTORY.get(item,0)
    return {"item": item, "have": have, "enough": have>=need}

def suggest_upsell(base:str):
    if "mocha" in base.lower():
        return "Would you like a croissant or brownie to go with that?"
    return "Would you like to try our oat latte or add a flavor shot?"
