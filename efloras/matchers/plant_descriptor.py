"""Common color snippets."""

from ..pylib.terms import TERMS


LABELS = ('seasonal', 'plant_sex', 'symmetry', 'temporal')


IS_DESCRIPTOR = {t['pattern'] for t in TERMS
                 if t['label'] in LABELS and t['category'] == 'descriptor'}


def descriptor(span):
    """Enrich a phrase match."""
    token = span[0]
    value = token.text.lower()
    label = token._.label
    if value not in IS_DESCRIPTOR:
        return {}
    return dict(
        value=value,
        category=label,
        start=span.start_char,
        end=span.end_char,
    )


PLANT_DESCRIPTOR = {
    'name': 'descriptor',
    'matchers': [
        {
            'label': 'descriptor',
            'on_match': descriptor,
            'patterns': [[
                {'_': {'label': {'IN': LABELS}}},
            ]],
        },
    ]
}
