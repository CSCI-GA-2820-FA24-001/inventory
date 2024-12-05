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
Inventory Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Inventory
"""

from flask import jsonify, request, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Api, Resource, fields, reqparse

from service.models import Inventory, StockLevel, Condition
from service.common import status  # HTTP Status Codes

######################################################################
# FLASK REST X
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Inventory Demo REST API Service",
    description="This is inventory server.",
    default="inventory",
    default_label="Inventory operations",
    doc="/apidocs",
    prefix="/api",
)


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


######################################################################
# REST X
######################################################################
create_model = api.model(
    "Inventory",
    {
        "name": fields.String(required=True, description="The name of the Inventory"),
        "quantity": fields.Integer(
            required=True,
            description="The quantity of the Inventory",
        ),
        # pylint: disable=protected-access
        "condition": fields.String(
            enum=Condition._member_names_, description="The condition of the Inventory"
        ),
        # pylint: disable=protected-access
        "stock_level": fields.String(
            enum=StockLevel._member_names_,
            description="The stock level of the Inventory",
        ),
    },
)

inventory_model = api.inherit(
    "InventoryModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

inventory_args = reqparse.RequestParser()
inventory_args.add_argument(
    "name", type=str, location="args", required=False, help="List inventory by name"
)
inventory_args.add_argument(
    "condition",
    type=str,
    location="args",
    required=False,
    help="List inventory by condition",
)
inventory_args.add_argument(
    "stock_level",
    type=str,
    location="args",
    required=False,
    help="List inventory by stock_level",
)


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################
@api.route("/inventory/<inventory_id>")
@api.param("inventory_id", "The Inventory identifier")
@api.response(404, "Inventory not found")
class InventoryResource(Resource):
    """
    InventoryResource class

    Allows the manipulation of a single inventory
    GET /inventory{id} - Returns a inventory with the id
    PUT /inventory{id} - Update a inventory with the id
    DELETE /inventory{id} -  Deletes a inventory with the id
    """

    @api.doc("get_inventory")
    @api.marshal_with(inventory_model)
    def get(self, inventory_id):
        """Retrieve a single Inventory item"""
        app.logger.info("Request to Retrieve a Inventory with id [%s]", inventory_id)
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )

        return inventory.serialize(), status.HTTP_200_OK

    @api.doc("update_inventory")
    @api.response(404, "Pet not found")
    @api.response(400, "The posted Pet data was not valid")
    @api.expect(inventory_model)
    @api.marshal_with(inventory_model)
    def put(self, inventory_id):
        """Update an Inventory item"""
        app.logger.info("Request to Update an inventory with id [%s]", inventory_id)
        check_content_type("application/json")

        # Attempt to find the Inventory and abort if not found
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )

        # Update the Inventory with the new data
        data = request.get_json()
        app.logger.info("Processing: %s", data)
        inventory.deserialize(data)

        # Save the updates to the database
        inventory.update()

        app.logger.info("Inventory with ID: %d updated.", inventory_id)
        return inventory.serialize(), status.HTTP_200_OK

    @api.doc("delete_inventory")
    @api.response(204, "Inventory deleted")
    def delete(self, inventory_id):
        """Delete an Inventory item"""
        app.logger.info(f"Request to delete inventory with id: {inventory_id}")
        inventory = Inventory.find(inventory_id)
        if inventory:
            inventory.delete()
            app.logger.info(
                f"Inventory with id {inventory_id} has been deleted successfully."
            )

        # Always return 204_NO_CONTENT
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory
######################################################################
@api.route("/inventory", strict_slashes=False)
class InventoryCollection(Resource):
    """Handles all interactions with collections of Inventory"""

    @api.doc("create_inventory")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(inventory_model, code=201)
    def post(self):
        """Create an Inventory item"""
        app.logger.info("Request to Create an Inventory Item...")
        check_content_type("application/json")

        inventory = Inventory()
        # Get the data from the request and deserialize it
        data = request.get_json()
        app.logger.info("Processing: %s", data)
        inventory.deserialize(data)

        # Save the new Inventory to the database
        inventory.create()
        app.logger.info("Inventory with new id [%s] saved!", inventory.id)

        # Return the location of the new Inventory item
        location_url = api.url_for(
            InventoryResource, inventory_id=inventory.id, _external=True
        )
        return (
            inventory.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )

    @api.doc("list_inventory")
    @api.expect(inventory_args, validate=True)
    @api.marshal_list_with(inventory_model)
    def get(self):
        """List all Inventory items"""
        app.logger.info("Request to list all Inventory Items...")
        inventories = []

        # Parse query string parameters
        name = request.args.get("name")
        quantity_min = request.args.get("quantity_min")
        quantity_max = request.args.get("quantity_max")
        condition = request.args.get("condition")
        stock_level = request.args.get("stock_level")

        # Apply filtering based on query parameters
        if name:
            app.logger.info("Filtering by name: %s", name)
            inventories = Inventory.find_by_name(name)
        elif quantity_min or quantity_max:
            app.logger.info(
                f"Filtering by quantity range: [{quantity_min}, {quantity_max}]"
            )
            quantity_min = int(quantity_min) if quantity_min else 0
            quantity_max = int(quantity_max) if quantity_max else float("inf")
            inventories = Inventory.find_by_quantity_range(quantity_min, quantity_max)
        elif condition:
            app.logger.info("Filtering by condition: %s", condition)
            inventories = Inventory.find_by_condition(condition)
        elif stock_level:
            app.logger.info("Filtering by stock level: %s", stock_level)
            inventories = Inventory.find_by_stock_level(stock_level)
        else:
            inventories = Inventory.all()

        results = [i.serialize() for i in inventories]
        app.logger.info("Returning %d inventory items", len(results))
        return results, status.HTTP_200_OK


@api.route("/inventory/<inventory_id>/restock/<quantity>")
@api.param("inventory_id", "The Inventory identifier")
class RestockResource(Resource):
    """Restock action for a single inventory"""

    @api.doc("restock_inventory")
    @api.response(404, "Inventory not found")
    @api.response(200, "Inventory restocked")
    def put(self, inventory_id, quantity):
        """Restock an Inventory item (Can be negative)"""
        app.logger.info(
            "Request to restock [%s] count of inventory with id [%s]",
            quantity,
            inventory_id,
        )
        try:
            quantity = int(quantity)
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST, f"'{quantity}' is not a valid integer.")
        # Attempt to find the Inventory and abort if not found
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Inventory with id '{inventory_id}' was not found.",
            )

        new_quantity = inventory.quantity + quantity
        if new_quantity < 0:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Restocking by {quantity}: resulting quantity would be negative.",
            )
        inventory.quantity = new_quantity
        # Save the updates to the database
        inventory.update()
        app.logger.info(
            "Inventory with ID: %s restock by %d count.", inventory_id, quantity
        )
        return inventory.serialize(), status.HTTP_200_OK


def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
