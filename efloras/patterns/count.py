"""Common count snippets."""

import re

import spacy
from traiter.const import CROSS, FLOAT_RE, INT_TOKEN_RE, SLASH
from traiter.matcher_compiler import MatcherCompiler
from traiter.pipe_util import REJECT_MATCH, RejectMatch
from traiter.util import to_positive_int

from ..pylib.const import COMMON_PATTERNS, REPLACE

NOT_COUNT_WORDS = CROSS + SLASH + """ average side times days weeks by """.split()
NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()

COMPILE = MatcherCompiler(COMMON_PATTERNS | {
    'adp': {'POS': {'IN': ['ADP']}},
    'count_suffix': {'ENT_TYPE': 'count_suffix'},
    'count_word': {'ENT_TYPE': 'count_word'},
    'not_count_ent': {'ENT_TYPE': {'IN': NOT_COUNT_ENTS}},
    'not_count_word': {'LOWER': {'IN': NOT_COUNT_WORDS}},
    'per_count': {'ENT_TYPE': 'per_count'},
})

COUNT = [
    {
        'label': 'count',
        'on_match': 'count.v1',
        'patterns': COMPILE(
            '99-99 -? per_count?',
            '99-99 per_count count_suffix?',
            'per_count adp? 99-99 count_suffix?',
            '( 99-99 count_suffix? ) per_count',
        ),
    },
    {
        'label': 'count_word',
        'on_match': 'count_word.v1',
        'patterns': COMPILE(
            'count_word',
        )
    },
    {
        'label': '_not_a_count',
        'on_match': REJECT_MATCH,
        'patterns': COMPILE(
            '99-99 not_count_ent',
            '99-99 not_count_word 99-99? not_count_ent?',
            '9 / 9',
        ),
    },
]


@spacy.registry.misc(COUNT[0]['on_match'])
def count(ent):
    """Enrich the match with data."""
    range_ = range_values(ent)

    if per_count_ := [e for e in ent.ents if e.label_ == 'per_count']:
        per_count_ = per_count_[0].text.lower()
        range_._.data['group'] = REPLACE.get(per_count_, per_count_)


@spacy.registry.misc(COUNT[1]['on_match'])
def count_word(ent):
    """Enrich the match with data."""
    ent._.new_label = 'count'
    word = [e for e in ent.ents if e.label_ == 'count_word'][0]
    word._.data = {'low': to_positive_int(REPLACE[word.text])}
    word._.new_label = 'count'


def range_values(ent):
    """Extract values from the range and cached label."""
    data = {}
    range_ = [e for e in ent.ents if e._.cached_label.split('.')[0] == 'range'][0]

    values = re.findall(FLOAT_RE, range_.text)

    if not all([re.search(INT_TOKEN_RE, v) for v in values]):
        raise RejectMatch

    keys = range_.label_.split('.')[1:]
    for key, value in zip(keys, values):
        data[key] = to_positive_int(value)

    range_._.data = data
    range_._.new_label = 'count'
    return range_