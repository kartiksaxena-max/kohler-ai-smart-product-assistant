import json, uuid
from datetime import datetime
from app.config import BASE_DIR
from app.logging_config import logger

TICKET_FILE = BASE_DIR / 'data' / 'tickets.json'

def create_ticket(issue, model='', customer=''):
    TICKET_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(TICKET_FILE.read_text(encoding='utf-8')) if TICKET_FILE.exists() else []
    except Exception:
        data = []
    ticket = {'ticket_id': 'KAI-' + uuid.uuid4().hex[:8].upper(), 'created_at': datetime.now().isoformat(timespec='seconds'),
              'issue': issue, 'model': model or 'Unknown', 'customer': customer or 'Not provided', 'status': 'Open'}
    data.append(ticket)
    TICKET_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')
    logger.info('Support ticket created: %s', ticket['ticket_id'])
    return ticket
