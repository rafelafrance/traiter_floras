"""List all of the matchers."""

import regex

from .plant_color import PLANT_COLOR
from .plant_count import PLANT_COUNT
from .plant_descriptor import PLANT_DESCRIPTOR
from .plant_shape import PLANT_SHAPE
from .plant_size import PLANT_SIZE
from ..pylib.util import FLAGS


MATCHERS = {
    PLANT_COLOR: """caylx_color corolla_color flower_color hypanthium_color
        petal_color sepal_color """.split(),

    PLANT_COUNT: """""".split(),

    PLANT_DESCRIPTOR: """ sexual_descriptor symmetry_descriptor """.split(),

    PLANT_SHAPE: """ caylx_shape corolla_shape flower_shape hypanthium_shape
        leaf_shape petal_shape petiole_shape sepal_shape """.split(),

    PLANT_SIZE: """ calyx_size corolla_size flower_size hypanthium_size
        leaf_size petal_size petiole_size seed_size sepal_size """.split(),
}

TRAITS = {t: k for k, v in MATCHERS.items() for t in v}


def all_traits():
    """Return a list of all traits."""
    return sorted(t for t in TRAITS.keys())


def expand_traits(args):
    """Expand traits using wildcards in given as arguments."""
    traits = set()
    for trait in args.trait:
        pattern = trait.replace('*', '.*').replace('?', '.?')
        pattern = regex.compile(pattern, regex.IGNORECASE)
        hits = {t for t in all_traits() if pattern.search(t)}
        traits |= hits
    return sorted(traits)


ALL = ['sexual_descriptor', 'symmetry_descriptor']
CALYX = ['calyx_size', 'caylx_shape', 'caylx_color']
COROLLA = ['corolla_size', 'corolla_shape', 'corolla_color']
FLOWER = ['flower_shape', 'flower_size', 'flower_color']
HYPANTHIUM = ['hypanthium_shape', 'hypanthium_size', 'hypanthium_color']
LEAF = ['leaf_size', 'leaf_shape']
PETAL = ['petal_size', 'petal_shape', 'petal_color']
PETIOLE = ['petiole_size', 'petiole_shape']
SEED = ['seed_size']
SEPAL = ['sepal_size', 'sepal_shape', 'sepal_color']


# Keywords used to split treatment into text atoms
ATOMS = {
    r'2n': [],
    'anther heads': [],
    'asexual structures': [],
    'basal leaves': (LEAF + PETIOLE),
    'basal rosettes': [],
    'calyptra': [],
    'capsule': [],
    'capsules': [],
    'caudices': [],
    'cauline leaves': (LEAF + PETIOLE),
    'corollas': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowering stems': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'flowers': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'fruiting peduncles': [],
    'fruits': [],
    'herbs': [],
    'hypanthia': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'inflorescences': [],
    'inflorescenses': [],
    'leaf blades': (LEAF + PETIOLE),
    'leaflets': (LEAF + PETIOLE),
    'leaves': (LEAF + PETIOLE),
    'pedicels': [],
    'peduncles': [],
    'pepos': [],
    'petals': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'petioles': (LEAF + PETIOLE),
    'pistillate flowers': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'pistillate': [],
    'plants': [],
    'pollen': [],
    'protonematal flaps': [],
    'racemes': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'seeds': SEED,
    'seta': [],
    'seta superficial cells': [],
    'sexual condition': [],
    'specialized asexual structures': [],
    'spores': [],
    'staminate corollas': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate flowers': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate inflorescences': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'staminate racemes': (
            FLOWER + HYPANTHIUM + SEPAL + PETAL + CALYX + COROLLA),
    'stem leaves': [],
    'stems': [],
    'stolon leaves': [],
    'stolons': [],
    'tendrils': [],
    'thallose protonematal flaps': [],
    'vines': [],
    'x': [],
}

ATOMS = {k: v for k, v in sorted(
    ATOMS.items(), reverse=True, key=lambda x: len(x[0]))}

ATOMIZER = ' | '.join(
    r' \s+ '.join(x.split()) for x in ATOMS.keys())
ATOMIZER = regex.compile(
    rf"""
        (?<! [\w:;,<>()] \s ) (?<! [\w:;,<>()] )
        \b ( {ATOMIZER} ) \b
        """,
    flags=FLAGS)