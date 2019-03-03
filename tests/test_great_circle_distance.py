from jsonschema import ValidationError
from unittest2 import TestCase

from src.great_circle_distance import GreatCircleDistance


class GreatCircleDistanceTestCase(TestCase):

    def test_with_invalid_input(self):

        with self.assertRaises(ValidationError):
            GreatCircleDistance.calculate({}, {}, 100)

    def test_distance_is_correctly_calculated(self):

        point_1 = {
            "latitude": 53.339428,
            "longitude": -6.257664
        }

        point_2 = {
            "latitude": 53.2451022,
            "longitude": -6.238335
        }

        distance = GreatCircleDistance.calculate(point_1, point_2)

        self.assertAlmostEqual(distance, 10.57, 2)
