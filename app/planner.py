from app.catalog import load_catalog


def plan_bathroom(length_cm, width_cm, budget=None, theme='Modern'):
    area = float(length_cm) * float(width_cm)
    candidates = []
    for p in load_catalog():
        price = p.get('price_inr')
        # Catalog prices may intentionally be unknown (None). Do not crash or
        # exclude such products when the user enters a budget; simply mark them
        # as "verify price" in the UI.
        if budget is not None and price is not None:
            try:
                if float(price) > float(budget):
                    continue
            except (TypeError, ValueError):
                pass
        candidates.append(p)

    def sort_key(p):
        style = str(p.get('style', ''))
        style_match = 0 if str(theme).lower() in style.lower() else 1
        price = p.get('price_inr')
        try:
            price_key = float(price) if price is not None else float('inf')
        except (TypeError, ValueError):
            price_key = float('inf')
        return (style_match, price_key)

    candidates.sort(key=sort_key)
    selected = candidates[:4]
    return {
        'area_cm2': round(area, 2),
        'area_m2': round(area / 10000, 2),
        'products': selected,
        'layout_note': 'Keep required plumbing/electrical clearances and verify the exact model installation guide before installation.'
    }
