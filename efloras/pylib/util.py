"""Holds misc functions and constants."""

from pathlib import Path

import inflect
import regex

FLAGS = regex.VERBOSE | regex.IGNORECASE

BATCH_SIZE = 1_000_000  # How many records to work with at a time

DATA_DIR = Path('.') / 'data'

INFLECT = inflect.engine()


class DotDict(dict):
    """Allow dot.notation access to dictionary items"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def shorten(text):
    """Collapse whitespace in a string."""
    return ' '.join(text.split())


def flatten(nested):
    """Flatten an arbitrarily nested list."""
    flat = []
    nested = nested if isinstance(nested, (list, tuple, set)) else [nested]
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def squash(values):
    """Squash a list to a single value if its length is one."""
    return values if len(values) != 1 else values.pop()


def as_list(values):
    """Convert values to a list."""
    return values if isinstance(values, (list, tuple, set)) else [values]


def as_tuple(values):
    """Convert values to a tuple."""
    return values if isinstance(values, tuple) else tuple(values)


def as_member(values):
    """Convert values to set members (hashable)."""
    return tuple(values) if isinstance(values, (list, set)) else values


def to_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.-]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_positive_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_int(value):
    """Convert value to an integer, handle 'no' or 'none' etc."""
    value = regex.sub(r'[^\d-]', '', value) if value else ''
    try:
        return int(value)
    except ValueError:
        return 0


def camel_to_snake(name):
    """Convert a camel case string to snake case."""
    split = regex.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return regex.sub('([a-z0-9])([A-Z])', r'\1_\2', split).lower()


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number):
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)
