from app.rag import search_documents, detect_intent

def test_rag_finds_smart_toilet():
    results = search_documents("How do I use a KOHLER digital flush?")
    assert results
    assert any("smart_toilet" in r["filename"] for r in results)

def test_intent():
    assert detect_intent("How do I clean my KOHLER toilet?") == "Care & Maintenance"
