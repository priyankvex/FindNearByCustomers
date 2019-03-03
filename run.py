import logging

from src.exceptions import LoadingCustomersFailedException
from src.load_customers import LoadCustomers
from src.nearby_customers import NearByCustomers


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


if __name__ == "__main__":

    max_distance_km = 100

    try:
        customer_records = LoadCustomers.from_file("customers.txt")
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