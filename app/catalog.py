from pathlib import Path
import json
from app.config import BASE_DIR

CATALOG_PATH = BASE_DIR / 'data' / 'products' / 'catalog.json'

def load_catalog():
    if not CATALOG_PATH.exists():
        return []
    try:
        return json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    except Exception:
        return []

def find_products(query='', budget=None, category='All'):
    products = load_catalog()
    q = (query or '').lower()
    out = []
    for p in products:
        if category != 'All' and p.get('category') != category:
            continue
        text = ' '.join(str(v) for v in p.values()).lower()
        score = sum(1 for token in q.split() if token in text)
        if budget is not None and p.get('price_inr') and p['price_inr'] <= budget:
            score += 2
        if not q and budget is None:
            score = 1
        if score > 0:
            out.append((score, p))
    out.sort(key=lambda x: (-x[0], x[1].get('price_inr') or 0))
    return [p for _, p in out]
