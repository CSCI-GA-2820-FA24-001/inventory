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

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Inventory, DataValidationError
from service.common import status  # HTTP Status Codes


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
    return (
        jsonify(
            name="Inventory Service",
            version="1.0",
            paths=url_for("list_inventory", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/inventory", methods=["POST"])
def create_inventory():
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
    location_url = url_for("get_inventory", inventory_id=inventory.id, _external=True)
    return (
        jsonify(inventory.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/inventory", methods=["GET"])
def list_inventory():
    """List all Inventory items"""
    app.logger.info("Request to list all Inventory Items...")
    inventories = []

    # Parse any arguments from the query string
    name = request.args.get("name")
    quantity = request.args.get("quantity")
    condition = request.args.get("condition")
    stock_level = request.args.get("stock_level")

    inventories = Inventory.all()

    if name:
        app.logger.info("Filter by name")
        inventories = [inventory for inventory in inventories if inventory.name == name]
    if quantity:
        app.logger.info("Filter by quantity")
        inventories = [
            inventory
            for inventory in inventories
            if inventory.quantity == int(quantity)
        ]
    if condition:
        app.logger.info("Filter by condition")
        inventories = [
            inventory
            for inventory in inventories
            if inventory.condition.value == condition
        ]
    if stock_level:
        app.logger.info("Filter by stock level")
        inventories = [
            inventory
            for inventory in inventories
            if inventory.stock_level.value == stock_level
        ]

    results = [inventory.serialize() for inventory in inventories]
    app.logger.info("Returning %d inventory item", len(results))
    return jsonify(results), status.HTTP_200_OK


@app.route("/inventory/<int:inventory_id>", methods=["GET"])
def get_inventory(inventory_id):
    """Retrieve a single Inventory item"""
    app.logger.info("Request to Retrieve a Inventory with id [%s]", inventory_id)
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Inventory with id '{inventory_id}' was not found.",
        )

    return jsonify(inventory.serialize()), status.HTTP_200_OK


@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
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
    return jsonify(inventory.serialize()), status.HTTP_200_OK



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
<<<<<<< HEAD


@app.route("/inventory/<int:inventory_id>/restock/<path:quantity>", methods=["PUT"])
def restock_inventory(inventory_id, quantity):
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
        "Inventory with ID: %d restock by %d count.", inventory_id, quantity
    )
    return jsonify(inventory.serialize()), status.HTTP_200_OK
=======
>>>>>>> melody
