from unittest.mock import patch

from unittest2 import TestCase

from src.exceptions import LoadingCustomersFailedException
from src.load_customers import LoadCustomers


class LoadCustomersTestCase(TestCase):

    @patch("src.load_customers.read_from_file")
    def test_from_file_with_empty_text_file(self, file_read):
        file_read.return_value = ""
        file_name = "customers.txt"

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_file(file_name)

    @patch("src.load_customers.read_from_file")
    def test_from_file_with_malformed_text_file(self, file_read):
        file_read.return_value = "woueriouwioeruwioruiowuueiwreo"
        file_name = "customers.txt"

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_file(file_name)

    @patch("src.load_customers.read_from_file")
    def test_from_file_with_valid_text_file(self, file_read):
        data = "{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        file_read.return_value = data
        file_name = "customers.txt"

        LoadCustomers.from_file(file_name)
