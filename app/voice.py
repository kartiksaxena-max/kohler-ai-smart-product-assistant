import tempfile
from pathlib import Path
from app.logging_config import logger

def transcribe_audio(file_bytes, suffix='.wav'):
    """Free local voice transcription using faster-whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {'ok': False, 'text': '', 'error': 'Free voice mode needs faster-whisper. Run: pip install faster-whisper'}
    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(file_bytes); path = f.name
        model = WhisperModel('base', device='cpu', compute_type='int8')
        segments, _ = model.transcribe(path)
        text = ' '.join(segment.text.strip() for segment in segments).strip()
        if not text:
            return {'ok': False, 'text': '', 'error': 'No speech was detected. Please upload a clearer recording.'}
        return {'ok': True, 'text': text}
    except Exception as exc:
        logger.exception('Local transcription failed: %s', type(exc).__name__)
        return {'ok': False, 'text': '', 'error': 'Local voice transcription failed. WAV audio works most reliably.'}
    finally:
        if path:
            try: Path(path).unlink(missing_ok=True)
            except Exception: pass
