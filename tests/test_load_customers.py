from unittest.mock import patch

from requests import Response
from requests.exceptions import MissingSchema
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
    def test_from_file_with_file_no_found(self, file_read):
        data = "{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        file_read.return_value = data
        file_name = "customers.txt"

        file_read.side_effect = FileNotFoundError()

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_file(file_name)

    @patch("src.load_customers.read_from_file")
    def test_from_file_with_invalid_file_extension(self, file_read):
        data = "{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        file_read.return_value = data
        file_name = "customers.config"

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_file(file_name)

    @patch("src.load_customers.read_from_file")
    def test_from_file_with_valid_text_file(self, file_read):
        data = "{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        file_read.return_value = data
        file_name = "customers.txt"

        customers = LoadCustomers.from_file(file_name)

        self.assertEqual(len(customers), 1)
        self.assertDictEqual(
            {
                "latitude": "51.92893",
                "user_id": 1,
                "name": "Alice Cahill",
                "longitude": "-10.27699"
            }, customers[0]
        )

    @patch("src.load_customers.requests.get")
    def test_from_url_with_incorrect_extension(self, get):
        response = Response()
        response.status_code = 200
        response._content = ""

        get.return_value = response

        file_url = "http:exmaple.com/data.config"

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_url(file_url)

    @patch("src.load_customers.requests.get")
    def test_from_url_with_invalid_url(self, get):
        response = Response()
        response.status_code = 200
        response._content = ""

        get.side_effect = MissingSchema()

        file_url = "lihkdjfh"

        with self.assertRaises(LoadingCustomersFailedException):
            LoadCustomers.from_url(file_url)

    @patch("src.load_customers.requests.get")
    def test_from_url_with_valid_content(self, get):
        data = b"{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        response = Response()
        response.status_code = 200
        response._content = data

        get.return_value = response

        file_url = "http:example.com/data.txt"

        customers = LoadCustomers.from_url(file_url)

        self.assertEqual(len(customers), 1)
        self.assertDictEqual(
            {
                "latitude": "51.92893",
                "user_id": 1,
                "name": "Alice Cahill",
                "longitude": "-10.27699"
            }, customers[0]
        )
