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
TestInventoryModel API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock
from service.models import db, Inventory
from service.common import status
from tests.factories import InventoryFactory
from wsgi import app


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/inventory"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestInventoryService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_inventory(self, count: int = 1) -> list:
        """Factory method to create inventory in bulk"""
        inventory = []
        for _ in range(count):
            test_inventory = InventoryFactory()
            response = self.client.post(BASE_URL, json=test_inventory.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test inventory item",
            )
            new_inventory = response.get_json()
            test_inventory.id = new_inventory["id"]
            inventory.append(test_inventory)
        return inventory

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # TEST CREATE
    def test_create_inventory(self):
        """It should Create a new Inventory"""
        test_inventory = InventoryFactory()
        logging.debug("Test Inventory: %s", test_inventory.serialize())
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["name"], test_inventory.name)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)
        self.assertEqual(new_inventory["condition"], test_inventory.condition.value)
        self.assertEqual(new_inventory["stock_level"], test_inventory.stock_level.value)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["name"], test_inventory.name)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)
        self.assertEqual(new_inventory["condition"], test_inventory.condition.value)
        self.assertEqual(new_inventory["stock_level"], test_inventory.stock_level.value)

    # TEST LIST
    def test_get_inventory_list(self):
        """It should get a list of Inventory items"""
        self._create_inventory(10)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 10)

    # TEST GET
    def test_get_inventory(self):
        """It should get an inventory item"""

        created_inventory = self._create_inventory()[0]

        logging.debug("Created inventory with id %s", created_inventory)
        response = self.client.get(f"{BASE_URL}/{created_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["name"], created_inventory.name)
        self.assertEqual(data["quantity"], created_inventory.quantity)
        self.assertEqual(data["condition"], created_inventory.condition.value)
        self.assertEqual(data["stock_level"], created_inventory.stock_level.value)

    def test_get_inventory_not_found(self):
        """It should not return an inventory that does not exist"""
        response = self.client.get(f"{BASE_URL}/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TEST UPDATE
    def test_update_inventory(self):
        """It should Update an existing Inventory"""
        # create a inventory item to update
        test_inventory = InventoryFactory()
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the inventory
        new_inventory = response.get_json()
        logging.debug(new_inventory)
        new_inventory["name"] = "updated-name"
        new_inventory["quantity"] = 100
        new_inventory["condition"] = "OPENBOX"
        new_inventory["stock_level"] = "LOW_STOCK"
        response = self.client.put(
            f"{BASE_URL}/{new_inventory['id']}", json=new_inventory
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_inventory = response.get_json()
        self.assertEqual(updated_inventory["name"], "updated-name")
        self.assertEqual(updated_inventory["quantity"], 100)
        self.assertEqual(updated_inventory["condition"], "OPENBOX")
        self.assertEqual(updated_inventory["stock_level"], "LOW_STOCK")

    # TEST DELETE
    def test_delete_inventory(self):
        """It should Delete an inventory item"""
        # First, create an inventory item
        test_inventory = self._create_inventory()[0]
        logging.debug("Created inventory with id %s", test_inventory.id)

        # Ensure the item has been created
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the inventory item
        response = self.client.delete(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to retrieve the deleted item, should return 404
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without an inventory id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_inventory_no_data(self):
        """It should not Create a inventory with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_inventory_no_content_type(self):
        """It should not Create a inventory with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_inventory_wrong_content_type(self):
        """It should not Create a inventory with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_inventory_bad_quantity(self):
        """It should not Create a inventory with bad quantity data"""
        test_inventory = InventoryFactory()
        logging.debug(test_inventory)
        # quantity should be a number, not a string
        test_inventory.quantity = "XXX"  # invalid quantity
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_inventory_bad_condition(self):
    #     """It should not Create a inventory with bad condition data"""
    #     inventory = InventoryFactory()
    #     logging.debug(inventory)
    #     # change condition to a bad string
    #     test_inventory = inventory.serialize()
    #     test_inventory["condition"] = "XXX"  # invalid condition
    #     response = self.client.post(BASE_URL, json=test_inventory)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ######################################################################
    #  T E S T   M O C K S
    ######################################################################

    # @patch("service.routes.Inventory.find_by_name")
    # def test_bad_request(self, bad_request_mock):
    #     """It should return a Bad Request error from Find By Name"""
    #     bad_request_mock.side_effect = DataValidationError()
    #     response = self.client.get(BASE_URL, query_string="name=fido")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("service.routes.Inventory.find_by_name")
    def test_mock_search_data(self, pet_find_mock):
        """It should showing how to mock data"""
        pet_find_mock.return_value = [MagicMock(serialize=lambda: {"name": "fido"})]
        response = self.client.get(BASE_URL, query_string="name=fido")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
