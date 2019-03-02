import os

import requests

from parser import JSONParser, TextParser, XMLParser
from utils import read_from_file


class LoadCustomers(object):

    @classmethod
    def from_file(cls, filename):

        _, file_extension = os.path.splitext(filename)
        customers_data = read_from_file(filename).strip()

        parsed_customers = cls.__parse_customers_data(customers_data, filename)

        return parsed_customers

    @classmethod
    def from_url(cls, file_url):

        response = requests.get(file_url)

        customers_data = response.text.strip() if response.ok else None

        parsed_customers = cls.__parse_customers_data(customers_data, file_url)

        return parsed_customers

    @classmethod
    def __parse_customers_data(cls, customers_data, file_path):

        if not customers_data:
            return None

        _, file_extension = os.path.splitext(file_path)
        parser = cls.__get_parser_from_extension(file_extension)

        if parser:
            parsed_customers_data = parser.parse(customers_data)
        else:
            parsed_customers_data = None

        return parsed_customers_data

    @classmethod
    def __get_parser_from_extension(cls, extension):
        extension = extension.lower()

        if extension == ".json":
            return JSONParser
        elif extension == ".txt":
            return TextParser
        elif extension == ".xml":
            return XMLParser

        return None
