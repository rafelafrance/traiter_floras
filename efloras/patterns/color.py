"""Common color snippets."""

import re

from spacy import registry
from traiter.const import DASH, DASH_CHAR
from traiter.patterns.matcher_patterns import MatcherPatterns

from efloras.pylib.const import COMMON_PATTERNS, MISSING, REMOVE, REPLACE

MULTIPLE_DASHES = ['\\' + c for c in DASH_CHAR]
MULTIPLE_DASHES = fr'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = DASH + MISSING

COLOR = MatcherPatterns(
    'color',
    on_match='efloras.color.v1',
    decoder=COMMON_PATTERNS | {
        'color_words': {'ENT_TYPE': {'IN': ['color', 'color_mod']}},
        'color': {'ENT_TYPE': 'color'},
    },
    patterns=[
        'missing? color_words* -* color+ -* color_words*',
    ],
)


@registry.misc(COLOR.on_match)
def color(ent):
    """Enrich a phrase match."""
    parts = {r: 1 for t in ent
             if (r := REPLACE.get(t.lower_, t.lower_)) not in SKIP
             and not REMOVE.get(t.lower_)}
    value = '-'.join(parts.keys())
    value = re.sub(MULTIPLE_DASHES, r'-', value)
    ent._.data['color'] = REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in MISSING):
        ent._.data['missing'] = True
