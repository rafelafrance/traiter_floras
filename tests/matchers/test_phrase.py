"""Test matching literal phrases."""

# pylint: disable=missing-function-docstring

import unittest

from efloras.pylib.pipeline import parse


class TestPhrase(unittest.TestCase):
    """Test the plant descriptor trait parser."""

    def test_phrase_01(self):
        self.assertEqual(
            parse('Pistillate flowers  usually sessile; hypogynous'),
            {'part': [{'start': 0, 'end': 18,
                       'sex': 'female', 'part': 'flower'}],
             'flower_floral_location': [{'sex': 'female',
                                         'floral_location': 'superior',
                                         'start': 37, 'end': 47}]}
        )

    def test_phrase_02(self):
        self.assertEqual(
            parse('Petals glabrous, deciduous;'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_duration': [
                 {'start': 17, 'end': 26, 'duration': 'deciduous'}]}
        )

    def test_phrase_03(self):
        self.assertEqual(
            parse('leaf blade herbaceous.'),
            {'part': [{'start': 0, 'end': 10, 'part': 'leaf'}],
             'leaf_woodiness': [
                 {'woodiness': 'herbaceous', 'start': 11, 'end': 21}]}
        )
