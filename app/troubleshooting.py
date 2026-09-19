from app.tickets import create_ticket

def diagnose(symptom, model=''):
    q = (symptom or '').lower()
    steps = []
    if any(x in q for x in ['no power','not turning on','dead','display off']):
        steps = ['Check whether the product is receiving power.', 'If the model requires an electrical outlet, verify the outlet/circuit safely.', 'Do not open electrical components; use the model manual or KOHLER support if the issue remains.']
    elif any(x in q for x in ['flush','not flushing','flush does not']):
        steps = ['Check whether the water supply is available.', 'Try the model’s documented manual flush/control method if provided.', 'If the issue continues, identify the exact model and consult the model-specific troubleshooting guide.']
    elif any(x in q for x in ['leak','water leaking']):
        steps = ['Stop using the product if continued use could worsen the leak.', 'Check visible connections without disassembling components.', 'For persistent leaks, contact KOHLER support or a qualified professional.']
    else:
        steps = ['Tell me the exact symptom and model number if available.', 'Share a clear photo of the product/control panel or error indicator.', 'Use KOHLER official support for model-specific repair instructions.']
    return steps
