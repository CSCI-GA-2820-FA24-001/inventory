"""
Test Factory to make fake objects for testing
"""

import factory
import factory.fuzzy
from service.models import Inventory


class YourResourceModelFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")

    # Todo: Add your other attributes here...
    quantity =  factory.Faker('pyint', min_value = 0, max_value = 1000)
    condition = factory.fuzzy.FuzzyChoice(choices=["New", "Refurbished", "Used"])
    stock_level = factory.fuzzy.FuzzyChoice(choices=["In Stock", "Low"])