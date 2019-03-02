from unittest2 import TestCase

from src.exceptions import ParsingFailedException
from src.parser import TextParser


class TextParserTestCase(TestCase):

    def setUp(self):
        pass

    def test_parser_with_empty_text(self):
        data = ""
        with self.assertRaises(ParsingFailedException):
            TextParser.parse(data)

    def test_parser_with_malformed_text(self):
        data = "{'latitude': '123123123'}^%"
        with self.assertRaises(ParsingFailedException):
            TextParser.parse(data)

    def test_parser_with_none(self):
        data = None
        with self.assertRaises(ParsingFailedException):
            TextParser.parse(data)

    def test_parser_with_proper_text(self):
        data = "{\"latitude\": \"51.92893\", \"user_id\": 1, \"name\": \"Alice Cahill\", \"longitude\": \"-10.27699\"}"
        parsed_data = TextParser.parse(data)

        self.assertEqual(len(parsed_data), 1)

        self.assertDictEqual(
            {
                "latitude": "51.92893",
                "user_id": 1,
                "name": "Alice Cahill",
                "longitude": "-10.27699"
            }, parsed_data[0]
        )
