import logging
import os

import requests
from jsonschema import validate, ValidationError
from requests.exceptions import MissingSchema

from exceptions import LoadingCustomersFailedException, ParsingFailedException
from parser import JSONParser, TextParser, XMLParser
from utils import read_from_file

logger = logging.getLogger(__name__)


class LoadCustomers(object):

    @classmethod
    def from_file(cls, filename):

        error_msg = None
        parsed_customers = None
        _, file_extension = os.path.splitext(filename)

        try:
            customers_data = read_from_file(filename).strip()
        except FileNotFoundError:
            error_msg = "File {0} couldn't be found".format(filename)
            logger.error(error_msg)
        else:
            parsed_customers, error_msg = cls.__parse_customers_data(customers_data, filename)

        if error_msg:
            raise LoadingCustomersFailedException(error_msg)

        return parsed_customers

    @classmethod
    def from_url(cls, file_url):

        error_msg = None
        parsed_customers = None

        try:
            response = requests.get(file_url, timeout=20)
        except MissingSchema:
            error_msg = "{0} doesn't seem to be a valid URL".format(file_url)
            logger.error(error_msg)
        else:
            customers_data = response.text.strip() if response.ok else None

            if not response.ok:
                error_msg = "Failed to get data from URL {0}. Error: {1}".format(file_url, response.content)
                logger.error(error_msg)
            else:
                parsed_customers, error_msg = cls.__parse_customers_data(customers_data, file_url)

        if error_msg:
            raise LoadingCustomersFailedException(error_msg)

        return parsed_customers

    @classmethod
    def __parse_customers_data(cls, customers_data, file_path):

        error_msg = None
        parsed_customers_data = None

        if not customers_data:
            return None

        _, file_extension = os.path.splitext(file_path)
        parser = cls.__get_parser_from_extension(file_extension)

        if not parser:
            error_msg = "File extension {0} is not supported.".format(file_extension)
            logger.error(error_msg)
        else:
            try:
                parsed_customers_data = parser.parse(customers_data) if parser else None
                cls.__validate_customers_data(parsed_customers_data)
            except (ParsingFailedException, ValidationError) as error:
                error_msg = str(error)

        return parsed_customers_data, error_msg

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

    @classmethod
    def __validate_customers_data(cls, customers_data):
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "string"
                    },
                    "longitude": {
                        "type": "string"
                    },
                    "user_id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            }
        }

        validate(customers_data, schema)
