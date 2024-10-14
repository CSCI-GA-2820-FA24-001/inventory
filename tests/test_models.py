######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Inventory Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app

from service.models import Inventory, db, DataValidationError
from .factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Inventory   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCaseBase(TestCase):
    """Base Test Case for common setup"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################


class TestInventoryModel(TestCaseBase):
    """Inventory Model CRUD Tests"""

    def test_update_no_id(self):
        """It should not Update a inventory with no id"""
        inventory = InventoryFactory()
        logging.debug(inventory)
        inventory.id = None
        self.assertRaises(DataValidationError, inventory.update)

    def test_deserialize_missing_data(self):
        """It should not deserialize a inventory with missing data"""
        data = {"id": 1, "name": "someitem2"}
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_quantity(self):
        """It should not deserialize a bad quantity attribute"""
        test_inventory = InventoryFactory()
        data = test_inventory.serialize()
        data["quantity"] = "XXX"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_condition(self):
        """It should not deserialize a bad condition attribute"""
        test_inventory = InventoryFactory()
        data = test_inventory.serialize()
        data["condition"] = "XXX"  # invalid condition
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_stock_level(self):
        """It should not deserialize a bad stock_level attribute"""
        test_inventory = InventoryFactory()
        data = test_inventory.serialize()
        data["stock_level"] = "XXX"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Inventory Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCaseBase):
    """Inventory Model Query Tests"""

    def test_find_inventory(self):
        """It should Find a Inventory by ID"""
        all_inventory = InventoryFactory.create_batch(5)
        for inv in all_inventory:
            inv.create()
        logging.debug(all_inventory)
        # make sure they got saved
        self.assertEqual(len(Inventory.all()), 5)
        # find the 2nd item in the list
        inventory = Inventory.find(all_inventory[1].id)
        self.assertIsNot(inventory, None)
        self.assertEqual(inventory.id, all_inventory[1].id)
        self.assertEqual(inventory.name, all_inventory[1].name)
        self.assertEqual(inventory.quantity, all_inventory[1].quantity)
        self.assertEqual(inventory.condition, all_inventory[1].condition)
        self.assertEqual(inventory.stock_level, all_inventory[1].stock_level)

    def test_find_by_name(self):
        """It should Find a Inventory by Name"""
        all_inventory = InventoryFactory.create_batch(10)
        for inv in all_inventory:
            inv.create()
        name = all_inventory[0].name
        count = len([inv for inv in all_inventory if inv.name == name])
        found = Inventory.find_by_name(name)
        self.assertEqual(found.count(), count)
        for inv in found:
            self.assertEqual(inv.name, name)

    def test_find_by_condition(self):
        """It should Find Inventory by Condition"""
        all_inventory = InventoryFactory.create_batch(10)
        for inv in all_inventory:
            inv.create()
        condition = all_inventory[0].condition
        count = len([inv for inv in all_inventory if inv.condition == condition])
        found = Inventory.find_by_condition(condition)
        self.assertEqual(found.count(), count)
        for inv in found:
            self.assertEqual(inv.condition, condition)

    def test_find_by_stock_level(self):
        """It should Find Inventory by Stock Level"""
        all_inventory = InventoryFactory.create_batch(10)
        for inv in all_inventory:
            inv.create()
        stock_level = all_inventory[0].stock_level
        count = len([inv for inv in all_inventory if inv.stock_level == stock_level])
        found = Inventory.find_by_stock_level(stock_level)
        self.assertEqual(found.count(), count)
        for inv in found:
            self.assertEqual(inv.stock_level, stock_level)
