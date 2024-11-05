"""
Models for Inventory

All of the models are stored in this module

Models
------
Inventory - An inventory item

Attributes:
-----------
name (string) - the name of the inventory item
quantity (int) - the quantity of the inventory item available
condition (enum) - the condition of the inventory item
stock_level (enum) - the stock level of the inventory item
"""

import os
import logging
from enum import Enum
from retry import retry
from flask_sqlalchemy import SQLAlchemy

# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 5))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


@retry(
    Exception,
    delay=RETRY_DELAY,
    backoff=RETRY_BACKOFF,
    tries=RETRY_COUNT,
    logger=logger,
)
def init_db() -> None:
    """Initialize Tables"""
    db.create_all()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Condition(Enum):
    """Enumeration of valid Inventory conditions"""

    NEW = "NEW"
    OPENBOX = "OPENBOX"
    USED = "USED"


class StockLevel(Enum):
    """Enumeration of valid Inventory stock levels"""

    IN_STOCK = "IN_STOCK"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class Inventory(db.Model):
    """
    Class that represents a Inventory
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Enum(Condition), nullable=False, server_default="NEW")
    stock_level = db.Column(
        db.Enum(StockLevel), nullable=False, server_default="IN_STOCK"
    )

    def __repr__(self):
        return f"<Inventory {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Inventory Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Inventory to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Inventory from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Inventory into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "condition": self.condition.value,  # convert enum to string
            "stock_level": self.stock_level.value,  # convert enum to string
        }

    def deserialize(self, data):
        """
        Deserializes a Inventory from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            if isinstance(data["quantity"], int):
                self.quantity = data["quantity"]
            else:
                raise DataValidationError(
                    "Invalid type for int [quantity]: " + str(type(data["quantity"]))
                )

            try:
                self.condition = Condition(data["condition"])
            except ValueError as exc:
                raise DataValidationError(f"Invalid value for Condition: {data['condition']}") from exc

            try:
                self.stock_level = StockLevel(data["stock_level"])
            except ValueError as exc:
                raise DataValidationError(f"Invalid value for StockLevel: {data['stock_level']}") from exc

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Inventory: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Inventory: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Inventory in the database"""
        logger.info("Processing all Inventory")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Inventory by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Inventory with the given name

        Args:
            name (string): the name of the Inventory you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_condition(cls, condition):
        """Returns all Inventory with the given condition

        Args:
            condition (string): the condition of the Inventory you want to match
        """
        logger.info("Processing condition query for %s ...", condition)
        return cls.query.filter(cls.condition == condition)

    @classmethod
    def find_by_stock_level(cls, stock_level):
        """Returns all Inventory with the given stock level

        Args:
            stock_level (string): the stock level of the Inventory you want to match
        """
        logger.info("Processing stock level query for %s ...", stock_level)
        return cls.query.filter(cls.stock_level == stock_level)
