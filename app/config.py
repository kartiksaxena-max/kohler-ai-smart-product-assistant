import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'
load_dotenv(ENV_FILE, override=True)

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434').strip().rstrip('/')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5vl:3b').strip() or 'qwen2.5vl:3b'
OLLAMA_VISION_MODEL = os.getenv('OLLAMA_VISION_MODEL', OLLAMA_MODEL).strip() or OLLAMA_MODEL
OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '180'))
MAX_UPLOAD_MB = 5
