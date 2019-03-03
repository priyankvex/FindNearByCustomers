from src.great_circle_distance import GreatCircleDistance


class NearByCustomers(object):

    OFFICE_COORDINATES = {
        "latitude": 53.339428,
        "longitude": -6.257664
    }

    @classmethod
    def get_nearby_customers(cls, customer_records, max_distance, target_location=None):
        """
        Given a list of customer records returns the list of customer records that are
        at the great circle distance of <= the max_distance from the office location.

        :param target_location: Location of the target (by default points to the office location).
        :param customer_records: List of customer records.
        :param max_distance: max distance to consider a customer near by.
        :return: list of near by customer records.
        """

        if not target_location:
            target_location = cls.OFFICE_COORDINATES

        if not customer_records:
            return []

        nearby_customers = []

        for customer_record in customer_records:
            customer_coordinates = {
                "latitude": float(customer_record["latitude"]),
                "longitude": float(customer_record["longitude"])
            }
            distance = GreatCircleDistance.calculate(target_location, customer_coordinates)

            if distance <= max_distance:
                nearby_customers.append(customer_record)

        nearby_customers = sorted(nearby_customers, key=lambda k: k["user_id"])

        return nearby_customers
