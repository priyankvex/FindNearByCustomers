import json
from abc import ABC
from json import JSONDecodeError

from exceptions import ParsingFailedException


class AbstractParser(ABC):

    @classmethod
    def parse(cls, raw_data):
        raise NotImplementedError


class TextParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        raw_records = raw_data.strip().split("\n")
        parsed_records = []
        error_msg = None

        try:
            for record in raw_records:
                parsed_records.append(json.loads(record))
        except JSONDecodeError as error:
            error_msg = "Failed to parse JSON: {0}".format(error.msg)

        if error_msg:
            raise ParsingFailedException(error_msg)

        return parsed_records


class JSONParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        raise NotImplementedError


class XMLParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        raise NotImplementedError
