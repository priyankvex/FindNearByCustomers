from unittest2 import TestCase

from src.nearby_customers import NearByCustomers


class NearByCustomersTestCase(TestCase):

    def test_nearby_customers_gives_correct_results(self):

        customers = [
            {"latitude": "51.92893", "user_id": 1, "name": "Alice Cahill", "longitude": "-10.27699"},
            {"latitude": "53.2451022", "user_id": 4, "name": "Ian Kehoe", "longitude": "-6.238335"}
        ]

        nearby_customers = NearByCustomers.get_nearby_customers(customers, 100)

        self.assertEqual(len(nearby_customers), 1)
        self.assertDictEqual(
            {"latitude": "53.2451022", "user_id": 4, "name": "Ian Kehoe", "longitude": "-6.238335"}
            , nearby_customers[0]
        )
