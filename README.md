# KOHLER AI Smart Product Assistant — Free Local AI Edition

Advanced demo for the KOHLER-MITWPU AI Research Lab Program.

## What changed
This edition removes the paid OpenAI dependency. The AI runs locally through **Ollama** using the free/open Qwen2.5-VL 3B model. The same local model handles text chat, product-image analysis and bill/image extraction. Voice uses local `faster-whisper`.

Ollama serves a local API on `http://127.0.0.1:11434`, so the app does not need an OpenAI API key or paid API credits.

## Install Ollama
Install Ollama for Windows from the official site:
https://ollama.com/download/windows

Then open PowerShell and run:

```powershell
ollama pull qwen2.5vl:3b
```

The 3B vision model is about 3.2 GB. Keep Ollama running in the background.

## Run the project

```powershell
python -m pip install -r requirements.txt
.\venv\Scripts\Activate.ps1
streamlit run app/main.py
```

If the virtual environment already exists, activate it before installing/running.

## Environment
No OpenAI key is required. You may copy `.env.example` to `.env`, but the defaults already point to the local Ollama server:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5vl:3b
OLLAMA_VISION_MODEL=qwen2.5vl:3b
OLLAMA_TIMEOUT=180
```

## Voice
Voice transcription uses `faster-whisper` locally. The first use downloads the Whisper model and can take time. WAV is the most reliable upload format. No paid transcription API is used.

## Included
- Local AI customer/product support chat with RAG
- Local product image scanner
- Local bill/invoice extraction
- Local voice transcription + AI answer
- Product finder with local demo catalog
- Bathroom size planner and concept product bundle
- Guided troubleshooting
- Support-ticket generation
- Manual/support/warranty knowledge search
- Privacy page and backend logging

## Prototype boundaries
- The catalog is a demo knowledge/catalog layer, not live KOHLER inventory or live pricing.
- Image and bill extraction are AI-assisted and must be verified.
- Bathroom planning is a concept tool, not an engineering drawing.
- Troubleshooting intentionally avoids unsafe electrical/plumbing repair instructions.
- Exact product details vary by model and region.
