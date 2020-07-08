"""Test plant size trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from efloras.pylib.pipeline import parse


class TestSize(unittest.TestCase):
    """Test plant size trait parsers."""

    def test_size_01(self):
        self.assertEqual(
            parse('Leaf (12-)23-34 × 45-56 cm'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_size': [
                 {'start': 5, 'end': 26, 'length_min': 12.0,
                  'length_low': 23.0, 'length_high': 34.0, 'width_low': 45.0,
                  'width_high': 56.0, 'width_units': 'cm'}]}
        )

    def test_size_02(self):
        self.assertEqual(
            parse('leaf (12-)23-34 × 45-56'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 4}]}
        )

    def test_size_03(self):
        self.assertEqual(
            parse('blade 1.5–5(–7) cm'),
            {'part': [{'start': 0, 'end': 5, 'part': 'leaf'}],
             'leaf_size': [
                 {'start': 6, 'end': 18, 'length_low': 1.5,
                  'length_high': 5.0, 'length_max': 7.0,
                  'length_units': 'cm'}]}
        )

    def test_size_04(self):
        self.assertEqual(
            parse('leaf shallowly to deeply 5–7-lobed'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_lobe_count': [
                 {'start': 25, 'end': 34, 'low': 5, 'high': 7}]}
        )

    def test_size_05(self):
        self.assertEqual(
            parse('leaf 4–10 cm wide'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_size': [
                 {'start': 5, 'end': 17, 'width_low': 4.0,
                  'width_high': 10.0, 'width_units': 'cm'}]}
        )

    def test_size_06(self):
        self.assertEqual(
            parse('leaf sinuses 1/5–1/4 to base'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'subpart': [{'subpart': 'sinus', 'start': 5, 'end': 12},
                         {'subpart': 'base', 'start': 24, 'end': 28}]}
        )

    def test_size_07(self):
        self.assertEqual(
            parse('petiolules 2–5 mm'),
            {'part': [{'start': 0, 'end': 10, 'part': 'petiole'}],
             'petiole_size': [
                 {'start': 11, 'end': 17, 'length_low': 2.0,
                  'length_high': 5.0, 'length_units': 'mm'}]}
        )

    def test_size_08(self):
        self.assertEqual(
            parse('petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            {'part': [{'start': 0, 'end': 10, 'part': 'petiole'},
                      {'start': 37, 'end': 45, 'part': 'petiole'}],
             'petiole_size': [
                 {'start': 11, 'end': 17, 'length_low': 2.0,
                  'length_high': 5.0, 'length_units': 'mm'},
                 {'start': 46, 'end': 54, 'length_low': 16.0,
                  'length_high': 28.0, 'length_units': 'mm'}],
             'petiole_margin_shape': [
                 {'start': 19, 'end': 35, 'margin_shape': 'serrate'}]}
        )

    def test_size_09(self):
        self.assertEqual(
            parse('Leaves: petiole 2–15 cm;'),
            {'part': [{'start': 0, 'end': 6, 'part': 'leaf'},
                      {'start': 8, 'end': 15, 'part': 'petiole'}],
             'petiole_size': [
                 {'start': 16, 'end': 23, 'length_low': 2.0,
                  'length_high': 15.0, 'length_units': 'cm'}]}
        )

    def test_size_10(self):
        self.assertEqual(
            parse('petiole [5–]7–25[–32] mm, glabrous,'),
            {'part': [{'start': 0, 'end': 7, 'part': 'petiole'}],
             'petiole_size': [{'start': 8, 'end': 24,
                               'length_min': 5.0, 'length_low': 7.0,
                               'length_high': 25.0, 'length_max': 32.0,
                               'length_units': 'mm'}]}
        )

    def test_size_11(self):
        self.assertEqual(
            parse('leaf 2–4 cm × 2–10 mm'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_size': [
                 {'start': 5, 'end': 21, 'length_low': 2.0, 'length_high': 4.0,
                  'length_units': 'cm', 'width_low': 2.0, 'width_high': 10.0,
                  'width_units': 'mm'}]}
        )

    def test_size_12(self):
        self.assertEqual(
            parse('leaf deeply to shallowly lobed, 4–5(–7) cm wide,'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_size': [{'start': 32, 'end': 47,
                            'width_low': 4.0, 'width_high': 5.0,
                            'width_max': 7.0, 'width_units': 'cm'}]}
        )

    def test_size_13(self):
        self.assertEqual(
            parse(
                'Leaves 3-foliolate, lateral pair of leaflets '
                'deeply lobed, petiolules 2–5 mm,'),
            {'part': [{'part': 'leaf', 'start': 0, 'end': 6},
                      {'location': 'lateral', 'group': 'pair',
                       'part': 'leaflet', 'start': 20, 'end': 44},
                      {'part': 'petiole', 'location': 'lateral', 'start': 59,
                       'end': 69}],
             'leaf_count': [{'low': 3, 'start': 7, 'end': 18}],
             'petiole_size': [{'length_low': 2, 'length_high': 5,
                               'length_units': 'mm', 'location': 'lateral',
                               'start': 70, 'end': 76}]}
        )

    def test_size_14(self):
        self.assertEqual(
            parse('terminal leaflet 3–5 cm, blade petiolule 3–12 mm,'),
            {'part': [{'start': 0, 'end': 16, 'location': 'terminal',
                       'part': 'leaflet'},
                      {'location': 'terminal', 'start': 25, 'end': 30,
                       'part': 'leaf'},
                      {'location': 'terminal', 'start': 31, 'end': 40,
                       'part': 'petiole'}],
             'leaflet_size': [
                 {'location': 'terminal', 'start': 17, 'end': 23,
                  'length_low': 3.0, 'length_high': 5.0,
                  'length_units': 'cm'}],
             'petiole_size': [{'location': 'terminal', 'start': 41, 'end': 48,
                               'length_low': 3.0, 'length_high': 12.0,
                               'length_units': 'mm'}]}

        )

    def test_size_15(self):
        self.assertEqual(
            parse('leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,'),
            {'part': [{'start': 0, 'end': 4, 'part': 'leaf'}],
             'leaf_lobe_count': [
                 {'start': 15, 'end': 28, 'low': 3, 'high': 5, 'max': 7}],
             'leaf_size': [{'start': 30, 'end': 54,
                            'length_low': 5, 'length_high': 25,
                            'width_min': 8, 'width_low': 10,
                            'width_high': 25, 'width_max': 30,
                            'width_units': 'cm'}]}
        )

    def test_size_16(self):
        self.assertEqual(
            parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            {'plant_lobe_count': [{'start': 0, 'end': 11, 'min': 3, 'low': 5}],
             'plant_size': [{'start': 13, 'end': 32,
                             'length_low': 6, 'length_high': 20,
                             'length_max': 30, 'width_low': 6,
                             'width_high': 25, 'width_units': 'cm'}]}
        )

    def test_size_17(self):
        self.assertEqual(
            parse('petiole to 11 cm;'),
            {'part': [{'start': 0, 'end': 7, 'part': 'petiole'}],
             'petiole_size': [{'start': 8, 'end': 16,
                               'length_high': 11.0,
                               'length_units': 'cm'}]}
        )

    def test_size_18(self):
        self.assertEqual(
            parse(
                'petals (1–)3–10(–12) mm (pistillate) '
                'or 5–8(–10) mm (staminate)'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_size': [{'start': 7, 'end': 36,
                             'length_min': 1.0, 'length_low': 3.0,
                             'length_high': 10.0, 'length_max': 12.0,
                             'length_units': 'mm',
                             'sex': 'pistillate'},
                            {'start': 40, 'end': 63,
                             'length_low': 5.0, 'length_high': 8.0,
                             'length_max': 10.0, 'length_units': 'mm',
                             'sex': 'staminate'}]}
        )

    def test_size_19(self):
        self.assertEqual(
            parse('Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            {'part': [{'start': 0, 'end': 7, 'part': 'flower'},
                      {'start': 23, 'end': 33, 'part': 'hypanthium'}],
             'flower_size': [{'start': 8, 'end': 20,
                              'diameter_low': 5.0, 'diameter_high': 10.0,
                              'diameter_units': 'cm'}],
             'hypanthium_size': [{'start': 34, 'end': 40,
                                  'length_low': 4.0, 'length_high': 8.0,
                                  'length_units': 'mm'}]}
        )

    def test_size_20(self):
        self.assertEqual(
            parse('Flowers 5--16 × 4--12 cm'),
            {'part': [{'start': 0, 'end': 7, 'part': 'flower'}],
             'flower_size': [{'start': 8, 'end': 24,
                              'length_low': 5.0, 'length_high': 16.0,
                              'width_low': 4.0, 'width_high': 12.0,
                              'width_units': 'cm'}]}
        )

    def test_size_21(self):
        self.assertEqual(
            parse(
                'Inflorescences formed season before flowering and exposed '
                'during winter; staminate catkins in 1 or more clusters '
                'of 2--5, 3--8.5 cm,'),
            {'part': [{'start': 0, 'end': 14, 'part': 'inflorescence'}],
             'inflorescence_count': [{'start': 94, 'end': 95, 'low': 1},
                                     {'start': 116, 'end': 120, 'low': 2,
                                      'high': 5}],
             'inflorescence_size': [{'start': 122, 'end': 131,
                                     'length_low': 3.0, 'length_high': 8.5,
                                     'length_units': 'cm'}]}
        )

    def test_size_22(self):
        self.assertEqual(
            parse('Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,'),
            {'part': [{'start': 0, 'end': 8, 'part': 'leaflet'},
                      {'start': 22, 'end': 27, 'part': 'leaf'}],
             'leaf_shape': [{'shape': 'ovate', 'start': 28, 'end': 33}],
             'leaf_size': [{'start': 35, 'end': 49,
                            'length_low': 8.0, 'length_high': 15.0,
                            'width_low': 4.0, 'width_high': 15.0,
                            'width_units': 'cm'}]}
        )

    def test_size_23(self):
        self.assertEqual(
            parse('calyx, 8-10 mm, 3-4 mm high,'),
            {'part': [{'start': 0, 'end': 5, 'part': 'calyx'}],
             'calyx_size': [{'start': 7, 'end': 14,
                             'length_low': 8.0,
                             'length_high': 10.0,
                             'length_units': 'mm'},
                            {'start': 16, 'end': 27,
                             'height_low': 3.0,
                             'height_high': 4.0,
                             'height_units': 'mm'}]}
        )

    def test_size_24(self):
        self.assertEqual(
            parse('Petals 15-21 × ca. 8 mm,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_size': [{'start': 7, 'end': 23,
                             'length_low': 15, 'length_high': 21,
                             'width_low': 8, 'width_units': 'mm'}]}
        )

    def test_size_25(self):
        self.assertEqual(
            parse('Petals ca. 8 mm,'),
            {'part': [{'start': 0, 'end': 6, 'part': 'petal'}],
             'petal_size': [{'start': 7, 'end': 15,
                             'length_low': 8.0, 'length_units': 'mm'}]}
        )

    def test_size_26(self):
        self.assertEqual(
            parse('Legumes 7-10 mm, 2.8-4.5 mm high and wide'),
            {'part': [{'start': 0, 'end': 7, 'part': 'legume'}],
             'legume_size': [
                 {'start': 8, 'end': 15, 'length_low': 7.0,
                  'length_high': 10.0, 'length_units': 'mm'},
                 {'start': 17, 'end': 41,
                  'height_low': 2.8, 'height_high': 4.5, 'height_units': 'mm',
                  'width_low': 2.8, 'width_high': 4.5, 'width_units': 'mm'}]}
        )

    def test_size_27(self):
        self.assertEqual(
            parse('Ra­cemes 3-4 cm,'),
            {'part': [{'start': 0, 'end': 8, 'part': 'inflorescence'}],
             'inflorescence_size': [{'start': 9, 'end': 15, 'length_low': 3,
                                     'length_high': 4, 'length_units': 'cm'}]}
        )

    def test_size_28(self):
        self.assertEqual(
            parse('Petals pale violet, with darker keel; standard '
                  'elliptic, 6-7 × 3-4;'),
            {'part': [{'part': 'petal', 'start': 0, 'end': 6}],
             'petal_color': [{'color': 'purple', 'start': 12, 'end': 18}],
             'subpart': [{'subpart': 'keel', 'start': 32, 'end': 36}],
             'petal_keel_shape': [
                 {'shape': 'elliptic', 'start': 47, 'end': 55}]}
        )

    def test_size_29(self):
        self.assertEqual(
            parse('Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm.'),
            {'part': [{'part': 'seed', 'start': 0, 'end': 5}],
             'seed_size': [{'length_low': 1.6,
                            'width_low': 1.0, 'width_high': 1.3,
                            'thickness_low': 0.7, 'thickness_high': 0.8,
                            'thickness_units': 'cm',
                            'start': 6, 'end': 34}],
             'subpart': [{'subpart': 'hilum', 'start': 36, 'end': 41}],
             'seed_hilum_size': [{'length_low': 8, 'length_high': 10,
                                  'length_units': 'mm',
                                  'start': 42, 'end': 49}]}
        )

    def test_size_30(self):
        self.assertEqual(
            parse('leaflets obovate, 1-2.5 × to 1.6 cm,'),
            {'part': [{'part': 'leaflet', 'start': 0, 'end': 8}],
             'leaflet_shape': [{'shape': 'obovate', 'start': 9, 'end': 16}],
             'leaflet_size': [{'length_low': 1.0, 'length_high': 2.5,
                               'width_low': 1.6, 'width_units': 'cm',
                               'start': 18, 'end': 35}]}
        )

    def test_size_31(self):
        self.assertEqual(
            parse('Shrubs, 0.5–1[–2.5] m.'),
            {'plant_habit': [{'habit': 'shrub', 'start': 0, 'end': 6}],
             'plant_size': [{'length_low': 0.5, 'length_high': 1.0,
                             'length_max': 2.5, 'length_units': 'm',
                             'start': 8, 'end': 22}]}
        )
