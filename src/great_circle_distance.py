import logging
import math
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class GreatCircleDistance(object):

    EARTH_RADIUS_KM = 6371

    @classmethod
    def calculate(cls, point_1, point_2, radius=EARTH_RADIUS_KM):

        cls.__validate_input(point_1)
        cls.__validate_input(point_2)

        x1 = point_1["latitude"]
        y1 = point_1["longitude"]
        x1 = math.radians(x1)
        y1 = math.radians(y1)

        x2 = point_2["latitude"]
        y2 = point_2["longitude"]
        x2 = math.radians(x2)
        y2 = math.radians(y2)

        central_angle = math.acos(
            (math.sin(x1) * math.sin(x2)) + (math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))
        )

        return central_angle * radius

    @classmethod
    def __validate_input(cls, input_point):

        schema = {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number"
                },
                "longitude": {
                    "type": "number"
                }
            }
        }

        try:
            validate(input_point, schema)
        except ValidationError as error:
            logger.error("Invalid input for the great circle distance. {0}. Error: {1}".format(input_point, error))
            raise ValidationError("Invalid input format")
