import json
import logging
from abc import ABC, abstractmethod
from json import JSONDecodeError

logger = logging.getLogger(__name__)


class AbstractParser(ABC):

    @classmethod
    def parse(cls, raw_data):
        raise NotImplementedError


class TextParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        raw_records = raw_data.strip().split("\n")
        parsed_records = []

        try:
            for record in raw_records:

                parsed_records.append(json.loads(record))
        except JSONDecodeError as error:
            logger.error(
                "Failed to parse JSON: {0}".format(error.msg), extra={"error": error}
            )
            return None
        else:
            return parsed_records


class JSONParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        pass


class XMLParser(AbstractParser):

    @classmethod
    def parse(cls, raw_data):
        pass
