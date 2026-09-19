import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import BASE_DIR

DATA_FOLDER = BASE_DIR / "data"
SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md"}

def load_documents():
    documents = []
    if not DATA_FOLDER.exists():
        return documents
    for path in DATA_FOLDER.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if content.strip():
                documents.append({
                    "filename": path.name,
                    "path": str(path.relative_to(BASE_DIR)),
                    "content": content,
                })
    return documents

def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def search_documents(query, top_k=4):
    query = (query or "").strip()
    if not query:
        return []
    docs = load_documents()
    if not docs:
        return []
    texts = [d["content"] for d in docs]
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    qv = vectorizer.transform([query])
    tfidf = cosine_similarity(qv, matrix).flatten()
    qwords = set(_tokens(query))
    scores = []
    for i, doc in enumerate(docs):
        dwords = set(_tokens(doc["content"]))
        overlap = len(qwords & dwords) / max(len(qwords), 1)
        score = 0.65 * float(tfidf[i]) + 0.35 * overlap
        scores.append(score)
    ranked = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)
    results = []
    for i in ranked[:top_k]:
        results.append({
            "filename": docs[i]["filename"],
            "path": docs[i]["path"],
            "content": docs[i]["content"],
            "score": round(scores[i], 4),
        })
    return results

def detect_intent(question):
    q = (question or "").lower()
    if any(x in q for x in ["manual", "installation", "install", "setup"]):
        return "Installation / Manual"
    if any(x in q for x in ["clean", "care", "maintain", "maintenance"]):
        return "Care & Maintenance"
    if any(x in q for x in ["not working", "problem", "trouble", "error", "won't", "doesn't work"]):
        return "Troubleshooting"
    if any(x in q for x in ["warranty", "guarantee", "coverage"]):
        return "Warranty"
    if any(x in q for x in ["buy", "price", "shop", "where can i get"]):
        return "Product / Purchase"
    if any(x in q for x in ["how do i", "how does", "use", "activate", "flush"]):
        return "Product Usage"
    return "General Product Support"
