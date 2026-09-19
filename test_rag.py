from app.rag import search_documents

results = search_documents("How do I use a KOHLER digital flush?")
print("\nSEARCH RESULTS\n")
for result in results:
    print("Document:", result["filename"])
    print("Score:", result["score"])
    print()
