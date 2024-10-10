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
YourResourceModel Service

This service implements a REST API that allows you to Create, Read, Update
and Delete YourResourceModel
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Inventory, DataValidationError
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...
@app.route('/inventory', methods=['POST'])
def create_inventory():
    return jsonify({'error': "NOT IMPLEMENTED"}), 400

@app.route('/inventory', methods=['GET'])
def list_inventory():
    return jsonify({'error': "NOT IMPLEMENTED"}), 400

@app.route('/inventory/<int:id>', methods=['GET'])
def get_inventory(id):
    return jsonify({'error': "NOT IMPLEMENTED"}), 400

@app.route('/inventory/<int:id>', methods=['PUT'])
def update_inventory(id):
    return jsonify({'error': "NOT IMPLEMENTED"}), 400

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    app.logger.info(f"delete inventory with id: {id}")
    inventory = Inventory.find(id) 
    if inventory is None:
        app.logger.error(f"Inventory with id {id} not found.")
        return jsonify({"error": "Inventory not found"}), status.HTTP_404_NOT_FOUND

    try:
        inventory.delete()
        app.logger.info(f"Inventory with id {id} has deleted successfully.")
        return '', status.HTTP_204_NO_CONTENT
    except DataValidationError as e:
        app.logger.error(f"Error deleting inventory: {str(e)}")
        return jsonify({"error": str(e)}), status.HTTP_400_BAD_REQUEST