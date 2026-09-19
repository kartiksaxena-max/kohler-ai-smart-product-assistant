import base64
import json
import urllib.error
import urllib.request

from app.config import OLLAMA_BASE_URL, OLLAMA_VISION_MODEL, OLLAMA_TIMEOUT
from app.logging_config import logger

VISION_PROMPT = """You are a KOHLER product identification assistant. Analyze this uploaded image.
Return JSON only with keys: product_type, likely_model, visible_brand, visible_model_number,
visible_features, confidence, next_step. Never invent a model number. If uncertain, use null and
say what additional photo/label is needed."""

BILL_PROMPT = """Extract purchase information from this bill/invoice image. Return JSON only with keys:
merchant, invoice_number, invoice_date, customer_name, products (array of {description, model_number,
quantity, amount}), total, currency, raw_model_numbers. Do not guess missing values; use null or empty
arrays. This is a prototype extraction and must be verified by the customer."""

def _ollama_vision(prompt, file_bytes):
    payload = json.dumps({
        "model": OLLAMA_VISION_MODEL,
        "messages": [{"role": "user", "content": prompt,
                      "images": [base64.b64encode(file_bytes).decode("utf-8")]}],
        "stream": False, "format": "json", "options": {"temperature": 0.1},
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat", data=payload,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=OLLAMA_TIMEOUT) as response:
        data = json.loads(response.read().decode("utf-8"))
    text = data.get("message", {}).get("content", "").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)

def _call_vision(prompt, file_bytes):
    try:
        return {"ok": True, "data": _ollama_vision(prompt, file_bytes)}
    except urllib.error.URLError:
        return {"ok": False, "error": "The free local AI engine is not running. Start Ollama and make sure the vision model is installed."}
    except Exception as exc:
        logger.exception("Local vision request failed: %s", type(exc).__name__)
        return {"ok": False, "error": "Image analysis failed. Try a clearer image and make sure the local vision model is installed."}

def identify_product(file_bytes, mime="image/jpeg"):
    return _call_vision(VISION_PROMPT, file_bytes)

def extract_bill(file_bytes, mime="image/jpeg"):
    return _call_vision(BILL_PROMPT, file_bytes)
