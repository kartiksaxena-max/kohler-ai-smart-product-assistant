import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.ai import ask_ai
from app.catalog import find_products, load_catalog
from app.planner import plan_bathroom
from app.troubleshooting import diagnose
from app.tickets import create_ticket
from app.vision import identify_product, extract_bill
from app.voice import transcribe_audio

st.set_page_config(
    page_title="KOHLER AI Smart Product Assistant",
    page_icon="🚽",
    layout="wide",
)

st.markdown("""
<style>
.block-container{max-width:1250px;padding-top:1rem}
.hero{padding:.5rem 0 1rem}
.card{border:1px solid #e4e7ec;border-radius:16px;padding:18px;min-height:115px;background:#fff}
.small{color:#667085;font-size:.9rem}
.stButton>button{border-radius:10px}
</style>
""", unsafe_allow_html=True)

# ---------- session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "scanner_result" not in st.session_state:
    st.session_state.scanner_result = None
if "bill_result" not in st.session_state:
    st.session_state.bill_result = None
if "page" not in st.session_state:
    st.session_state.page = "💬 AI Chat"
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def go_to(page, question=None):
    st.session_state.page = page
    st.session_state.pending_question = question
    st.rerun()


def run_chat_question(question):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("KOHLER AI is thinking locally…"):
            result = ask_ai(question, st.session_state.messages[:-1])
        if result.get("ok"):
            answer = result.get("answer", "")
            st.markdown(answer)
            confidence = float(result.get("confidence", 0))
            st.caption(f"Intent: {result.get('intent','General Product Support')} · Knowledge relevance: {confidence:.0%}")
            sources = result.get("sources", [])
            if sources:
                with st.expander("📚 Knowledge sources"):
                    for source in sources:
                        if isinstance(source, dict):
                            st.write(f"📄 {source.get('filename','KOHLER knowledge base')} · relevance {source.get('score','N/A')}")
                        else:
                            st.write(f"📄 {source}")
        else:
            answer = result.get("answer", "The local AI could not generate a response.")
            st.error(answer)
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "intent": result.get("intent", "General Product Support"),
        "confidence": result.get("confidence", 0),
        "sources": result.get("sources", []),
    })


# ---------- sidebar ----------
with st.sidebar:
    st.title("🚽 KOHLER AI")
    st.caption("Smart Product Assistant • Advanced Demo")
    st.divider()

    st.subheader("What I can help with")
    help_items = [
        ("🔹 Product information", "What are the key features of KOHLER smart toilets?"),
        ("🔹 Smart toilet usage", "How does a KOHLER smart toilet work and how do I use its main functions?"),
        ("🔹 Installation guidance", "What should I check before installing a KOHLER smart toilet?"),
        ("🔹 Troubleshooting", "My KOHLER smart toilet is not flushing automatically. What should I check first?"),
        ("🔹 Care & maintenance", "How should I clean and maintain a KOHLER smart toilet?"),
        ("🔹 Warranty guidance", "What warranty information applies to KOHLER smart toilets and what should I verify?"),
        ("🔹 Product selection", "Help me choose a KOHLER smart toilet for a modern bathroom."),
        ("🔹 Bathroom planning", "Plan a modern 8 by 6 foot bathroom with a ₹2 lakh budget using KOHLER products."),
    ]
    for label, question in help_items:
        if st.button(label, key=f"help_{label}", use_container_width=True):
            go_to("💬 AI Chat", question)

    st.divider()
    st.subheader("Advanced tools")
    tool_items = [
        ("📷 Product Scanner", "📷 Product Scanner"),
        ("🧾 Bill Scanner", "🧾 Bill Scanner"),
        ("🎤 Voice Assistant", "🎤 Voice Assistant"),
        ("🧩 Product Finder", "🧩 Product Finder"),
        ("📐 Bathroom Planner", "📐 Bathroom Planner"),
        ("🔧 Troubleshooting", "🔧 Troubleshooting"),
        ("📖 Manual & Support", "📖 Manual & Support"),
    ]
    for label, target in tool_items:
        if st.button(label, key=f"tool_{label}", use_container_width=True):
            go_to(target)

    st.divider()
    st.caption("100% local/free AI demo: Ollama + Qwen2.5-VL. No OpenAI API key required.")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

page = st.session_state.page

st.title("KOHLER AI Smart Product Assistant")
st.caption("One assistant for product questions, identification, purchase documents, planning and support workflows.")

# ---------- AI CHAT ----------
if page == "💬 AI Chat":
    st.markdown("### Quick actions")
    cols = st.columns(4)
    quick = [
        ("🤖 Product info", "What are the key features of KOHLER smart toilets?"),
        ("🚽 Smart usage", "How does a KOHLER smart toilet work?"),
        ("🔧 Troubleshoot", "My KOHLER smart toilet is not flushing automatically. What should I check first?"),
        ("📐 Plan bathroom", "Plan a modern 8 by 6 foot bathroom with a ₹2 lakh budget using KOHLER products."),
    ]
    for col, (label, question) in zip(cols, quick):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.pending_question = question
                st.rerun()

    st.divider()

    for m in st.session_state.messages:
        with st.chat_message(m.get("role", "assistant")):
            st.markdown(m.get("content", ""))
            if m.get("role") == "assistant" and m.get("intent"):
                st.caption(f"Intent: {m.get('intent')} · Knowledge relevance: {float(m.get('confidence',0)):.0%}")

    pending = st.session_state.pending_question
    if pending:
        st.session_state.pending_question = None
        run_chat_question(pending)

    q = st.chat_input("Ask a KOHLER product question…")
    if q:
        run_chat_question(q)

# ---------- PRODUCT SCANNER ----------
elif page == "📷 Product Scanner":
    st.header("📷 Product Image Scanner")
    st.write("Upload a clear photo of a KOHLER product, control panel or model label.")
    f = st.file_uploader("Upload product image", type=["jpg", "jpeg", "png", "webp"])
    if f:
        st.image(f, width=420)
        if st.button("🔎 Analyze product", type="primary"):
            with st.spinner("Analyzing image with local vision AI…"):
                st.session_state.scanner_result = identify_product(f.getvalue(), f.type)
    r = st.session_state.scanner_result
    if r:
        if r.get("ok"):
            st.subheader("Identification result")
            st.json(r["data"])
            d = r["data"]
            model = d.get("likely_model") or d.get("visible_model_number")
            if model:
                st.success(f"Possible model/identifier: {model}")
            st.info("Verify the model number on the product label or official KOHLER support before purchasing parts or beginning repairs.")
        else:
            st.error(r.get("error", "Unable to analyze image."))

# ---------- BILL SCANNER ----------
elif page == "🧾 Bill Scanner":
    st.header("🧾 Bill / Invoice Scanner")
    st.write("Extract model numbers and purchase details from a bill or invoice using local vision AI.")
    f = st.file_uploader("Upload bill or invoice", type=["jpg", "jpeg", "png", "webp"])
    if f:
        st.image(f, width=650)
        if st.button("🧠 Extract bill details", type="primary"):
            with st.spinner("Reading invoice with local vision AI…"):
                st.session_state.bill_result = extract_bill(f.getvalue(), f.type)
    r = st.session_state.bill_result
    if r:
        if r.get("ok"):
            st.subheader("Extracted information")
            st.json(r["data"])
            st.download_button("⬇️ Download extracted JSON", json.dumps(r["data"], indent=2), file_name="kohler_bill_extraction.json", mime="application/json")
        else:
            st.error(r.get("error", "Unable to read bill."))

# ---------- VOICE ----------
elif page == "🎤 Voice Assistant":
    st.header("🎤 Voice Assistant")
    st.write("Upload a short recording. Local Whisper transcribes it and local KOHLER AI answers it.")
    f = st.file_uploader("Upload voice recording", type=["wav", "mp3", "m4a"])
    if f:
        st.audio(f)
        if st.button("🎙️ Transcribe & ask KOHLER AI", type="primary"):
            with st.spinner("Transcribing locally…"):
                tr = transcribe_audio(f.getvalue(), "." + f.name.split(".")[-1])
            if tr.get("ok"):
                st.success("Transcript")
                st.write(tr["text"])
                with st.spinner("Generating local AI answer…"):
                    r = ask_ai(tr["text"], st.session_state.messages)
                if r.get("ok"):
                    st.markdown(r["answer"])
                else:
                    st.error(r["answer"])
            else:
                st.error(tr.get("error", "Transcription failed."))

# ---------- PRODUCT FINDER ----------
elif page == "🧩 Product Finder":
    st.header("🧩 Product Finder")
    st.write("Search the included KOHLER demo catalog by product type, style and budget.")
    q = st.text_input("What are you looking for?", placeholder="e.g. smart toilet, modern, bidet")
    cat = st.selectbox("Category", ["All"] + sorted({p.get("category", "Other") for p in load_catalog()}))
    budget = st.number_input("Maximum budget (₹, optional)", min_value=0, value=0, step=500)
    results = find_products(q, budget if budget > 0 else None, cat)
    if not results:
        st.info("No local catalog match. Ask the AI for guidance or verify current availability/pricing on KOHLER.")
    for p in results:
        with st.container(border=True):
            st.subheader(p.get("name", "KOHLER product"))
            st.write(f"**Category:** {p.get('category','Other')} · **Style:** {p.get('style','Not specified')}")
            st.write("Features: " + ", ".join(p.get("features", [])))
            price = p.get("price_inr")
            st.write(f"**Price:** ₹{price:,}" if isinstance(price, (int, float)) else "**Price:** Verify current regional pricing")
            st.caption(p.get("source", "Verify official product details."))

# ---------- PLANNER ----------
elif page == "📐 Bathroom Planner":
    st.header("📐 Bathroom Planner & Product Bundle")
    st.write("Generate a concept bundle based on room size, budget and aesthetic theme.")
    c1, c2 = st.columns(2)
    length = c1.number_input("Bathroom length (cm)", min_value=100.0, value=240.0, step=10.0)
    width = c2.number_input("Bathroom width (cm)", min_value=100.0, value=180.0, step=10.0)
    budget = st.number_input("Target budget (₹, optional)", min_value=0, value=0, step=1000)
    theme = st.selectbox("Aesthetic theme", ["Modern", "Luxury", "Minimal"])
    if st.button("✨ Generate concept", type="primary"):
        plan = plan_bathroom(length, width, budget or None, theme)
        st.success(f"Room area: {plan['area_m2']} m²")
        st.info(plan['layout_note'])
        for p in plan['products']:
            price = p.get('price_inr')
            price_text = f"₹{price:,}" if isinstance(price, (int, float)) else "Price: verify current regional pricing"
            st.write(f"• **{p['name']}** — {', '.join(p.get('features', []))} — {price_text}")
        st.caption("Concept only. Verify exact clearances, plumbing, electrical requirements and current regional pricing against the selected model guide.")

# ---------- TROUBLESHOOTING ----------
elif page == "🔧 Troubleshooting":
    st.header("🔧 Guided Troubleshooting")
    model = st.text_input("Model number (if known)")
    issue = st.text_area("Describe the problem", placeholder="Example: The toilet is not responding to the remote.")
    if st.button("🩺 Diagnose", type="primary"):
        if not issue.strip():
            st.warning("Describe the problem first.")
        else:
            st.subheader("Safe first checks")
            for i, step in enumerate(diagnose(issue, model), 1):
                st.write(f"{i}. {step}")
            t = create_ticket(issue, model)
            st.success(f"Support ticket generated: {t['ticket_id']}")
            st.download_button("⬇️ Download ticket JSON", json.dumps(t, indent=2), file_name=f"{t['ticket_id']}.json", mime="application/json")

# ---------- MANUAL / SUPPORT ----------
elif page == "📖 Manual & Support":
    st.header("📖 Manual, Warranty & Support Finder")
    q = st.text_input("Search the knowledge base", placeholder="manual, warranty, model number, installation")
    if q:
        from app.rag import search_documents
        for result in search_documents(q, top_k=6):
            with st.expander(f"{result['filename']} · relevance {result['score']}"):
                st.write(result['content'])
    st.markdown("### Official resources")
    st.markdown("- [KOHLER Support](https://www.kohler.com/en/support/contact)\n- [KOHLER Assist](https://assist.kohler.com/en)\n- [Smart Toilets](https://www.kohler.com/en/products/smart-home/shop-smart-toilets)\n- [Smart Toilet Support](https://support.kohler.com/en/smart-toilets)\n- [Warranty](https://assist.kohler.com/en/warranty)")
    st.info("Exact model-specific manuals, compatibility, pricing and warranty eligibility should be verified using the official KOHLER resource for the customer’s region and model.")
