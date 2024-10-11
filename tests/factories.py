"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Inventory


class InventoryFactory(factory.Factory):
    """Creates fake inventory items"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    quantity = factory.Faker("random_int", min=0, max=10000)
    condition = FuzzyChoice(choices=["NEW", "OPEN_BOX", "USED"])
    stock_level = FuzzyChoice(choices=["LOW", "MEDIUM", "HIGH"])
