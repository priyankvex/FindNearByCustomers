import logging

from src.exceptions import LoadingCustomersFailedException
from src.great_circle_distance import GreatCircleDistance
from src.load_customers import LoadCustomers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


class NearByCustomers(object):

    OFFICE_COORDINATES = {
        "latitude": 53.339428,
        "longitude": -6.257664
    }

    @classmethod
    def get_nearby_customers(cls, customer_records, max_distance):

        if not customer_records:
            return []

        nearby_customers = []

        for customer_record in customer_records:
            customer_coordinates = {
                "latitude": float(customer_record["latitude"]),
                "longitude": float(customer_record["longitude"])
            }
            distance = GreatCircleDistance.calculate(cls.OFFICE_COORDINATES, customer_coordinates)

            if distance <= max_distance:
                nearby_customers.append(customer_record)

        nearby_customers = sorted(nearby_customers, key=lambda k: k["user_id"])

        return nearby_customers


if __name__ == "__main__":

    max_distance_km = 100

    try:
        customer_records = LoadCustomers.from_url("https://s3.amazonaws.com/intercom-take-home-test/customers.txt")
    except LoadingCustomersFailedException as error:
        logger.error("Failed to load customer records.\nError Message: {0}".format(str(error)))
    else:
        nearby_customers = NearByCustomers.get_nearby_customers(customer_records, max_distance_km)

        print(
            "Found {0} customers within {1} KMs to invite over for coffee!".format(
                len(nearby_customers), max_distance_km
            )
        )
        for customer in nearby_customers:
            print("Customer Name: {0}, User ID: {1}".format(customer["name"], customer["user_id"]))
