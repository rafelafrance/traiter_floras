"""Misc. utils."""

from datetime import datetime
from pathlib import Path

BASE_DIR = Path('.').resolve().parts[-1]
BASE_DIR = Path('.') if BASE_DIR.find('efloras') > -1 else Path('..')

DATA_DIR = BASE_DIR / 'data'
VOCAB_DIR = BASE_DIR / 'efloras' / 'vocabulary'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
ATTACH_STEP = 'attach'
STEPS2ATTACH = {TRAIT_STEP, ATTACH_STEP}

CONVERT = {
    'cm': 10.0,
    'dm': 100.0,
    'm': 1000.0,
    'mm': 1.0,
    'µm': 1.0e-3,
}


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)


def log(msg):
    """Log a status message."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'{now} {msg}'
    print(msg)
